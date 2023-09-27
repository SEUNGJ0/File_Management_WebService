from django.urls import path
from . import Auth_views, EmailFunc
app_name = "App_Auth"

urlpatterns = [
    path('login/', Auth_views.login_view, name='login'),
    path('logout/', Auth_views.logout_view, name='logout'),
    path('sign/', Auth_views.SignupView.as_view(), name='signup'),
]