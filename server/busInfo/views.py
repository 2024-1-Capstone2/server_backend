from django.shortcuts import render
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import translation
from django.conf import settings
from .busData import getBusInfo, test, addBusStop, addCity, addDistrict
from busInfo.models import City, District, BusStop, TimeTable, Bus
from datetime import datetime

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
    # BusStop 인스턴스 가져오기
    bus_stop = BusStop.objects.get(name='Sinsa Station')

    # 해당 BusStop 인스턴스에 연결된 모든 TimeTable 인스턴스를 가져옵니다.
    timetables = TimeTable.objects.filter(arrival_bus_stop=bus_stop)

    # 각 TimeTable 인스턴스에 대해
    bus = timetables.first().bus
    timetables = timetables.order_by('time')

    now = datetime.now().time()
    timetables = timetables.filter(time__gte=now).order_by('time')

    # timetables를 10개씩 분할하면서 time 필드만 가져오고 시간,분만 표현
    chunks = [[item.time.strftime("%H:%M") for item in timetables[i:i + 10]] for i in range(0, len(timetables), 10)]

    # 각 분할된 리스트의 길이가 10이 아닐 경우, 리스트에 빈 문자열(" ")을 추가
    for chunk in chunks:
        while len(chunk) < 10:
            chunk.append(" ")

    date = datetime.now().strftime("%Y- %m- %d")

    first_timetable = timetables.first()
    bus_number = first_timetable.bus.number

    number1 = [i for i in range(1, 11)]
    number2 = [i for i in range(11, 21)]
    number3 = [i for i in range(21, 31)]

    return render(request, 'schedule/bus_schedule.html', {
    'bus_number': bus_number,
    'timetables': timetables, 'date': date, 'chunks': chunks,
    'number1': number1, 'number2': number2, 'number3': number3})

def temp(request):
    # addDistrict()
    test()
    return render(request, 'temp.html')

def temp1(request):
    getBusInfo()
    return render(request, 'temp.html')
