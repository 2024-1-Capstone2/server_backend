# -*- coding: utf-8 -*-
import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from handML.detection import load_model_by_name
from channels.layers import get_channel_layer
import asyncio
import deepl
from django.conf import settings

'''
flutterCommunicator: Flutter 앱과 통신하는 웹소켓 커넥터
javaScriptCommunicator: JavaScript 앱과 통신하는 웹소켓 커넥터
'''

auth_key = settings.SECRET_KEY # deepl api key

target_languages = ['KO', 'EN-US', 'ZH'] # 한국어, 영어, 중국어

def find_target_language():
    if settings.language_code == 'zh-hans':
        return 'ZH'
    elif settings.language_code == 'en-us':
        return 'EN-US'


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

    '''
    receive 메소드는 플러터로부터 메시지를 받으면, 현재 target 언어로 번역한다.
    그리고 javaScript_group에 번역된 메시지를 전송한다.
    '''

    async def receive(self, text_data=None, bytes_data=None):
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            return

        type = data.get('type')
        result = None

        # # deepl api를 이용하여 현재 설정의 언어로 번역
        message = data.get('message')
        translator = deepl.Translator(auth_key)
        target_language = find_target_language()
        result = translator.translate_text(message, target_lang=target_language)
        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            'javaScript_group',
            {
                'type': 'javaScript_message',
                'message_type': 'add_message',
                'message': result.text
            }
        )


# 비동기: AsyncWebsocketConsumer
# 동기: WebsocketConsumer

class JavaScriptCommunicator(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.origin = None
        self.message = []

    async def connect(self):
        # load_model_by_name을 판단하기 위한 origin을 받아온다.
        self.origin = self.scope['query_string'].decode().split('=')[1]
        await self.accept()
        await self.channel_layer.group_add(
            'javaScript_group',
            self.channel_name
        )
        load_model_by_name(self.origin)
        #logging.log(logging.INFO, f"Connected to {self.origin}")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            'javaScript_group',
            self.channel_name
        )

    async def send_data(self, data=None):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        pass

    async def javaScript_message(self, event):
        message = event['message']
        message_type = event['message_type']

        # 메시지를 클라이언트에게 보냅니다.
        await self.send(text_data=json.dumps({
            'message': message,
            'message_type': message_type
        }))

