from django.shortcuts import render
from django.conf import settings
from django.utils import translation
from handML.detection import ActionDetector

import warnings
warnings.filterwarnings('ignore')

# 초기화면

def initial_screen(request):
    return render(request, 'screen.html')

def question(request):
    translation.activate(settings.LANGUAGE_CODE)
    detector = ActionDetector()
    detector.action_cleaner()
    return render(request, 'question/question.html')

def re_question(request):
    translation.activate(settings.LANGUAGE_CODE)
    return render(request, 'question/reQuestion.html')

# information desk


def information_desk(request):
    translation.activate(settings.LANGUAGE_CODE)
    return render(request, 'information_desk.html')