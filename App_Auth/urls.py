from django.urls import path
from . import Auth_views, Email_views
app_name = "App_Auth"

urlpatterns = [
    path('login/', Auth_views.login_view, name='login'),
    path('logout/', Auth_views.logout_view, name='logout'),
    path('sign/', Auth_views.SignupView.as_view(), name='signup'),
    path('password/find', Email_views.EmailVerificationView.as_view(), name='email_check'),
    path('send_email/', Email_views.send_email_with_verification_code, name='send_email')
]