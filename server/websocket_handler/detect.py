# detect.py
import numpy as np
from tensorflow.keras.models import load_model
from django.conf import settings

# Keras 모델 로드
model = load_model('path_to_your_model.h5')
actions = ['action1', 'action2', 'action3']  # select_action과 동일하게 설정

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

def predict_action(data_buffer, seq_length):
    if len(data_buffer) < seq_length:
        return None, None

    input_data = np.expand_dims(np.array(data_buffer, dtype=np.float32), axis=0)
    y_pred = model.predict(input_data, verbose=0).squeeze()
    i_pred = int(np.argmax(y_pred))
    conf = y_pred[i_pred]

    if conf < 0.9:
        return None, None

    action = actions[i_pred]
    return action, conf
