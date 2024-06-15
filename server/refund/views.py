from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.utils import translation
from django.conf import settings

# web socket으로 안내원으로 부터 받은 단계가 표 요청일 때 표 요청
@api_view(['GET'])
def request_ticket(request):
    channel_layer = get_channel_layer()
    async def async_group_send():
        await channel_layer.group_send(
            'javaScript_group',
            {
                'type': 'javaScript_message',
                'message_type': 'url_move',
                'message': str('refund/')
            }
    )

    async_to_sync(async_group_send)()

    return Response(status=200)

# 환불 티켓 이후 질문
@api_view(['GET'])
def request_question(request):
    channel_layer = get_channel_layer()

    async def async_group_send():
        await channel_layer.group_send(
            'javaScript_group',
            {
                'type': 'javaScript_message',
                'message_type': 'url_move',
                'message': str('refund/question')
            }
        )

    async_to_sync(async_group_send)()

    return Response(status=200)

def ticket(request):
    translation.activate(settings.LANGUAGE_CODE)
    language_code = settings.LANGUAGE_CODE
    return render(request, 'refund_request_ticket.html', {'language_code': language_code})

def question(request):
    translation.activate(settings.LANGUAGE_CODE)
    return render(request, 'refund_question.html')

