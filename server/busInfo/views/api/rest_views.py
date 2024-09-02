from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework.decorators import api_view
from rest_framework.response import Response
from config.utils import get_recognition_result, RecognitionResultSerializer

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
                'message': str('busInfo/boarding-id')
            }
    )

    result = get_recognition_result('busInfo/boarding-id')
    serializer = RecognitionResultSerializer(data={"response": result})
    serializer.is_valid(raise_exception=True)
    async_to_sync(async_group_send)()

    return Response(status=200, data=serializer.data)

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

    result = get_recognition_result('busInfo/gate')
    serializer = RecognitionResultSerializer(data={"response": result})
    serializer.is_valid(raise_exception=True)
    async_to_sync(async_group_send)()

    return Response(serializer.data, status=200)

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
    result = get_recognition_result('busInfo/schedule')
    serializer = RecognitionResultSerializer(data={"response": result})
    serializer.is_valid(raise_exception=True)
    async_to_sync(async_group_send)()
    return Response(serializer.data, status=200)

@api_view(['GET'])
def request_bus_schedule_request(request):
    channel_layer = get_channel_layer()
    async def async_group_send():
        await channel_layer.group_send(
            'javaScript_group',
            {
                'type': 'javaScript_message',
                'message_type': 'url_move',
                'message': str('busInfo/schedule-number')
            }
    )
    result = get_recognition_result('busInfo/schedule-number')
    serializer = RecognitionResultSerializer(data={"response": result})
    serializer.is_valid(raise_exception=True)
    async_to_sync(async_group_send)()
    return Response(serializer.data, status=200)
