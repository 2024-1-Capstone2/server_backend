from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
# Create your views here.
from django.conf import settings
from django.utils import translation
from busInfo.models import City, District, BusStop, TimeTable
from datetime import datetime

def index(request):
    return render(request, 'select_region.html')

def index1(request):
    return render(request, 'slide-.html')

@api_view(['GET'])
def request_select_region(request):
    channel_layer = get_channel_layer()
    async def async_group_send():
        await channel_layer.group_send(
            'javaScript_group',
            {
                'type': 'javaScript_message',
                'message': str('ticket/selectRegion')
            }
    )

    async_to_sync(async_group_send)()

    return Response(status=200)

def select_region(request):
    city = City.objects.all()
    translation.activate(settings.LANGUAGE_CODE)
    return render(request, 'select_region.html', {'city': city})

@api_view(['GET'])
def request_select_small_region(request):
    channel_layer = get_channel_layer()
    async def async_group_send():
        await channel_layer.group_send(
            'javaScript_group',
            {
                'type': 'javaScript_message',
                'message': str('ticket/selectSmallRegion')
            }
    )

    async_to_sync(async_group_send)()

    return Response(status=200)

def select_small_region(request):
    action = request.GET.get('action')
    print(action)
    districts = list(District.objects.all())
    districts1 = districts[:12]
    districts2 = districts[12:24]
    translation.activate(settings.LANGUAGE_CODE)
    number1 = [i for i in range(1, 13)]
    number2 = [i for i in range(13, 25)]
    return render(request, 'select_region_temp.html', {'number1': number1 , 'number2':number2 , 'districts1': districts1, 'districts2': districts2})

@api_view(['GET'])
def request_bus_schedule_info(request):
    channel_layer = get_channel_layer()
    async def async_group_send():
        await channel_layer.group_send(
            'javaScript_group',
            {
                'type': 'javaScript_message',
                'message': str('ticket/busScheduleInfo')
            }
    )

    async_to_sync(async_group_send)()

    return Response(status=200)

def bus_schedule_info(request):
    number1 = [i for i in range(1, 11)]
    number2 = [i for i in range(11, 21)]
    number3 = [i for i in range(20, 31)]
    print(number1)
    translation.activate(settings.LANGUAGE_CODE)
    return render(request, 'bus_schedule_info.html', {'number1': number1, 'number2': number2, 'number3': number3})

@api_view(['GET'])
def request_select_bus_stop(request):
    channel_layer = get_channel_layer()
    async def async_group_send():
        await channel_layer.group_send(
            'javaScript_group',
            {
                'type': 'javaScript_message',
                'message': str('ticket/selectBusStop')
            }
    )

    async_to_sync(async_group_send)()

    return Response(status=200)

def select_bus_stop(request):
    translation.activate(settings.LANGUAGE_CODE)
    district = District.objects.get(name='Gangnam-gu')
    bus_stops = district.bus_stops.all()
    number = [i for i in range(1, len(bus_stops)+1)]
    return render(request, 'select_bus_stop.html', {'bus_stops': bus_stops, 'number': number})

@api_view(['GET'])
def request_bus_info(request):
    channel_layer = get_channel_layer()
    async def async_group_send():
        await channel_layer.group_send(
            'javaScript_group',
            {
                'type': 'javaScript_message',
                'message': str('ticket/busInfo')
            }
    )

    async_to_sync(async_group_send)()

    return Response(status=200)

def bus_info(request):
    translation.activate(settings.LANGUAGE_CODE)
    # BusStop 인스턴스 가져오기
    bus_stop = BusStop.objects.get(name='Sinsa Station')

    # 해당 BusStop 인스턴스에 연결된 모든 TimeTable 인스턴스를 가져옵니다.
    timetables = TimeTable.objects.filter(arrival_bus_stop=bus_stop)

    # 각 TimeTable 인스턴스에 대해
    bus = timetables.first().bus
    timetables = timetables.order_by('time')

    # 가장 빠른 시간과 가장 늦은 시간 가져오기
    earliest_time = timetables.first().time.strftime("%H:%M")
    latest_time = timetables.last().time.strftime("%H:%M")

    return render(request, 'bus_info.html', {'bus': bus, 'earliest_time': earliest_time, 'latest_time': latest_time})

@api_view(['GET'])
def request_bus_info_schedule(request):
    channel_layer = get_channel_layer()
    async def async_group_send():
        await channel_layer.group_send(
            'javaScript_group',
            {
                'type': 'javaScript_message',
                'message': str('ticket/busInfoSchedule')
            }
    )

    async_to_sync(async_group_send)()

    return Response(status=200)

def bus_info_schedule(request):
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

    number1 = [i for i in range(1, 11)]
    number2 = [i for i in range(11, 21)]
    number3 = [i for i in range(21, 31)]

    print(timetables)
    return render(request, 'bus_info_schedule.html', {'timetables': timetables})