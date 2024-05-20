from django.shortcuts import render
from django.utils import translation
from django.utils.translation import gettext as _

def index(request):
    language_code = request.session.get('language_code')
    translation.activate(language_code)
    camera_message = _("Please choose a language by looking at the camera.")
    return render(request, 'language.html', {'camera_message': camera_message})
def change_language_mode(request, upperLevel, lowerLevel):
    # 후에 templates 렌더링과 데이터 넣어주기.
    translation.activate(lowerLevel)
    camera_message = _("Please choose a language by looking at the camera.")
    request.session['language_code'] = lowerLevel
    return render(request, 'language_request.html', {'camera_message': camera_message})