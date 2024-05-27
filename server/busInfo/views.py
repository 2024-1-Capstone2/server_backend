from django.shortcuts import render
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

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
def request_reQuestion(request):
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

def question(request):
    return render(request, 'question.html')

def reQuestion(request):
    return render(request, 'reQuestion.html')
