from django.urls import path
from .views import *

app_name='App_Files'

urlpatterns = [
    path('list', HomeListView.as_view(), name='HomeList'),
    path('manager', FileManagerView, name = 'FileManager')
]

