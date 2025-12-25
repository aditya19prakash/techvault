from django.urls import path
from users import views

urlpatterns = [
    path('', views.UserView.as_view()),
    path("login/", views.UserLogin.as_view()),
    path("logout/", views.UserLogout.as_view()),
    path("refresh/", views.RefreshTokenView.as_view()),
]
