from django.shortcuts import render
from django.utils import translation
from django.utils.translation import gettext as _

def index(request):
    return render(request, 'initial_screen.html')

def change_language_mode(request, upperLevel, lowerLevel):
    # 후에 templates 렌더링과 데이터 넣어주기.
    translation.activate(lowerLevel)
    camera_message = _("Please choose a language by looking at the camera.")
    request.session['language_code'] = lowerLevel
    return render(request, 'language_request.html', {'camera_message': camera_message})