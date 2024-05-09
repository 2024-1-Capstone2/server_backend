from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hand_tracking', views.hand_tracking, name='hand_tracking'),
]