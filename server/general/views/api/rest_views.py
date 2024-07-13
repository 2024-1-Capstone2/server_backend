from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework.decorators import api_view
from rest_framework.response import Response

import warnings
warnings.filterwarnings('ignore')

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

@api_view(['GET'])
def request_question(request):
    channel_layer = get_channel_layer()
    async def async_group_send():
        await channel_layer.group_send(
            'javaScript_group',
            {
                'type': 'javaScript_message',
                'message_type': 'url_move',
                'message': str('general/question_template')
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