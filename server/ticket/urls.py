from django.urls import path

from . import views
from .views.api import rest_views
from .views.ssr import ssr_views

urlpatterns = [
    # rest
    path('api/region', rest_views.request_select_region, name='request_select_region'),
    path('api/smallRegion', rest_views.request_select_small_region, name='request_select_small_region'),
    path('api/busStop', rest_views.request_select_bus_stop, name='request_select_bus_stop'),
    path('api/bus', rest_views.request_bus_info, name='request_bus_info'),
    path('api/schedule', rest_views.request_bus_info_schedule, name='request_bus_info_schedule'),
    path('api/cnt', rest_views.request_number_of_people, name='request_number_of_people'),
    path('api/purchase', rest_views.request_purchase_info, name='request_purchase_info'),

    # render
    path('region', ssr_views.select_region, name='select_region'),
    path('small_region', ssr_views.select_small_region, name='select_small_region'),
    path('bus_stop', ssr_views.select_bus_stop, name='select_bus_stop'),
    path('bus', ssr_views.bus_info, name='bus_info'),
    path('schedule', ssr_views.bus_info_schedule, name='bus_info_schedule'),
    path('cnt', ssr_views.number_of_people, name='number_of_people'),
    path('purchase', ssr_views.purchase_info, name='purchase_info'),
]