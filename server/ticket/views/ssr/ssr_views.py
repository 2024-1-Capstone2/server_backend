from django.conf import settings
from django.utils import translation
from busInfo.models import City, District, BusStop, TimeTable, Bus
from datetime import datetime
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework.response import Response
import random, json
from django.shortcuts import render

import warnings
warnings.filterwarnings('ignore')

def select_region(request):
    city = City.objects.all()
    translation.activate(settings.LANGUAGE_CODE)
    return render(request, 'select_region.html', {'city': city})

def select_small_region(request):
    # city에 맞는 도시 출력하기.
    action = request.GET.get('action')
    districts = list(District.objects.all())
    districts1 = districts[:12]
    districts2 = districts[12:24]
    translation.activate(settings.LANGUAGE_CODE)
    number1 = [i for i in range(1, 13)]
    number2 = [i for i in range(13, 25)]
    return render(request, 'select_small_region.html', {'number1': number1 , 'number2':number2 , 'districts1': districts1, 'districts2': districts2})


def select_bus_stop(request):
    translation.activate(settings.LANGUAGE_CODE)
    district = District.objects.get(name='Gangnam-gu')
    bus_stops = district.bus_stops.all()
    bus_dict_chunks = chunk_and_number(bus_stops, 10)
    return render(request, 'select_bus_stop.html', {'bus_dict': bus_dict_chunks})

def bus_info(request):
    translation.activate(settings.LANGUAGE_CODE)
    # BusStop 인스턴스 가져오기
    bus_name = request.GET.get('bus_name')
    bus_stop = BusStop.objects.get(name=bus_name)

    # 해당 BusStop 인스턴스에 연결된 모든 TimeTable 인스턴스를 가져오기
    timetables = TimeTable.objects.filter(arrival_bus_stop=bus_stop)
    if not timetables:
        return Response({'error': 'No timetables'}, status=404)

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

    # 웹소켓을 통해 버스 정보를 보냅니다.
    send_to_websocket('javaScript_group', 'bus_info', json.dumps(bus_info))

    return render(request, 'bus_info.html', bus_info)

def bus_info_schedule(request):
    translation.activate(settings.LANGUAGE_CODE)
    # BusStop 인스턴스 가져오기
    bus_name = request.GET.get('bus_name')
    bus_stop = BusStop.objects.get(name=bus_name)

    # 해당 BusStop 인스턴스에 연결된 모든 TimeTable 인스턴스를 가져옵니다.
    now = datetime.now().time()
    timetables = TimeTable.objects.filter(arrival_bus_stop=bus_stop, time__gte=now).order_by('time')

    # timetables를 10개씩 분할하면서 time 필드만 가져오고 시간,분만 표현
    chunks = [timetable.time.strftime("%H:%M") for timetable in timetables]

    # 각 분할된 리스트의 길이가 10이 아닐 경우, 리스트에 빈 문자열(" ")을 추가
    while len(chunks) % 10 != 0:
        chunks.append(" ")

    chunked_timetables = [chunks[i:i + 10] for i in range(0, len(chunks), 10)]

    date = datetime.now().strftime("%Y-%m-%d")
    bus_number = timetables.first().bus.number

    return render(request, 'select_bus_schedule.html', {
        'bus_number': bus_number,
        'date': date,
        'chunks': chunked_timetables
    })

def number_of_people(request):
    translation.activate(settings.LANGUAGE_CODE)

    bus_number = request.GET.get('bus_number')
    bus_name = request.GET.get('bus_name')
    bus = Bus.objects.get(number=bus_number)
    bus_stop = BusStop.objects.get(name=bus_name)

    # 해당 BusStop 인스턴스에 연결된 모든 TimeTable 인스턴스를 가져옵니다.
    now = datetime.now().time()
    timetables = TimeTable.objects.filter(arrival_bus_stop=bus_stop, time__gte=now).order_by('time')

    # timetables를 10개씩 분할하면서 time 필드만 가져오고 시간,분만 표현, 각 분할된 리스트의 길이가 10이 아닐 경우, 리스트에 빈 문자열(" ")을 추가
    chunks = [[item.time.strftime("%H:%M") for item in timetables[i:i + 10]] for i in range(0, len(timetables), 10)]
    for chunk in chunks:
        while len(chunk) < 10:
            chunk.append(" ")

    first_timetable_time = timetables.first().time.strftime("%H:%M")

    adult_fare = bus.fare
    student_fare = int(adult_fare * 0.8)
    child_fare = int(adult_fare * 0.5)
    return render(request, 'number_people.html',
                  {'time': first_timetable_time,
                   'date': datetime.now().strftime("%Y-%m-%d"),'adult_fare': adult_fare,
                   'student_fare': student_fare, 'child_fare': child_fare, 'bus_number': bus_number})

def purchase_info(request):
    translation.activate(settings.LANGUAGE_CODE)
    # BusStop 인스턴스 가져오기
    bus_name = request.GET.get('bus_name')
    bus_stop = BusStop.objects.get(name=bus_name)

    # 해당 BusStop 인스턴스에 연결된 모든 TimeTable 인스턴스를 가져옵니다.
    now = datetime.now().time()
    timetables = TimeTable.objects.filter(arrival_bus_stop=bus_stop, time__gte=now).order_by('time')

    bus_number = timetables.bus.number

    common_count = int(request.GET.get('common_count'))
    student_count = int(request.GET.get('student_count'))
    child_count = int(request.GET.get('child_count'))

    total_fare = calculate_fares(timetables.first().bus, common_count, student_count, child_count)

    return render(request, 'purchase_info.html', {
    'bus_number': bus_number, 'total_fare': total_fare, 'common_count': common_count, 'student_count': student_count,
    'child_count': child_count,'timetables': timetables, 'date': datetime.now().strftime("%Y-%m-%d"),
    'first_time': timetables.first().time.strftime("%H:%M"), 'departure': bus_stop.name,
    'total_count': common_count + student_count + child_count})

def chunk_and_number(objects, chunk_size=10):
    """
    주어진 객체 리스트를 chunk_size 크기로 분할하고, 각 분할에 번호를 매깁니다.
    """
    numbered_objects = list(enumerate(objects, start=1))
    chunks = [dict(numbered_objects[i:i + chunk_size]) for i in range(0, len(numbered_objects), chunk_size)]
    return chunks

def send_to_websocket(group_name, message_type, message):
    """
    WebSocket 그룹으로 메시지 보내기
    """
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'javaScript_message',
            'message_type': message_type,
            'message': message
        }
    )

def calculate_fares(bus, common_count, student_count, child_count):
    adult_fare = bus.fare
    student_fare = int(adult_fare * 0.8)
    child_fare = int(adult_fare * 0.5)
    total_fare = (common_count * adult_fare) + (student_count * student_fare) + (child_count * child_fare)
    return total_fare