from django.shortcuts import render

# Create your views here.
import cv2
from django.http import StreamingHttpResponse
from django.views.decorators import gzip
import mediapipe as mp
import numpy as np
import time
from tensorflow.keras.models import load_model
from django.conf import settings

#
actions_dict = {
    'actions_asl': [
        # 기본 단어
        'departures', 'bus', 'next', 'time',
        'last', 'first', 'take(bus)', 'arrivals',
        'ticket', 'where', 'purchase', 'when',
        'how_much', 'how_many', 'this', 'timetable',
        'earliest', 'take(time)', 'adult', 'child',
        'student', 'seat', 'alone', 'together',
        'baggage', 'what', 'refund', 'miss',
        'new', 'gate', 'late_night',

        # 숫자
        '0', '1', '2', '3', '4',
        '5', '6', '7', '8', '9',

        # 알파벳
        'A', 'N',

        # 추가 단어
        'retry', 'yes', 'no', 'change',
    ],

    'actions_asl_num': [
        # 기본 단어
        'retry', 'yes', 'no',

        # 숫자
        '0', '1', '2', '3', '4',
        '5', '6', '7', '8', '9',

        # 알파벳
        'A', 'N',
    ],

    'actions_asl_headcnt': [
        # 기본 단어
        'retry', 'yes', 'no',

        # 숫자
        '0', '1', '2', '3', '4',
        '5', '6', '7', '8', '9',

        # 인원 종류
        'adult', 'child', 'student',
    ],

    'actions_asl_yesorno': [
        'retry', 'yes', 'no',
    ],

    # 중국 수어 단어 리스트

    'actions_csl': [
        # 기본 단어
        '买票', '什么时候', '哪里', '时候',
        '尾班车', '头班车', '乘搭', '度过',
        '目的地', '出发地', '巴士', '下一班车',
        '多少', '时间表', '这', '走',
        '成年', '孩子', '学生', '座位',
        '单独', '一起', '行李', '什么',
        '退钱', '错过', '新的', '怎么',
        '夜',

        # 숫자
        '0', '1', '2', '3', '4',
        '5', '6', '7', '8', '9',

        # 알파벳
        'A', 'N',

        # 추가 단어
        '重试', '是', '不是',
    ],

    'actions_csl_num':  [
        # 기본 단어
        '重试', '是', '不是',

        # 숫자
        '0', '1', '2', '3', '4',
        '5', '6', '7', '8', '9',

        # 알파벳
        'A', 'N',
    ],

    'actions_csl_headcnt': [
        # 기본 단어
        '重试', '是', '不是',

        # 숫자
        '0', '1', '2', '3', '4',
        '5', '6', '7', '8', '9',

        # 인원 종류
        '成年', '孩子', '学生',
    ],

    'actions_csl_yesorno':  [
        '重试', '是', '不是',
    ],
}
models = {
    'asl': load_model(settings.MODEL_PATH_ASL),
    'asl_headcnt': load_model(settings.MODEL_PATH_ASL_HEADCNT),
    'asl_num': load_model(settings.MODEL_PATH_ASL_NUM),
    'asl_yesorno': load_model(settings.MODEL_PATH_ASL_YESORNO),
    'csl': load_model(settings.MODEL_PATH_CSL),
    'csl_headcnt': load_model(settings.MODEL_PATH_CSL_HEADCNT),
    'csl_num': load_model(settings.MODEL_PATH_CSL_NUM),
    'csl_yesorno': load_model(settings.MODEL_PATH_CSL_YESORNO),
}
current_model = None
actions = None

