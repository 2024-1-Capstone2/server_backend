from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework.decorators import api_view
from rest_framework.response import Response
from config.utils import get_recognition_result, RecognitionResultSerializer

import warnings
warnings.filterwarnings('ignore')

@api_view(['GET'])
def request_select_region(request):
    channel_layer = get_channel_layer()
    async def async_group_send():
        await channel_layer.group_send(
            'javaScript_group',
            {
                'type': 'javaScript_message',
                'message_type': 'url_move',
                'message': str('ticket/region')
            }
    )

    result = get_recognition_result('ticket/region')
    serializer = RecognitionResultSerializer(data={"response": result})
    serializer.is_valid(raise_exception=True)
    async_to_sync(async_group_send)()
    return Response(status=200, data=serializer.data)

@api_view(['GET'])
def request_select_small_region(request):
    channel_layer = get_channel_layer()
    async def async_group_send():
        await channel_layer.group_send(
            'javaScript_group',
            {
                'type': 'javaScript_message',
                'message_type': 'url_move',
                'message': str('ticket/small-region')
            }
    )
    result = get_recognition_result('ticket/small-region')
    serializer = RecognitionResultSerializer(data={"response": result})
    serializer.is_valid(raise_exception=True)
    async_to_sync(async_group_send)()

    return Response(status=200, data=serializer.data)

@api_view(['GET'])
def request_select_bus_stop(request):
    channel_layer = get_channel_layer()
    async def async_group_send():
        await channel_layer.group_send(
            'javaScript_group',
            {
                'type': 'javaScript_message',
                'message_type': 'url_move',
                'message': str('ticket/bus-stop')
            }
    )
    result = get_recognition_result('ticket/bus-stop')
    serializer = RecognitionResultSerializer(data={"response": result})
    serializer.is_valid(raise_exception=True)
    async_to_sync(async_group_send)()

    return Response(status=200, data=serializer.data)

@api_view(['GET'])
def request_bus_info(request):
    channel_layer = get_channel_layer()
    async def async_group_send():
        await channel_layer.group_send(
            'javaScript_group',
            {
                'type': 'javaScript_message',
                'message_type': 'url_move',
                'message': str('ticket/bus')
            }
    )
    result = get_recognition_result('ticket/bus')
    serializer = RecognitionResultSerializer(data={"response": result})
    serializer.is_valid(raise_exception=True)
    async_to_sync(async_group_send)()

    return Response(status=200, data=serializer.data)

@api_view(['GET'])
def request_bus_info_schedule(request):
    channel_layer = get_channel_layer()
    async def async_group_send():
        await channel_layer.group_send(
            'javaScript_group',
            {
                'type': 'javaScript_message',
                'message_type': 'url_move',
                'message': str('ticket/schedule')
            }
    )
    result = get_recognition_result('ticket/schedule')
    serializer = RecognitionResultSerializer(data={"response": result})
    serializer.is_valid(raise_exception=True)
    async_to_sync(async_group_send)()

    return Response(status=200, data=serializer.data)

@api_view(['GET'])
def request_number_of_people(request):
    channel_layer = get_channel_layer()
    async def async_group_send():
        await channel_layer.group_send(
            'javaScript_group',
            {
                'type': 'javaScript_message',
                'message_type': 'url_move',
                'message': str('ticket/cnt')
            }
    )
    result = get_recognition_result('ticket/cnt')
    serializer = RecognitionResultSerializer(data={"response": result})
    serializer.is_valid(raise_exception=True)
    async_to_sync(async_group_send)()

    return Response(status=200, data=serializer.data)

@api_view(['GET'])
def request_purchase_info(request):
    channel_layer = get_channel_layer()
    async def async_group_send():
        await channel_layer.group_send(
            'javaScript_group',
            {
                'type': 'javaScript_message',
                'message_type': 'url_move',
                'message': str('ticket/purchaseInfo')
            }
    )

    async_to_sync(async_group_send)()

    return Response(status=200)
