from django.urls import path
from .views import userpage_render_view, user_update_view, password_update_view
app_name='App_Userpage'

urlpatterns = [
    # base_views.py
    path('detali/', userpage_render_view, name = 'userpage_render_view'),
    path('update/', user_update_view, name = 'user_update_view'),
    path('update/<user_id>/password/<user_token>', password_update_view, name = 'password_update_view'),

]

