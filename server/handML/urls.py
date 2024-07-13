from django.urls import path

from . import views

urlpatterns = [
    path('hand_tracking', views.hand_tracking, name='hand_tracking'),
    path('api/hand-data', views.hand_data, name='hand_data'),
]