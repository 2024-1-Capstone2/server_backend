from django.shortcuts import render
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import translation
from django.conf import settings
from .busData import getBusInfo, test, addBusStop, addCity, addDistrict

import warnings
warnings.filterwarnings('ignore')

# Create your views here.
def index(request):
    return render(request, 'bus_boarding/bus_schedule_request.html')

def bus_info_image(request, upperLevel, lowerLevel):
    return render(request, 'bus_info_image.html')

def crawl_and_save_bus_info(request):
    return render(request, 'bus_info.html')

# bus_boarding

@api_view(['GET'])
def request_bus_boarding(request):
    channel_layer = get_channel_layer()
    async def async_group_send():
        await channel_layer.group_send(
            'javaScript_group',
            {
                'type': 'javaScript_message',
                'message_type': 'url_move',
                'message': str('busInfo/busBoarding')
            }
    )

    async_to_sync(async_group_send)()

    return Response(status=200)

def bus_boarding(request):
    translation.activate(settings.LANGUAGE_CODE)
    return render(request, 'bus_boarding/bus_boarding_request.html')

@api_view(['GET'])
def request_bus_guide(request):
    channel_layer = get_channel_layer()
    async def async_group_send():
        await channel_layer.group_send(
            'javaScript_group',
            {
                'type': 'javaScript_message',
                'message_type': 'url_move',
                'message': str('busInfo/busGuide')
            }
    )

    async_to_sync(async_group_send)()

    return Response(status=200)

def bus_guide(request):
    translation.activate(settings.LANGUAGE_CODE)
    return render(request, 'bus_boarding/bus_guide.html')

# schedule

@api_view(['GET'])
def request_bus_schedule(request):
    channel_layer = get_channel_layer()
    async def async_group_send():
        await channel_layer.group_send(
            'javaScript_group',
            {
                'type': 'javaScript_message',
                'message_type': 'url_move',
                'message': str('busInfo/busSchedule')
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
                'message': str('busInfo/busScheduleRequest')
            }
    )

    async_to_sync(async_group_send)()

    return Response(status=200)

def bus_schedule_request(request):
    translation.activate(settings.LANGUAGE_CODE)
    return render(request, 'schedule/bus_schedule_request.html')

def bus_schedule(request):
    translation.activate(settings.LANGUAGE_CODE)
    number1 = [i for i in range(1, 11)]
    number2 = [i for i in range(11, 21)]
    number3 = [i for i in range(21, 31)]
    return render(request, 'schedule/bus_schedule.html', {'number1': number1, 'number2': number2, 'number3': number3})

def temp(request):
    # addDistrict()
    test()
    return render(request, 'temp.html')

def temp1(request):
    getBusInfo()
    return render(request, 'temp.html')
