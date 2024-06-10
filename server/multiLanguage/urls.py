from django.urls import path

from . import views

urlpatterns = [
    # rest
    path('requestChoiceLanguage', views.request_choice_language, name='request_choice_language'),
    # render
    path('choiceLanguage', views.choice_language, name='choice_language'),
]