# -*- coding: utf-8 -*-
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from handML.detection import detect_action
from multiLanguage.utils import change_language_code
from channels.layers import get_channel_layer
import time
import ast
from asgiref.sync import async_to_sync


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
        # 연결 시 'flutter_group' 그룹에 가입합니다.
        await self.channel_layer.group_add(
            'flutter_group',
            self.channel_name
        )

    async def disconnect(self, close_code):
        # 연결 종료 시 'flutter_group' 그룹에서 탈퇴합니다.
        await self.channel_layer.group_discard(
            'flutter_group',
            self.channel_name
        )

    async def flutter_message(self, event):
        message = event['message']
        # 메시지를 클라이언트에게 보냅니다.
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def send_data(self, data):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            return
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
            data = change_language_code(lowerLevel)
            print(f"Message: {data}")
            message = data['message']
            json_string = json.dumps(message, ensure_ascii=False)
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
        await self.channel_layer.group_add(
            'javaScript_group',
            self.channel_name
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            'javaScript_group',
            self.channel_name
        )

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

        if time.time() - self.start_time > 5:
            if action :
                self.recognized_actions.append(action)
                self.all_recognized_actions.append(action)
            self.action_seq = []
            self.start_time = time.time()
            self.last_action = None
            print(f"Recognized actions: {self.all_recognized_actions}")
            channel_layer = get_channel_layer()
            await channel_layer.group_send(
                'flutter_group',
                {
                    'type': 'flutter_message',
                    'message': str(self.all_recognized_actions)
                }
            )

    async def javaScript_message(self, event):
        message = event['message']
        # 메시지를 클라이언트에게 보냅니다.
        await self.send(text_data=json.dumps({
            'message': message
        }))

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