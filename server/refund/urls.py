from django.urls import path

from . import views

urlpatterns = [
    # rest
    path('api/ticket', views.request_ticket, name='request_ticket'),
    path('api/question', views.request_question, name='request_question'),

    # render
    path('ticket', views.ticket, name='ticket'),
    path('question', views.question, name='question'),
]