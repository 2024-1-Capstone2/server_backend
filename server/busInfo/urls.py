from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('bus/', views.crawl_and_save_bus_info, name='crawl_and_save_bus_info'),
    path('bus_image/<str:upperLevel>/<str:lowerLevel>', views.bus_info_image, name='bus_info_image'),
    path('<str:upperLevel>/<str:lowerLevel>', views.request_question, name='request_question'),

    # rest
    path('request_question', views.request_question, name='request_question'),
    path('request_reQuestion', views.request_reQuestion, name='request_reQuestion'),
    # render
    path('question', views.question, name='question'),
    path('reQuestion', views.reQuestion, name='reQuestion'),
]