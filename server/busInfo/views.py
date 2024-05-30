from django.shortcuts import render
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import translation
from .models import BusSchedule
from .busData import getBusInfo
import ast
from django.conf import settings
import json

import warnings
warnings.filterwarnings('ignore')

# Create your views here.
def index(request):
    return render(request, 'bus_schedule_request.html')

def bus_info_image(request, upperLevel, lowerLevel):
    return render(request, 'bus_info_image.html')

def crawl_and_save_bus_info(request):
    return render(request, 'bus_info.html')

@api_view(['GET'])
def request_question(request):
    channel_layer = get_channel_layer()
    async def async_group_send():
        await channel_layer.group_send(
            'javaScript_group',
            {
                'type': 'javaScript_message',
                'message': str('busInfo/question')
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
                'message': str('busInfo/reQuestion')
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
                'message': str('busInfo/busSchedule')
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
                'message': str('busInfo/informationDesk')
            }
    )

    async_to_sync(async_group_send)()

    return Response(status=200)

@api_view(['GET'])
def request_bus_guide(request):
    channel_layer = get_channel_layer()
    async def async_group_send():
        await channel_layer.group_send(
            'javaScript_group',
            {
                'type': 'javaScript_message',
                'message': str('busInfo/busGuide')
            }
    )

    async_to_sync(async_group_send)()

    return Response(status=200)

def question(request):
    return render(request, 'question/question.html')

def re_question(request):
    return render(request, 'question/reQuestion.html')

def bus_schedule(request):
    translation.activate('zh-hans')
    return render(request, 'bus_boarding/bus_schedule_request.html')

def information_desk(request):
    return render(request, 'information_desk.html')

def bus_guide(request):
    return render(request, 'bus_boarding/bus_guide.html')

def temp(request):
    info = getBusInfo()
    all_schedules = BusSchedule.objects.all()
    for schedule in all_schedules:
        print(schedule)

    return render(request, 'temp.html')
