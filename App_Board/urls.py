from django.urls import path
from .views import *

app_name='App_Board'

urlpatterns = [
    path('', board_home, name = 'post_all'),
    path('<category_slug>/', post_in_category, name = 'post_in_category'),
    path('create/<category_id>', post_create, name = 'post_create'),
    path('post/<int:board_id>', post_detail, name = 'post_detail'),
    path('post/download/<int:board_id>', file_download, name='file_download'),
    path('update/<int:board_id>', post_update, name = 'post_update'),
    path('post/<int:pk>/delete', post_delete.as_view(), name = 'post_delete'),

]

