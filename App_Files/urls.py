from django.urls import path
from .views import *

app_name='App_Files'

urlpatterns = [
    path('home', File_HomeView, name='File_Home'),
    path('<s_category_slug>/', File_in_CategoryView, name='File_in_category'),
    path('manager', FileManagerView, name = 'FileManager'),
    path('오류-로그/<int:pk>', ErrorLogDetailView.as_view() ,name = "ErrorLogDetail" )
]