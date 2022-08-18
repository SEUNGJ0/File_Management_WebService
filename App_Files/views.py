from unicodedata import category
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from App_Board.models import *
from .FileFunc import File_Manager
from django.conf import settings
import os

categories = Category.objects.all()

def File_HomeView(request):
    s_categories = S_Category.objects.all()
    return render(request, "Files_Home.html", {'s_categories':s_categories, 'categories':categories})
    
def File_in_CategoryView(request, s_category_slug = None):
    current_category = None
    s_categories = S_Category.objects.all()
    files = Files.objects.all()
    if s_category_slug:
        current_category = get_object_or_404(S_Category, slug=s_category_slug)
        files = files.filter(s_category=current_category)
    context = {'current_category' : current_category, 's_categories' : s_categories, 'files' : files, 'categories':categories}
    
    return render(request, 'Files_list.html', context)

def FileManagerView(request):
    if request.method == "POST":
        files = request.POST.getlist('board_id')

        if request.POST['action'] == "reload":
            posts = Board.objects.filter(category_id=3)
            for post in posts:
                if Files.objects.filter(board_id=post.id):
                    break
                else: 
                    Files.objects.create(
                        board = post,
                        s_category = S_Category.objects.get(id=1),
                        file = post.file
                    )             
            return redirect("App_Files:File_in_category", "취합-파일")
            
        elif request.POST['action'] == "sum":
            for board in files:
                board = Board.objects.get(id = board)
                path = str(board.file)
                file_path = os.path.join(settings.MEDIA_ROOT, path)
                File_Manager.CopyAndMove(file_path)
    
            return redirect("App_Files:File_in_category", "통합-파일")

        elif request.POST['action'] == "download":
            return redirect('App_Board:file_download', args=files)

        elif request.POST['action'] == "delete":
            return render(request, 'Files_list.html')


    return render(request, 'Files_list.html')

