# -*- coding: utf-8 -*-
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from handML.detection import detect_action
from multiLanguage.utils import change_language_code
import time
import ast

'''
refundCommunicator: 환불 정보를 전달하는 웹소켓 커넥터
ticketCommunicator: 표 정보를 전달하는 웹소켓 커넥터
busCommunicator: 버스 정보를 전달하는 웹소켓 커넥터
flutterCommunicator: Flutter 앱과 통신하는 웹소켓 커넥터
'''

class FlutterCommunicator(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def send_data(self, data):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            return
        print(f"Received data: {data}")
        upperLevel = data['upperLevel']
        lowerLevel = data['lowerLevel']

        if upperLevel == 'refund':
            if lowerLevel == '1':
                pass
            pass
        elif upperLevel == 'ticket':
            pass
        elif upperLevel == 'bus':
            pass
        elif upperLevel == 'multiLanguage':
            # 여기는 언어 선택
            message = change_language_code(lowerLevel)
            print(f"Message: {message}")
            data = {
                "message": "환영합니다."
            }
            json_string = json.dumps(data, ensure_ascii=False)
            await self.send(text_data=json_string)



# 손관절 데이터 수집
class JavaScriptCommunicator(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.action_seq = []
        self.recognized_actions = []
        self.start_time = time.time()
        self.last_action = None
        self.all_recognized_actions = []

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def send_data(self, data=None):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        action = None
        if text_data is not None:
            try:
                text_data = ast.literal_eval(text_data)
                hand_data = json.loads(text_data)
            except json.JSONDecodeError:
                print(f"Invalid JSON data: {text_data}")
                return

            # print(f"Received hand data: {hand_data}")
            action = detect_action(hand_data)
            if action == "Not enough data":
                pass
            elif action is not None:
                self.action_seq.append(action)
            print(action)

        if time.time() - self.start_time > 5:
            if action :
                self.recognized_actions.append(action)
                self.all_recognized_actions.append(action)
            print(f"Sent actions: {action}")
            self.action_seq = []
            self.start_time = time.time()
            self.last_action = None

        if len(self.all_recognized_actions) > 0:
            print(f"Recognized actions: {self.all_recognized_actions}")

class LanguageCommunicator(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = 0

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def send_data(self, data):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        await self.send(text_data=json.dumps({'message': 'Data received successfully'}))
        pass