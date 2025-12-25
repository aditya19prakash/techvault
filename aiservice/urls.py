from django.urls import path
from aiservice import views

urlpatterns = [
    path('', views.AskQuesView.as_view()),
]
