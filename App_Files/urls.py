from django.urls import path
from .views import *

app_name='App_Files'

urlpatterns = [
    path('home', File_HomeView, name='File_Home'),
    path('<s_category_slug>/', File_in_CategoryView, name='File_in_category'),
    path('manager', FileManagerView, name = 'FileManager'),
    path('sum', File_HomeView, name='SumList'),
]

'''
def add(request):
    if request.method == 'POST':
        Student.objects.create(
            name = request.POST['name']
        )
        return redirect('home')
    return render(request, 'add.html')
'''