from django.urls import path
from .views.api import rest_views
from .views.ssr import ssr_views

urlpatterns = [
    #rest
    path('api/question', rest_views.request_question, name='request_question'),
    path('api/re-question', rest_views.request_re_question, name='request_re_question'),
    path('api/info-desk', rest_views.request_information_desk, name='request_information_desk'),
    path('api/initial', rest_views.request_initial_screen, name='request_initial_screen'),

    #render
    path('question', ssr_views.question, name='question'),
    path('re-question', ssr_views.re_question, name='re_question'),
    path('info-desk', ssr_views.information_desk, name='information_desk'),
    path('', ssr_views.initial_screen, name='initial_screen'),
]