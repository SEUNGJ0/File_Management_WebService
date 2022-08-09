from django.urls import path

from .views import base_views, edit_views, file_views

app_name='App_Board'

urlpatterns = [
    # base_views.py
    path('', base_views.board_home, name = 'post_all'),
    path('<category_slug>/', base_views.post_in_category, name = 'post_in_category'),
    path('post/<int:board_id>', base_views.post_detail, name = 'post_detail'),

    # edit_views.py
    path('create/<category_id>', edit_views.post_create, name = 'post_create'),
    path('update/<int:board_id>', edit_views.post_update, name = 'post_update'),
    path('post/<int:pk>/delete', edit_views.post_delete.as_view(), name = 'post_delete'),

    # file_views.py
    path('post/download/<int:board_id>', file_views.file_download, name='file_download'),    
]

