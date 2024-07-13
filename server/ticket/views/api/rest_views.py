from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework.decorators import api_view
from rest_framework.response import Response

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
                'message': str('ticket/selectRegion')
            }
    )

    async_to_sync(async_group_send)()
    return Response(status=200)

@api_view(['GET'])
def request_select_small_region(request):
    channel_layer = get_channel_layer()
    async def async_group_send():
        await channel_layer.group_send(
            'javaScript_group',
            {
                'type': 'javaScript_message',
                'message_type': 'url_move',
                'message': str('ticket/selectSmallRegion')
            }
    )

    async_to_sync(async_group_send)()

    return Response(status=200)

@api_view(['GET'])
def request_select_bus_stop(request):
    channel_layer = get_channel_layer()
    async def async_group_send():
        await channel_layer.group_send(
            'javaScript_group',
            {
                'type': 'javaScript_message',
                'message_type': 'url_move',
                'message': str('ticket/selectBusStop')
            }
    )

    async_to_sync(async_group_send)()

    return Response(status=200)

@api_view(['GET'])
def request_bus_info(request):
    channel_layer = get_channel_layer()
    async def async_group_send():
        await channel_layer.group_send(
            'javaScript_group',
            {
                'type': 'javaScript_message',
                'message_type': 'url_move',
                'message': str('ticket/busInfo')
            }
    )

    async_to_sync(async_group_send)()

    return Response(status=200)

@api_view(['GET'])
def request_bus_info_schedule(request):
    channel_layer = get_channel_layer()
    async def async_group_send():
        await channel_layer.group_send(
            'javaScript_group',
            {
                'type': 'javaScript_message',
                'message_type': 'url_move',
                'message': str('ticket/busInfoSchedule')
            }
    )

    async_to_sync(async_group_send)()


    return Response(status=200)

@api_view(['GET'])
def request_number_of_people(request):
    channel_layer = get_channel_layer()
    async def async_group_send():
        await channel_layer.group_send(
            'javaScript_group',
            {
                'type': 'javaScript_message',
                'message_type': 'url_move',
                'message': str('ticket/numberOfPeople')
            }
    )

    async_to_sync(async_group_send)()

    return Response(status=200)

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