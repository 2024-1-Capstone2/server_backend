from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework.decorators import api_view
from rest_framework.response import Response

import warnings
warnings.filterwarnings('ignore')

@api_view(['GET'])
def request_bus_boarding(request):
    channel_layer = get_channel_layer()
    async def async_group_send():
        await channel_layer.group_send(
            'javaScript_group',
            {
                'type': 'javaScript_message',
                'message_type': 'url_move',
                'message': str('busInfo/boardingId')
            }
    )

    async_to_sync(async_group_send)()

    return Response(status=200)

@api_view(['GET', 'POST'])
def request_bus_guide(request):
    channel_layer = get_channel_layer()
    async def async_group_send():
        await channel_layer.group_send(
            'javaScript_group',
            {
                'type': 'javaScript_message',
                'message_type': 'url_move',
                'message': str('busInfo/gate')
            }
    )

    async_to_sync(async_group_send)()

    return Response(status=200)

@api_view(['GET'])
def request_bus_schedule(request):
    channel_layer = get_channel_layer()
    async def async_group_send():
        await channel_layer.group_send(
            'javaScript_group',
            {
                'type': 'javaScript_message',
                'message_type': 'url_move',
                'message': str('busInfo/schedule')
            }
    )

    async_to_sync(async_group_send)()
    return Response(status=200)

@api_view(['GET'])
def request_bus_schedule_request(request):
    channel_layer = get_channel_layer()
    async def async_group_send():
        await channel_layer.group_send(
            'javaScript_group',
            {
                'type': 'javaScript_message',
                'message_type': 'url_move',
                'message': str('busInfo/schedule_number')
            }
    )

    return Response(status=200)