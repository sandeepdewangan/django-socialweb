from django.urls import path
from django.contrib.auth import views as auth_views
# Import from project
from .import views

urlpatterns = [
    # login view - handling forms by us
    #path('login/', views.user_login, name='login'),
     # login view - handling forms by django auth framework
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LoginView.as_view(), name='logout'),

    path('', views.dashboard, name='dashboard'),
]
