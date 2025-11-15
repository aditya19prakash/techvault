from django.urls import path, include
from aiservice import views

urlpatterns = [
    path('', views.ask_ques),
]
