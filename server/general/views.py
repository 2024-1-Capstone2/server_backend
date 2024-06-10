from django.shortcuts import render
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.conf import settings
from django.utils import translation
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.
# question

# 초기화면

@api_view(['GET'])
def request_initial_screen(request):
    channel_layer = get_channel_layer()
    async def async_group_send():
        await channel_layer.group_send(
            'javaScript_group',
            {
                'type': 'javaScript_message',
                'message_type': 'url_move',
                'message': str('general/initialScreen')
            }
    )

    async_to_sync(async_group_send)()

    return Response(status=200)

def initial_screen(request):
    return render(request, 'screen.html')

# question

@api_view(['GET'])
def request_question(request):
    channel_layer = get_channel_layer()
    async def async_group_send():
        await channel_layer.group_send(
            'javaScript_group',
            {
                'type': 'javaScript_message',
                'message_type': 'url_move',
                'message': str('general/question')
            }
    )

    async_to_sync(async_group_send)()

    return Response(status=200)

@api_view(['GET'])
def request_re_question(request):
    channel_layer = get_channel_layer()
    async def async_group_send():
        await channel_layer.group_send(
            'javaScript_group',
            {
                'type': 'javaScript_message',
                'message_type': 'url_move',
                'message': str('general/reQuestion')
            }
    )

    async_to_sync(async_group_send)()

    return Response(status=200)

def question(request):
    translation.activate(settings.LANGUAGE_CODE)
    return render(request, 'question/question.html')

def re_question(request):
    translation.activate(settings.LANGUAGE_CODE)
    return render(request, 'question/reQuestion.html')

# information desk

@api_view(['GET'])
def request_information_desk(request):
    channel_layer = get_channel_layer()
    async def async_group_send():
        await channel_layer.group_send(
            'javaScript_group',
            {
                'type': 'javaScript_message',
                'message_type': 'url_move',
                'message': str('general/informationDesk')
            }
    )

    async_to_sync(async_group_send)()

    return Response(status=200)

def information_desk(request):
    translation.activate(settings.LANGUAGE_CODE)
    return render(request, 'information_desk.html')