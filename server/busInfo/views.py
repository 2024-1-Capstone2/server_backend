from django.shortcuts import render
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import HttpResponse
# from .models import BusInfo
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from time import sleep
# from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver.common.alert import Alert
import warnings
from django.templatetags.static import static
warnings.filterwarnings('ignore')

# Create your views here.
def index(request):
    return HttpResponse("장고 시작")

def bus_info_image(request, upperLevel, lowerLevel):
    return render(request, 'bus_info_image.html')

def crawl_and_save_bus_info(request):
    return render(request, 'bus_info.html')

def request_question(request, upperLevel, lowerLevel):
    channel_layer = get_channel_layer()
    # 현재 모듈
    message = f'busInfo/bus_image/{upperLevel}/{lowerLevel}'
    async_to_sync(channel_layer.group_send)('javaScript_group', {
        'type': 'javaScript.message',
        'message': message
    })
    return HttpResponse("Message sent successfully")