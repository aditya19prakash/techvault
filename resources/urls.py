from django.urls import path, include
from resources import views

urlpatterns = [
    path('', views.ResourceView.as_view()),
    path('<int:id>/', views.ResourceViewId.as_view()),
    path("<int:id>/voting/",views.ResourceVoting.as_view()),
    path('<int:id>/comments/', include('comments.urls')),
    path('<int:id>/ask-ai/', include('aiservice.urls')),
    path('techstack/', views.TechstackView.as_view()),
]
