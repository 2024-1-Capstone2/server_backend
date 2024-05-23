from django.urls import path

from . import views

urlpatterns = [
    path('request_ticket', views.request_ticket, name='request_ticket'),
    path('', views.index, name='index'),
]