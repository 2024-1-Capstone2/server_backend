from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.conf import settings
from django.utils import translation
from busInfo.models import City, District, BusStop, TimeTable, Bus
from datetime import datetime
import random, json

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
                'message_type': 'url_move',
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
    return render(request, 'select_small_region.html', {'number1': number1 , 'number2':number2 , 'districts1': districts1, 'districts2': districts2})

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

    return Response(bus_info_json, status=200)

def select_bus_stop(request):
    translation.activate(settings.LANGUAGE_CODE)
    district = District.objects.get(name='Gangnam-gu')
    bus_stops = district.bus_stops.all()
    number = [i for i in range(1, len(bus_stops)+1)]
    bus_dict = dict(zip(number, bus_stops))
    bus_dict_chunks = [dict(list(bus_dict.items())[i:i + 10]) for i in range(0, len(bus_dict), 10)]
    return render(request, 'select_bus_stop.html', {'bus_dict': bus_dict_chunks ,'bus_stops': bus_stops, 'number': number})

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
    # BusStop 인스턴스 가져오기
    bus_stop = BusStop.objects.get(name='Sinsa Station')

    # 해당 BusStop 인스턴스에 연결된 모든 TimeTable 인스턴스를 가져오기
    timetables = TimeTable.objects.filter(arrival_bus_stop=bus_stop)

    # 각 TimeTable 인스턴스에 대해
    bus = timetables.first().bus
    timetables = timetables.order_by('time')

    # 가장 빠른 시간과 가장 늦은 시간 가져오기
    earliest_time = timetables.first().time.strftime("%H:%M")
    latest_time = timetables.last().time.strftime("%H:%M")

    # 버스 정보를 JSON 형식으로 인코딩
    bus_info = {
        'bus_number': bus.number,
        'earliest_time': earliest_time,
        'bus_stop': bus_stop.name,
    }
    bus_info_json = json.dumps(bus_info)
    return Response(bus_info_json, status=200)

def bus_info(request):
    translation.activate(settings.LANGUAGE_CODE)
    # BusStop 인스턴스 가져오기
    bus_stop = BusStop.objects.get(name='Sinsa Station')

    # 해당 BusStop 인스턴스에 연결된 모든 TimeTable 인스턴스를 가져오기
    timetables = TimeTable.objects.filter(arrival_bus_stop=bus_stop)

    # 각 TimeTable 인스턴스에 대해
    bus = timetables.first().bus
    timetables = timetables.order_by('time')

    # 가장 빠른 시간과 가장 늦은 시간 가져오기
    earliest_time = timetables.first().time.strftime("%H:%M")
    latest_time = timetables.last().time.strftime("%H:%M")

    # 버스 정보를 JSON 형식으로 인코딩
    bus_info = {
        'bus_number': bus.number,
        'earliest_time': earliest_time,
        'latest_time': latest_time
    }
    bus_info_json = json.dumps(bus_info)

    # 웹소켓을 통해 버스 정보를 보냅니다.
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'javaScript_group',
        {
            'type': 'javaScript_message',
            'message_type': 'bus_info',
            'message': bus_info_json
        }
    )

    return render(request, 'bus_info.html', {'bus': bus, 'earliest_time': earliest_time, 'latest_time': latest_time})

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

    return render(request, 'select_bus_schedule.html', {
    'bus_number': bus_number,
    'timetables': timetables, 'date': date, 'chunks': chunks,
    'number1': number1, 'number2': number2, 'number3': number3})

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

def number_of_people(request):
    translation.activate(settings.LANGUAGE_CODE)
    total_seats = 28
    remaining_seats = random.randint(1, 28)
    time = datetime.now().time().strftime("%H:%M")
    date = datetime.now().strftime("%Y- %m- %d")
    bus_number = '6009'

    bus = Bus.objects.get(number=bus_number)

    adult_fare = bus.fare
    student_fare = int(adult_fare * 0.8)
    child_fare = int(adult_fare * 0.5)
    return render(request, 'number_people.html',
                  {'total_seats': total_seats, 'remaining_seats': remaining_seats, 'time': time, 'date': date,
                   'adult_fare': adult_fare, 'student_fare': student_fare, 'child_fare': child_fare, 'bus_number': bus_number})

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

def purchase_info(request):
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

    date = datetime.now().strftime("%Y- %m- %d")

    first_timetable = timetables.first()
    first_time = first_timetable.time.strftime("%H:%M")
    bus_number = first_timetable.bus.number

    seat_number = random.randint(15, 28)

    common_count = random.randint(0,1)
    student_count = random.randint(0,1)
    child_count = random.randint(0,1)
    total_count = common_count + student_count + child_count

    total_fare = common_count * bus.fare + student_count * int(bus.fare * 0.8) + child_count * int(bus.fare * 0.5)

    return render(request, 'purchase_info.html', {
    'bus_number': bus_number, 'total_fare': total_fare, 'common_count': common_count, 'student_count': student_count,
    'child_count': child_count,'timetables': timetables, 'date': date,
    'first_time': first_time, 'departure': bus_stop.name,
    'total_count': total_count, 'arrival': bus_stop.name, 'seat_number': seat_number})