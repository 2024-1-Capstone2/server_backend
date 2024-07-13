import json
from rest_framework.response import Response
import logging
from django.shortcuts import render
from rest_framework.decorators import api_view
from .detection import ActionDetector

import warnings
warnings.filterwarnings('ignore')

# 손동작 인식 화면 호출
def hand_tracking(request):
    return render(request, 'hand_tracking.html')

# 손동작 인식 데이터 전송
@api_view(['POST'])
def hand_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            timestamp = data[0]['timestamp']
            landmarks = data[0]['landmarks'][0]  # 첫 번째 손에 대한 랜드마크

            detector = ActionDetector()
            action = detector.detect_action(landmarks)
        except:
            return Response(status=400)
    return Response(status=200)