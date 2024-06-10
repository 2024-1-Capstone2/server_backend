from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('bus/', views.crawl_and_save_bus_info, name='crawl_and_save_bus_info'),

    # rest
    path('requestBusScheduleRequest', views.request_bus_schedule_request, name='request_bus_schedule_request'),
    path('requestBusGuide', views.request_bus_guide, name='request_bus_guide'),
    path('requestBusSchedule', views.request_bus_schedule, name='request_bus_schedule'),
    path('requestBusBoarding', views.request_bus_boarding, name='request_bus_boarding'),

    # render
    path('busScheduleRequest', views.bus_schedule_request, name='bus_schedule_request'),
    path('busGuide', views.bus_guide, name='bus_guide'),
    path('busSchedule', views.bus_schedule, name='bus_schedule'),
    path('busBoarding', views.bus_boarding, name='bus_boarding'),

    path('temp', views.temp, name='temp'),
    path('temp1', views.temp1, name='temp1'),
]