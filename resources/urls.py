from django.urls import path
from . import views

urlpatterns = [
    path('', views.resource_view),
    path('<int:id>/', views.resource_view_id),
]
