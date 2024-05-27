from django.urls import path

from . import views

urlpatterns = [
    # rest
    path('request_ticket', views.request_ticket, name='request_ticket'),
    path('ask_buy_new_ticket', views.ask_buy_new_ticket, name='ask_buy_new_ticket'),
    path('refund_impossible', views.refund_impossible, name='refund_impossible'),
    # path('ask_buy_ticket', views.ask_buy_ticket, name='ask_buy_ticket'),
    # render page
    path('', views.index, name='index'),
    path('new', views.new, name='new'),
    path('impossible', views.impossible, name='impossible'),
]