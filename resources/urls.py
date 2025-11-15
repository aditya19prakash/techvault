from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.resource_view),
    path('<int:id>/', views.resource_view_id),
    path('<int:id>/comments/', include('comments.urls')),
    path('<int:id>/ask-ai/', include('aiservice.urls')),
]
