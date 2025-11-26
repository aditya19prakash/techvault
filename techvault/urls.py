from django.contrib import admin
from django.urls import path, include
from django.urls import path
from users import views 
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('users.urls')),
    path('resources/', include('resources.urls')),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logut"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
