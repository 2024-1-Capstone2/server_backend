from django.urls import path

from . import views

urlpatterns = [
    path('request_ticket', views.request_ticket, name='request_ticket'),
    path('ask_buy_ticket', views.ask_buy_ticket, name='ask_buy_ticket'),
    path('', views.index, name='index'),
    path('new', views.new, name='new'),
]