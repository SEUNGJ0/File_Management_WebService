from django.shortcuts import render, redirect
from django.views import generic
from .models import *
from App_Board.models import *
from .FileFunc import File_Manager
from django.conf import settings
import shutil
import os

# Create your views here.
class HomeListView(generic.ListView):
    queryset = Board.objects.filter(category=3)
    context_object_name = 'files' 
    paginate_by = 5
    template_name = 'Files_list.html'

def FileManagerView(request):
    if request.method == "POST":
        boards = request.POST.getlist('board_id')
        if request.POST['action'] == "sum":
            print(boards)
            for board in boards:
                print(board)
                board = Board.objects.get(id = board)
                path = str(board.file)
                file_path = os.path.join(settings.MEDIA_ROOT, path)
                dst = os.getcwd()+"/media/file/자료 취합/취합 파일/"
                shutil.copy(file_path, dst)
                
            return redirect("App_Files:HomeList")

        elif request.POST['action'] == "download":
            return redirect('App_Board:file_download', args=boards)

        elif request.POST['action'] == "delete":
            return render(request, 'Files_list.html')


    return render(request, 'Files_list.html')
