from django.urls import path
from .views import edit_views, file_views, render_views

app_name='App_Board'

urlpatterns = [
    # base_views.py
    path('', render_views.mainpage_render_view, name = 'main_page'),
    path('<category_slug>/', render_views.board_render_view, name = 'board_render_view'),
    path('post/<int:board_id>', render_views.post_render_view, name = 'post_render_view'),

    # edit_views.py
    path('create/<category_id>', edit_views.post_create_view, name = 'post_create_view'),
    path('update/<int:board_id>', edit_views.post_update_view, name = 'post_update_view'),
    path('post/<int:pk>/delete', edit_views.post_delete.as_view(), name = 'post_delete_view'),

    # file_views.py
    path('post/download/<int:file_id>', file_views.file_download, name='file_download'),    
]

