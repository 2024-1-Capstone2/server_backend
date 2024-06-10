from django.urls import path

from . import views

urlpatterns = [
    #rest
    path('requestQuestion', views.request_question, name='request_question'),
    path('requestReQuestion', views.request_re_question, name='request_re_question'),
    path('requestInformationDesk', views.request_information_desk, name='request_information_desk'),
    path('requestInitialScreen', views.request_initial_screen, name='request_initial_screen'),

    #render
    path('question', views.question, name='question'),
    path('reQuestion', views.re_question, name='re_question'),
    path('informationDesk', views.information_desk, name='information_desk'),
    path('', views.initial_screen, name='initial_screen'),
]