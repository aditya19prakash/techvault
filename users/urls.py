from django.urls import path
from . import views

urlpatterns = [
    path('', views.users_view, name='api_view'),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logut"),
    path("refresh/", views.refresh_token, name="token_refresh"),
]
