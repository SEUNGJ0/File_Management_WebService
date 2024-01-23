from django.urls import path
from .Userpage_views import userpage_render_view, user_update_view, password_update_view, EmailVerificationView
app_name='App_Userpage'

urlpatterns = [
    path('detail/', userpage_render_view, name = 'userpage_render_view'),
    path('update/', user_update_view, name = 'user_update_view'),
    path('update/password/emailcheck', EmailVerificationView.as_view(), name='email_check'),
    path('update/<user_id>/password/<user_token>', password_update_view, name = 'password_update_view'),

]

