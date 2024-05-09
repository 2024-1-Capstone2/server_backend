# -*- coding: utf-8 -*-
from django.utils import translation
from django.utils.translation import gettext as _

def change_language_code(code):
    print(code)
    if code == '1':
        translation.activate('ko')
    elif code == '2':
        translation.activate('en')

    print("test1")
    temp_dict = {'message': _("Welcome to my site.")}
    print("test2")

    return temp_dict