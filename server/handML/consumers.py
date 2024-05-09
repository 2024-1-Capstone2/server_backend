import json
from channels.generic.websocket import AsyncWebsocketConsumer
from tensorflow.keras.models import load_model
from django.conf import settings
import time
import numpy as np

actions = [
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
    'A', 'B', 'C', 'D',
    'E', 'F', 'G', 'H',
    'I', 'J', 'K', 'L',
    'M', 'N', 'O', 'P',
    'Q', 'R', 'S', 'T',
    'U', 'V', 'W', 'X',
    'Y', 'Z',

    # 추가 단어
    # 'yes', 'no',
]

seq_length = 30

model = load_model(settings.MODEL_PATH)

class HandDataConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.seq = []
        self.action_seq = []
        self.recognized_actions = []
        self.all_recognized_actions = []  # 역대 인식된 단어들을 담을 리스트 초기화
        self.start_time = time.time()
        self.action_start_time = time.time()
        self.last_action = None
        self.counter = 0

    async def connect(self):
        await self.accept()
    
    # 연결을 끊고,
    async def disconnect(self, close_code):
        pass
    
    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        # print(f"Received hand data: {data}")
        self.counter += 1

        joint = np.zeros((21, 3))

        for j, lm in enumerate(data['landmarks']):
            joint[j] = [lm['x'], lm['y'], lm['z']]

        # 관절 간의 벡터값 구하기
        v1 = joint[[0,1,2,3,0,5,6,7,0,9,10,11,0,13,14,15,0,17,18,19], :] # 부모 관절
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

        self.seq.append(d)

        if len(self.seq) < seq_length:
            return

        # 위에서 구한 각도값으로 input 데이터 생성
        input_data = np.expand_dims(np.array(self.seq[-seq_length:], dtype=np.float32), axis=0)

        # input 데이터로 예측값 구하기
        y_pred = model.predict(input_data).squeeze()

        i_pred = int(np.argmax(y_pred))
        conf = y_pred[i_pred]

        # 예측값의 신뢰도(confidence)가 0.9 미만이라면 동작 다시 인식
        if conf < 0.9:
            return

        # 예측값의 신뢰도(confidence)가 0.9 이상이라면 동작들을 저장
        action = actions[i_pred]
        self.action_seq.append(action)

        if len(self.action_seq) < 3:
            return

        # 10초 동안 인식한 동작중 마지막으로 인식한 동작을 선택
        this_action = self.action_seq[-1]

        if (time.time() - self.action_start_time) <= 10:
            self.last_action = this_action
        else:
            if self.last_action:
                self.recognized_actions.append(self.last_action)
                self.all_recognized_actions.append(self.last_action)  # 처음 인식된 동작을 역대 인식된 동작 리스트에 추가
            else:
                self.recognized_actions.append("No action recognized")
                self.all_recognized_actions.append("No action recognized")  # 인식되지 않은 경우도 역대 인식된 동작 리스트에 추가
            self.last_action = None
            self.action_start_time = time.time()

        # 한 동작 인식 종료 후 3초 대기
        time.sleep(3)

        if self.counter % 20 == 0:
            print(f"Received hand data: {data}, {data}")

        if self.counter == 10:
            await self.send(text_data=json.dumps({'message': 'Data received successfully'}))
        elif self.counter == 100:
            await self.send(text_data=json.dumps({'message': 'Data received successfully v2'}))
        # elif self.counter == 150:
        #     await self.send(text_data=json.dumps({'message': 'disconnect'}))