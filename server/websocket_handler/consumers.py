# -*- coding: utf-8 -*-
import json
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from handML.detection import detect_action, load_model_by_name
# from multiLanguage.utils import change_language_code
from channels.layers import get_channel_layer
import time
import ast
from asgiref.sync import async_to_sync
import asyncio
import websockets
import deepl
from multiLanguage.models import GlobalLanguage
from django.utils import translation
from asgiref.sync import sync_to_async
from django.conf import settings
from collections import deque

'''
flutterCommunicator: Flutter 앱과 통신하는 웹소켓 커넥터
javaScriptCommunicator: JavaScript 앱과 통신하는 웹소켓 커넥터
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
        message_type = event['message_type']

        # 메시지를 클라이언트에게 보냅니다.
        await self.send(text_data=json.dumps({
            'message': message,
            'message_type': message_type
        }))

    async def send_data(self, data):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            return

        type = data.get('type')
        result = None

        if settings.LANGUAGE_CODE == 'en':
            lang_code = 'EN-US'
        else:
            lang_code = 'ZH'

        # # deepl api를 이용하여 번역
        if(type == 'translate'):
            message = data.get('message')
            auth_key = "42878139-d11b-4c9d-a100-2abfb30d4a7c:fx"
            translator = deepl.Translator(auth_key)
            result = translator.translate_text(message, target_lang=lang_code)
        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            'javaScript_group',
            {
                'type': 'javaScript_message',
                'message_type': 'add_message',
                'message': result.text
            }
        )
        print(result.text)



seq_length = 30

# 비동기: AsyncWebsocketConsumer
# 동기: WebsocketConsumer
class JavaScriptCommunicator(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.action_seq = []
        self.recognized_actions = []
        self.start_time = time.time()
        self.last_data_time = time.time()
        self.last_action = None
        self.all_recognized_actions = []
        self.this_action = None
        self.all_recognized_actions_length = 0
        self.origin = None
        self.lock = asyncio.Lock()  # Lock 추가
        self.buffer = deque(maxlen=30)
        self.seq = []

    def connect(self):
        self.origin = self.scope['query_string'].decode().split('=')[1]
        print(f"Connected to {self.origin}")
        self.accept()
        async_to_sync(self.channel_layer.group_add(
            'javaScript_group',
            self.channel_name
        ))
        load_model_by_name(self.origin)


    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard(
            'javaScript_group',
            self.channel_name
        ))

    def send_data(self, data=None):
        pass

    def receive(self, text_data=None, bytes_data=None):

        action = None

        if len(self.buffer) > 5:
            return

        if text_data is not None:
            try:
                text_data = ast.literal_eval(text_data)
                if type(text_data) is not dict:
                    hand_data = json.loads(text_data)
                else:
                    hand_data = json.dumps(text_data)
            except json.JSONDecodeError:
                return

            if len(self.buffer) < 5:
                self.buffer.append(hand_data)
            elif len(self.buffer) == 5:
                action= detect_action(hand_data)
                self.action_seq.append(action)

            if len(self.action_seq) < 3:
                return

            self.this_action = self.action_seq[-1]

            if (time.time() - self.start_time) <= 8:
                self.last_action = self.this_action

            elif time.time() - self.start_time > 8:
                if self.last_action :
                    self.recognized_actions.append(self.last_action)
                    self.all_recognized_actions.append(self.last_action)
                self.start_time = time.time()
                self.last_action = None
                self.action_seq.clear()
                self.buffer.clear()
                # 인식한 단어가 증가하면 웹 소켓으로 전달하기.
            if len(self.all_recognized_actions) > self.all_recognized_actions_length:
                # origin url에 따라서 detect 된 언어로 변경
                ChangeLanguage(self, self.origin, self.all_recognized_actions)
                TicketSelectRegion(self, self.origin, self.all_recognized_actions)
                channel_layer = get_channel_layer()
                recognized_actions = self.all_recognized_actions
                if len(self.all_recognized_actions) >= 10:
                    recognized_actions = self.all_recognized_actions[-10:]
                print(recognized_actions)
                async_to_sync(channel_layer.group_send(
                    'flutter_group',
                    {
                        'type': 'flutter_message',
                        'message_type': 'recognized_actions',
                        'message': str(recognized_actions)
                    }
                ))
                message = json.dumps(str(recognized_actions), ensure_ascii=False)
                async_to_sync(channel_layer.group_send(
                    'javaScript_group',
                    {
                        'type': 'javaScript_message',
                        'message_type': 'recognized_actions',
                        'message': message
                    }
                ))
                self.all_recognized_actions_length = len(self.all_recognized_actions)


    async def javaScript_message(self, event):
        message = event['message']
        message_type = event['message_type']

        # 메시지를 클라이언트에게 보냅니다.
        await self.send(text_data=json.dumps({
            'message': message,
            'message_type': message_type
        }))

# 언어 변경
def ChangeLanguage(self, origin, all_recognized_actions):
    if 'choiceLanguage' in origin:
        print(all_recognized_actions[-1])
        newCode = all_recognized_actions[-1]
        if newCode == '1':
            settings.LANGUAGE_CODE = 'en'
        elif newCode == '2':
            settings.LANGUAGE_CODE = 'zh-hans'

# 후에 이 부분에 지역에 따라 바꾸는 부분 있어야 함.
# 지금은 그냥 동작만 확인하고 무조건 서울, 강남구, 강남역으로 통일
def TicketSelectRegion(self, origin, all_recognized_actions):
    if 'selectRegion' in origin:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send(
            'javaScript_group',
            {
                    'type': 'javaScript_message',
                    'message_type': 'url_move',
                    'message': str('ticket/selectSmallRegion?action=' + all_recognized_actions[-1])
            }
        ))
    elif 'selectSmallRegion' in origin:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send(
            'javaScript_group',
            {
                'type': 'javaScript_message',
                'message_type': 'url_move',
                'message': str('ticket/selectBusStop?action=' + all_recognized_actions[-1])
            }
        ))
