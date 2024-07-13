from django.shortcuts import render
from django.utils import translation
from django.conf import settings
from busInfo.models import City, District, BusStop, TimeTable, Bus
from datetime import datetime

import warnings
warnings.filterwarnings('ignore')

def index(request):
    return render(request, 'bus_boarding/bus_schedule_request.html')

def bus_info_image(request, upperLevel, lowerLevel):
    return render(request, 'bus_info_image.html')

def crawl_and_save_bus_info(request):
    return render(request, 'bus_info.html')


def bus_boarding(request):
    translation.activate(settings.LANGUAGE_CODE)
    return render(request, 'bus_boarding/bus_boarding_request.html')

def bus_gate(request):
    translation.activate(settings.LANGUAGE_CODE)
    return render(request, 'bus_boarding/bus_guide.html')

# schedule

def bus_schedule_request(request):
    translation.activate(settings.LANGUAGE_CODE)
    return render(request, 'schedule/bus_schedule_request.html')


def bus_schedule(request):
    translation.activate(settings.LANGUAGE_CODE)
    bus_stop_name = request.GET.get('bus_stop_name')
    timetables = get_upcoming_timetables(bus_stop_name)

    chunks = format_timetables(timetables)
    date = datetime.now().strftime("%Y-%m-%d")
    bus_number = timetables.first().bus.number

    context = {
        'bus_number': bus_number,
        'date': date,
        'chunks': chunks,
        'number1': list(range(1, 11)),
        'number2': list(range(11, 21)),
        'number3': list(range(21, 31))
    }

    return render(request, 'schedule/bus_schedule.html', context)

def get_upcoming_timetables(bus_stop_name):
    now = datetime.now().time()
    return TimeTable.objects.filter(
        arrival_bus_stop__name=bus_stop_name,
        time__gte=now
    ).order_by('time')


def format_timetables(timetables):
    formatted = [t.time.strftime("%H:%M") for t in timetables]
    chunks = [formatted[i:i + 10] for i in range(0, len(formatted), 10)]
    return [chunk + [" "] * (10 - len(chunk)) for chunk in chunks]