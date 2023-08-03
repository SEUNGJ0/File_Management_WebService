from django.urls import path
from . import Auth_views
app_name = "App_Auth"

urlpatterns = [
    path('login/', Auth_views.login_view, name='login'),
    path('logout/', Auth_views.logout_view, name='logout'),
    path('sign/', Auth_views.signup_view, name='signup'),
    # path('password_change/<user_id>', Auth_views.password_change_view, name = 'password_change_view')
]