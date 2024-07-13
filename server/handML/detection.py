import logging
from tensorflow.keras.models import load_model
import numpy as np
from django.conf import settings
from collections import deque
from django.utils import timezone
import threading, time
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def create_action_list(base_words, numbers=True, alphabet=True, additional_words=None):
    action_list = base_words.copy()
    if numbers:
        action_list.extend([str(i) for i in range(10)])
    if alphabet:
        action_list.extend(['A', 'N'])
    if additional_words:
        action_list.extend(additional_words)
    return action_list

actions_dict = {
    'actions_asl': create_action_list([
        'departures', 'bus', 'next', 'time', 'last', 'first', 'take(bus)', 'arrivals',
        'ticket', 'where', 'purchase', 'when', 'how_much', 'how_many', 'this', 'timetable',
        'earliest', 'take(time)', 'adult', 'child', 'student', 'seat', 'alone', 'together',
        'baggage', 'what', 'refund', 'miss', 'new', 'gate', 'late_night'
    ], additional_words=['retry', 'yes', 'no', 'change']),

    'actions_asl_num': create_action_list(['retry', 'yes', 'no']),

    'actions_asl_headcnt': create_action_list(
        ['retry', 'yes', 'no'], additional_words=['adult', 'child', 'student']
    ),

    'actions_asl_yesorno': ['retry', 'yes', 'no'],

    'actions_csl': create_action_list([
        '买票', '什么时候', '哪里', '时候', '尾班车', '头班车', '乘搭', '度过',
        '目的地', '出发地', '巴士', '下一班车', '多少', '时间表', '这', '走',
        '成年', '孩子', '学生', '座位', '单独', '一起', '行李', '什么',
        '退钱', '错过', '新的', '怎么', '夜'
    ], additional_words=['重试', '是', '不是']),

    'actions_csl_num': create_action_list(['重试', '是', '不是']),

    'actions_csl_headcnt': create_action_list(
        ['重试', '是', '不是'], additional_words=['成年', '孩子', '学生']
    ),

    'actions_csl_yesorno': ['重试', '是', '不是'],
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

# 현재 사용하는 모델 로드하는 변수
current_model = None
actions = None
this_action = None


def load_model_by_name(origin):
    global current_model
    global actions

    lang_code = 'asl' if settings.LANGUAGE_CODE == 'en' else 'csl'

    origin_to_name_suffix = {
        'busInfo': '_num',
        'refund': '_yesorno' if 'question' not in origin else '',
        'multiLanguage': '_num',
        'general': '',
        'ticket': '_num' if 'select' in origin or 'busInfoSchedule' in origin else '_headcnt' if 'number' in origin else '_yesorno',
    }

    name_suffix = next((suffix for key, suffix in origin_to_name_suffix.items() if key in origin), '')

    name = f'{lang_code}{name_suffix}'

    logging.log(logging.INFO, f"Model name: {name}")

    current_model = models[name]
    actions = actions_dict[f'actions_{name}']
    ActionDetector.get_instance().update_model(current_model, actions)

class ActionDetector:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(ActionDetector, cls).__new__(cls)
                    cls._instance.init()
        return cls._instance

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(ActionDetector, cls).__new__(cls)
                    cls._instance.init()
        return cls._instance

    def update_model(self, model, actions):
        self.current_model = model
        self.actions = actions

    def init(self):
        self.seq = deque(maxlen=10)
        self.recent_actions = deque(maxlen=10)
        self.DUPLICATE_THRESHOLD = 2
        self.current_model = current_model
        self.actions = actions
        self.last_action_time = None  # 마지막 동작 감지 시간을 저장


    def action_cleaner(self):
        self.seq.clear()
        self.recent_actions.clear()


    def detect_action(self, landmarks):
        with self._lock:
            if len(landmarks) < 21:
                print("Not enough landmarks")
                return None

            joint = np.array([[lm['x'], lm['y'], lm['z']] for lm in landmarks])

            v1 = joint[[0,1,2,3,0,5,6,7,0,9,10,11,0,13,14,15,0,17,18,19], :]
            v2 = joint[[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20], :]
            v = v2 - v1
            v = v / np.linalg.norm(v, axis=1)[:, np.newaxis]

            angle = np.arccos(np.einsum('nt,nt->n',
            v[[0,1,2,4,5,6,8,9,10,12,13,14,16,17,18],:],
                v[[1,2,3,5,6,7,9,10,11,13,14,15,17,18,19],:]))

            angle = np.degrees(angle)

            d = np.concatenate([joint.flatten(), angle])

            self.seq.append(d)

            if len(self.seq) < 3:
                return None

            input_data = np.expand_dims(np.array(list(self.seq), dtype=np.float32), axis=0)

            y_pred = self.current_model.predict(input_data, verbose=0).squeeze()

            i_pred = int(np.argmax(y_pred))
            conf = y_pred[i_pred]

            if conf < 0.9:
                return None

            action = self.actions[i_pred]

            # 중복 검사
            current_time = timezone.now()

            is_duplicate = False
            if self.last_action_time is not None:
                if (current_time - self.last_action_time).total_seconds() < self.DUPLICATE_THRESHOLD:
                    is_duplicate = True

            if not is_duplicate:
                self.recent_actions.append((action, current_time))
                actions_only = [action for action, _ in self.recent_actions]
                self.last_action_time = current_time
                self.seq.clear()
                channel_layer = get_channel_layer()
                async def async_group_send():
                    await channel_layer.group_send(
                        'javaScript_group',
                        {
                            'type': 'javaScript_message',
                            'message_type': 'recognized_actions',
                            'message': str(actions_only)
                        }
                    )
                    await channel_layer.group_send(
                        'flutter_group',
                        {
                            'type': 'flutter_message',
                            'message_type': 'recognized_actions',
                            'message': str(actions_only)
                        }
                    )

                async_to_sync(async_group_send)()

            return None