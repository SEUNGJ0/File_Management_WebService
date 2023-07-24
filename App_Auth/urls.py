from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *
app_name = "App_Auth"

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('sign/', signup_view, name='signup'),
]