from tensorflow.keras.models import load_model
import numpy as np
from django.conf import settings

# 미국 수어 단어 리스트
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
seq_length = 30

# 모델
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

seq = []
action_seq = []
# 현재 사용하는 모델 로드하는 변수
current_model = None
actions = None
this_action = None

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
    current_model.summary()
    actions = actions_dict[f'actions_{name}']

def detect_action(hand_data):

    try:
        hand_id = hand_data['handId']
        landmarks = (hand_data["landmarks"])
    except (KeyError, TypeError):
        print(f"Invalid hand data format: {hand_data}")
        return None

    joint = np.zeros((21, 3))

    for j, lm in enumerate(landmarks):
        joint[j] = [lm['x'], lm['y'], lm['z']]

    # 관절 간의 벡터값 구하기
    v1 = joint[[0,1,2,3,0,5,6,7,0,9,10,11,0,13,14,15,0,17,18,19], :] # 부모 관절
    v2 = joint[[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20], :] # 자식 관절
    v = v2 - v1 # [20, 3]
    # 벡터값 일반화하기
    v = v / np.linalg.norm(v, axis=1)[:, np.newaxis]

    # 각도값 구하기
    angle = np.arccos(np.einsum('nt,nt->n',
    v[[0,1,2,4,5,6,8,9,10,12,13,14,16,17,18],:],
        v[[1,2,3,5,6,7,9,10,11,13,14,15,17,18,19],:])) # [15,]

    angle = np.degrees(angle) # 각도 단위 변환

    d = np.concatenate([joint.flatten(), angle])

    # 손 인덱스에 따라 적절한 리스트에 데이터를 추가
    seq.append(d)

    if len(seq) < seq_length:
        return None

    # 위에서 구한 각도값으로 input 데이터 생성
    input_data = np.expand_dims(np.array(seq[-seq_length:], dtype=np.float32), axis=0)

    # input 데이터로 예측값 구하기, verbose 옵션으로 진행바 로그 관리

    y_pred = current_model.predict(input_data, verbose = 0).squeeze()

    i_pred = int(np.argmax(y_pred))
    conf = y_pred[i_pred]

    # 예측값의 신뢰도(confidence)가 0.9 미만이라면 동작 다시 인식하는 부분 안내원에게 알리기?
    if conf < 0.9:
        return None

    # 예측값의 신뢰도(confidence)가 0.9 이상이라면 동작들을 저장
    action = actions[i_pred]

    return action
