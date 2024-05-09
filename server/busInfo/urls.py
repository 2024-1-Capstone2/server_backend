from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('bus/', views.crawl_and_save_bus_info, name='crawl_and_save_bus_info'),
    path('bus_image/', views.bus_info_image, name='bus_info_image'),
]