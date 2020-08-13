from django.urls import path

# Import from project
from .import views

urlpatterns = [
    path('login/', views.user_login, name='login'), 
]
