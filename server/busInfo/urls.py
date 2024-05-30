from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('bus/', views.crawl_and_save_bus_info, name='crawl_and_save_bus_info'),
    path('bus_image/<str:upperLevel>/<str:lowerLevel>', views.bus_info_image, name='bus_info_image'),
    path('<str:upperLevel>/<str:lowerLevel>', views.request_question, name='request_question'),

    # rest
    path('requestQuestion', views.request_question, name='request_question'),
    path('requestReQuestion', views.request_re_question, name='request_re_question'),
    path('requestBusSchedule', views.request_bus_schedule, name='request_bus_schedule'),
    path('requestInformationDesk', views.request_information_desk, name='request_information_desk'),
    path('requestBusGuide', views.request_bus_guide, name='request_bus_guide'),
    # render
    path('question', views.question, name='question'),
    path('reQuestion', views.re_question, name='re_question'),
    path('busSchedule', views.bus_schedule, name='bus_schedule'),
    path('busGuide', views.bus_guide, name='bus_guide'),
    path('informationDesk', views.information_desk, name='information_desk'),

    path('temp', views.temp, name='temp'),
]