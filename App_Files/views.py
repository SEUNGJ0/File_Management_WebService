from django.shortcuts import render, redirect
from django.views import generic
from .models import *
from App_Board.models import *
import zipfile

# Create your views here.
class HomeListView(generic.ListView):
    queryset = Board.objects.filter(category=3)
    context_object_name = 'files' 
    paginate_by = 5
    template_name = 'Files_list.html'

def FileManagerView(request):
    print(request.POST)
    if request.method == "POST":
        if request.POST['action'] == "sum":
            return render(request, 'Files_list.html')

        elif request.POST['action'] == "download":
            boards = request.POST.getlist('board_id')
            return redirect('App_Board:file_download', args=boards)
            
        elif request.POST['action'] == "delete":
            return render(request, 'Files_list.html')


    return render(request, 'Files_list.html')
