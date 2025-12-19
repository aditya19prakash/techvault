from django.urls import path
from users import views

urlpatterns = [
    path('', views.users_view, name='api_view'),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logut"),
    path("refresh/", views.refresh_token, name="token_refresh"),
    path("check_redis_connection/",views.redis_hard_test),
]
