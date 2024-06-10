# -*- coding: utf-8 -*-
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from handML.detection import detect_action
# from multiLanguage.utils import change_language_code
from channels.layers import get_channel_layer
import time
import ast
from asgiref.sync import async_to_sync
import asyncio
import deepl
from multiLanguage.models import GlobalLanguage
from django.utils import translation
from asgiref.sync import sync_to_async

from django.conf import settings

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
        # print(data)
        type = data.get('type')
        # # deepl api를 이용하여 번역
        # if(type == 'translate'):
        #     message = data.get('message')
        #     auth_key = "42878139-d11b-4c9d-a100-2abfb30d4a7c:fx"
        #     translator = deepl.Translator(auth_key)
        #     result = translator.translate_text(message, target_lang="EN-US")
        message = data.get('message')
        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            'javaScript_group',
            {
                'type': 'javaScript_message',
                'message_type': 'add_message',
                'message': message
            }
        )
        # print(result.text)

# 손관절 데이터 수집
class JavaScriptCommunicator(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.action_seq = []
        self.recognized_actions = []
        self.start_time = time.time()
        self.last_action = None
        self.all_recognized_actions = []
        self.this_action = None
        self.all_recognized_actions_length = 0
        self.origin = None

    async def connect(self):
        self.origin = self.scope['query_string'].decode().split('=')[1]
        print(f"Connected to {self.origin}")
        await self.accept()
        await self.channel_layer.group_add(
            'javaScript_group',
            self.channel_name
        )
        # 연결 후 2초 뒤 부터 입력
        await asyncio.sleep(2)


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
                return

            # 이때 self.origin을 보고 어떤 단계인지에 따라 detect_action을 다르게 호출하는 부분을 추가.
            # 그리고 이후에 각 단계에 따라 처리를 다르게 해야함. 그 부분을 다루는 방법 생각.
            action = detect_action(hand_data)
            if action == "Not enough data":
                pass
            elif action is not None:
                self.action_seq.append(action)
                if len(self.action_seq) < 3:
                    pass
                self.this_action = self.action_seq[-1]
                if (time.time() - self.start_time) <= 5:
                    self.last_action = self.this_action
                    self.action_seq = []

            if time.time() - self.start_time > 5:
                if self.last_action :
                    # print(f"Recognized action: {self.last_action}")
                    self.recognized_actions.append(self.last_action)
                    self.all_recognized_actions.append(self.last_action)
                # else:
                #     self.recognized_actions.append("No action recognized")
                #     self.all_recognized_actions.append("No action recognized")
                self.start_time = time.time()
                self.last_action = None

            # 인식한 단어가 증가하면 웹 소켓으로 전달하기.
            if len(self.all_recognized_actions) > self.all_recognized_actions_length:
                # origin url에 따라서 detect 된 언어로 변경
                await ChangeLanguage(self, self.origin, self.all_recognized_actions)
                await TicketSelectRegion(self, self.origin, self.all_recognized_actions)
                channel_layer = get_channel_layer()
                await channel_layer.group_send(
                    'flutter_group',
                    {
                        'type': 'flutter_message',
                        'message_type': 'recognized_actions',
                        'message': str(self.all_recognized_actions)
                    }
                )
                await channel_layer.group_send(
                    'javaScript_group',
                    {
                        'type': 'javaScript_message',
                        'message_type': 'recognized_actions',
                        'message': str(self.all_recognized_actions)
                    }
                )
                self.all_recognized_actions_length = len(self.all_recognized_actions)
                await asyncio.sleep(2)

    async def javaScript_message(self, event):
        message = event['message']
        message_type = event['message_type']

        # 메시지를 클라이언트에게 보냅니다.
        await self.send(text_data=json.dumps({
            'message': message,
            'message_type': message_type
        }))

# 언어 변경
async def ChangeLanguage(self, origin, all_recognized_actions):
    if 'choiceLanguage' in origin:
        language_code = GlobalLanguage.objects.get(pk=1)
        newCode = all_recognized_actions[-1]
        if newCode == '1':
            language_code.code = 'en'
            settings.LANGUAGE_CODE = 'en'
            language_code.api_name = 'EN-US'
            await sync_to_async(language_code.save)()
        elif newCode == '2':
            language_code.code = 'zh-hans'
            settings.LANGUAGE_CODE = 'zh-hans'
            language_code.api_name = 'ZH'
            await sync_to_async(language_code.save)()
        await asyncio.sleep(1)

# 후에 이 부분에 지역에 따라 바꾸는 부분 있어야 함.
# 지금은 그냥 동작만 확인하고 무조건 서울, 강남구, 강남역으로 통일
async def TicketSelectRegion(self, origin, all_recognized_actions):
    if 'selectRegion' in origin:
        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            'javaScript_group',
            {
                    'type': 'javaScript_message',
                    'message_type': 'url_move',
                    'message': str('ticket/selectSmallRegion?action=' + all_recognized_actions[-1])
            }
        )
        await asyncio.sleep(1)
    elif 'selectSmallRegion' in origin:
        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            'javaScript_group',
            {
                'type': 'javaScript_message',
                'message_type': 'url_move',
                'message': str('ticket/selectBusStop?action=' + all_recognized_actions[-1])
            }
        )
        await asyncio.sleep(1)