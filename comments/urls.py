from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.CommentView.as_view()),
    path('<int:cmt_id>/', views.NestedComments.as_view()),

]
