from django.shortcuts import render
import mediapipe as mp
from django.http import HttpResponse

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

server_text = ""


def index(request):
    return HttpResponse("장고 시작")
# 손동작 인식 화면 호출
def hand_tracking(request):
    return render(request, 'hand_tracking.html')