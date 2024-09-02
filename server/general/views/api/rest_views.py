from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework.decorators import api_view
from rest_framework.response import Response
from config.utils import get_recognition_result, RecognitionResultSerializer

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
                'message': str('general/')
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
                'message': str('general/question')
            }
    )

    result = get_recognition_result('general/question')
    serializer = RecognitionResultSerializer(data={"response": result})
    serializer.is_valid(raise_exception=True)
    async_to_sync(async_group_send)()

    return Response(status=200, data=serializer.data)

@api_view(['GET'])
def request_re_question(request):
    channel_layer = get_channel_layer()
    async def async_group_send():
        await channel_layer.group_send(
            'javaScript_group',
            {
                'type': 'javaScript_message',
                'message_type': 'url_move',
                'message': str('general/re-question')
            }
    )

    result = get_recognition_result('general/re-question')
    serializer = RecognitionResultSerializer(data={"response": result})
    serializer.is_valid(raise_exception=True)

    async_to_sync(async_group_send)()

    return Response(status=200, data=serializer.data)

@api_view(['GET'])
def request_information_desk(request):
    channel_layer = get_channel_layer()
    async def async_group_send():
        await channel_layer.group_send(
            'javaScript_group',
            {
                'type': 'javaScript_message',
                'message_type': 'url_move',
                'message': str('general/info-desk')
            }
    )

    result = get_recognition_result('general/info-desk')
    serializer = RecognitionResultSerializer(data={"response": result})
    serializer.is_valid(raise_exception=True)

    async_to_sync(async_group_send)()

    return Response(status=200, data=serializer.data)
