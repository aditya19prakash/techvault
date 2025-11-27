from django.contrib import admin
from django.urls import path, include
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('users.urls')),
    path('resources/', include('resources.urls')),
    
]
