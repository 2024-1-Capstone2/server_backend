from django.urls import path

from . import views

urlpatterns = [

    # rest
    path('requestSelectRegion', views.request_select_region, name='request_select_region'),
    path('requestSelectSmallRegion', views.request_select_small_region, name='request_select_small_region'),
    path('requestBusScheduleInfo', views.request_bus_schedule_info, name='request_bus_schedule_info'),
    path('requestSelectBusStop', views.request_select_bus_stop, name='request_select_bus_stop'),
    path('requestBusInfo', views.request_bus_info, name='request_bus_info'),
    path('requestBusInfoSchedule', views.request_bus_info_schedule, name='request_bus_info_schedule'),

    # render
    path('selectRegion', views.select_region, name='select_region'),
    path('selectSmallRegion', views.select_small_region, name='select_small_region'),
    path('busScheduleInfo', views.bus_schedule_info, name='bus_schedule_info'),
    path('selectBusStop', views.select_bus_stop, name='select_bus_stop'),
    path('busInfo', views.bus_info, name='bus_info'),
    path('busInfoSchedule', views.bus_info_schedule, name='bus_info_schedule'),


    path('1', views.index1),
    path('temp', views.index),
]