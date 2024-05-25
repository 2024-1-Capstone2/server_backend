from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# web socket으로 안내원으로 부터 받은 단계가 표 요청일 때 표 요청
@api_view(['GET'])
def request_ticket(request):
    channel_layer = get_channel_layer()
    async def async_group_send():
        await channel_layer.group_send(
            'javaScript_group',
            {
                'type': 'javaScript_message',
                'message': str('refund/')
            }
    )

    async_to_sync(async_group_send)()

    return Response(status=200)

# 표 소지 여부 yes - 환불 처리 후, 새 표 구매 요청 확인 페이지로 이동
@api_view(['GET'])
def ask_buy_ticket(request):
    channel_layer = get_channel_layer()

    async def async_group_send():
        await channel_layer.group_send(
            'javaScript_group',
            {
                'type': 'javaScript_message',
                'message': str('refund/new')
            }
        )

    async_to_sync(async_group_send)()

    return Response(status=200)

# 표 소지 여부 no 환불 불가능 페이지로 이동


def index(request):
    return render(request, 'refund_precautions.html')

def new(request):
    return render(request, 'refund_new.html')