def load_model_by_name(origin):
    global current_model
    global actions

    if settings.LANGUAGE_CODE == 'en':
        lang_code = 'asl'
    else:
        lang_code = 'csl'

    name = None
    if 'busInfo' in origin:
        name = f'{lang_code}_num'
    elif 'refund' in origin:
        if 'question' in origin:
            name = f'{lang_code}'
        else :
            name = f'{lang_code}_yesorno'
    elif 'multiLanguage' in origin:
        name = f'{lang_code}_num'
    elif 'general' in origin:
        name = f'{lang_code}'
    elif 'ticket' in origin:
        if 'select' in origin:
            name = f'{lang_code}_num'
        elif 'busInfoSchedule' in origin:
            name = f'{lang_code}_num'
        elif 'number' in origin:
            name = f'{lang_code}_headcnt'
        else:
            name = f'{lang_code}_yesorno'
    # 모델, action 리스트 로드
    current_model = models[name]
    actions = actions_dict[f'actions_{name}']


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)


def generate_frames():
    cap = cv2.VideoCapture(0)  # Change to the appropriate camera index if needed

    seq_length = 30
    seq = []
    action_seq = []
    recognized_actions = []
    all_recognized_actions = []
    start_time = time.time()
    action_start_time = time.time()
    last_action = None

    def put_text_on_image(image, text, position, font_path, font_size=40, color=(255, 255, 255)):
        image_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(image_pil)
        font = ImageFont.truetype(font_path, font_size)
        draw.text(position, text, font=font, fill=color)
        return cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)

    while cap.isOpened():
        ret, img = cap.read()
        if not ret:
            break

        img = cv2.flip(img, 1)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = hands.process(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        if result.multi_hand_landmarks is not None:
            for res in result.multi_hand_landmarks:
                joint = np.zeros((21, 3))
                for j, lm in enumerate(res.landmark):
                    joint[j] = [lm.x, lm.y, lm.z]

                v1 = joint[[0,1,2,3,0,5,6,7,0,9,10,11,0,13,14,15,0,17,18,19], :]
                v2 = joint[[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20], :]
                v = v2 - v1
                v = v / np.linalg.norm(v, axis=1)[:, np.newaxis]
                angle = np.arccos(np.einsum('nt,nt->n', v[[0,1,2,4,5,6,8,9,10,12,13,14,16,17,18],:], v[[1,2,3,5,6,7,9,10,11,13,14,15,17,18,19],:]))
                angle = np.degrees(angle)
                d = np.concatenate([joint.flatten(), angle])

                seq.append(d)

                if len(seq) < seq_length:
                    continue

                input_data = np.expand_dims(np.array(seq[-seq_length:], dtype=np.float32), axis=0)
                y_pred = model.predict(input_data, verbose=0).squeeze()

                i_pred = int(np.argmax(y_pred))
                conf = y_pred[i_pred]

                if conf < 0.9:
                    continue

                action = actions[i_pred]
                action_seq.append(action)

                if len(action_seq) < 3:
                    continue

                this_action = action_seq[-1]

                if (time.time() - action_start_time) <= 10:
                    img = put_text_on_image(img, f'{this_action}', (img.shape[1] - 200, img.shape[0] - 60), font_path=font_path,
                                            font_size=40, color=(255, 255, 255))
                    last_action = this_action


            if time.time() - action_start_time > 10:
                if last_action:
                    recognized_actions.append(last_action)
                    all_recognized_actions.append(last_action)
                else:
                    recognized_actions.append("No action recognized")
                    all_recognized_actions.append("No action recognized")

                last_action = None
                action_start_time = time.time()
                time.sleep(3)

            cv2.putText(img, f"Time left: {int(10 - (time.time() - action_start_time))} seconds", org=(50, 100),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255, 255, 255), thickness=2)

            if len(all_recognized_actions) > 0:
                recognized_text = ' '.join(all_recognized_actions)
                img = put_text_on_image(img, recognized_text, (50, img.shape[0] - 60), font_path=font_path, font_size=40,
                                        color=(255, 255, 255))

            ret, buffer = cv2.imencode('.jpg', img)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

            cap.release()


@gzip.gzip_page
def video_feed(request):
    return StreamingHttpResponse(generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')
