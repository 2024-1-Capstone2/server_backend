from django.shortcuts import render
from django.utils import translation
from django.utils.translation import gettext as _

def index(request):
    print("call")
    return render(request, 'initial_screen.html')