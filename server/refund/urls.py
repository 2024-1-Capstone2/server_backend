from django.urls import path

from . import views

urlpatterns = [
    # rest
    path('requestTicket', views.request_ticket, name='request_ticket'),
    path('requestQuestion', views.request_question, name='request_question'),

    # render
    path('', views.ticket, name='ticket'),
    path('question', views.question, name='question'),
]