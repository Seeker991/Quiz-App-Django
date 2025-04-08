from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name = "Login"),
    path('home/', views.home, name = "Home"),
    path('quiz/', views.quiz_view, name = "Quiz" ),
]
