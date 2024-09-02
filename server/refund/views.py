from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.utils import translation
from django.conf import settings
from config.utils import get_recognition_result, RecognitionResultSerializer


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
                'message': str('refund/ticket')
            }
    )
    result = get_recognition_result('refund/ticket')
    serializer = RecognitionResultSerializer(data={"response": result})
    serializer.is_valid(raise_exception=True)
    async_to_sync(async_group_send)()

    return Response(status=200, data=serializer.data)

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
    result = get_recognition_result('refund/question')
    serializer = RecognitionResultSerializer(data={"response": result})
    serializer.is_valid(raise_exception=True)
    async_to_sync(async_group_send)()

    return Response(status=200, data=serializer.data)

def ticket(request):
    translation.activate(settings.LANGUAGE_CODE)
    return render(request, 'refund_request_ticket.html')

def question(request):
    translation.activate(settings.LANGUAGE_CODE)
    return render(request, 'refund_question.html')

