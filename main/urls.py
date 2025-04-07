from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = "Home"),
    path('quiz/', views.quiz_view, name = "Quiz" ),
]
