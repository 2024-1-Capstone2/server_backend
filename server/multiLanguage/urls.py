from django.urls import path

from . import views

urlpatterns = [
    # rest
    path('api/choice', views.request_choice_language, name='request_choice_language'),
    # render
    path('choice', views.choice_language, name='choice_language'),
]