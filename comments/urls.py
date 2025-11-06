from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.comments),
    path('<int:cmt_id>/', views.nested_comments),

]
