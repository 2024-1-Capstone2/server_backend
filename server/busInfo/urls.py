from django.urls import path

from .views.api import rest_views
from .views.ssr import ssr_views

urlpatterns = [

    # crawling
    path('bus/', ssr_views.crawl_and_save_bus_info, name='crawl_and_save_bus_info'),

    # rest
    path('api/scheduleNum', rest_views.request_bus_schedule_request, name='request_bus_schedule_request'),
    path('api/schedule', rest_views.request_bus_schedule, name='request_bus_schedule'),
    path('api/gate', rest_views.request_bus_guide, name='request_bus_guide'),
    path('api/boardingId', rest_views.request_bus_boarding, name='request_bus_boarding'),

    # render
    path('schedule_number', ssr_views.bus_schedule_request, name='bus_schedule_request'),
    path('gate', ssr_views.bus_gate, name='bus_gate'),
    path('schedule', ssr_views.bus_schedule, name='bus_schedule'),
    path('boardingId', ssr_views.bus_boarding, name='bus_boarding'),
]