from unicodedata import category
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from App_Board.models import *
from .FileFunc import File_Manager
from django.conf import settings
import datetime
import os

categories = Category.objects.all()
date = datetime.datetime.now().strftime("%m월%d일%H시%M분")

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
    
    if  s_category_slug == "취합-파일":
        return render(request, 'Files_List.html', context)
    elif s_category_slug == "통합-파일":
        return render(request, 'Files_Sum.html', context)
    else:
        return render(request, 'Files_List.html', context)

def FileManagerView(request):
    if request.method == "POST":
        files = request.POST.getlist('file_id')
        # "불러오기" 버튼을 눌렀을 떄
        if request.POST['action'] == "reload":
            # "자료 취합" 내의 게시글을 모두 가져온다.
            posts = Board.objects.filter(category_id=3)
            for post in posts:
                # 해당 게시글이 이미 포함되있는 경우 페스한다.
                if Files.objects.filter(board_id=post.id):
                    break
                else: 
                    # 해당 게시글이 없는 경우 새로 만들고, 파일을 "취합 파일"로 옮긴다.
                    path = str(post.file)
                    file_path = os.path.join(settings.MEDIA_ROOT, path)
                    File_Manager.CopyAndMove(file_path)

                    file = f"file/자료 취합/취합 파일/{post.get_filename()}"
                    Files.objects.create(
                        board = post,
                        s_category = S_Category.objects.get(id=1),
                        file = file 
                        )
            return redirect("App_Files:File_in_category", "취합-파일")
        
        elif request.POST['action'] == "sum":
            file_list = []
            for id in files:
                file = Files.objects.get(id=int(id))
                file_name = file.get_filename()
                file_list.append(file_name)
            File_Manager.Absorption(file_list=file_list)
            # 통합된 파일을 Files에 추가
            file_path = f"file/자료 취합/통합 파일/통합 파일_{date}.xlsx"
            Files.objects.create(
                        board = None,
                        s_category = S_Category.objects.get(id=3),
                        file = file_path
                        )
            return redirect("App_Files:File_in_category", "통합-파일")

        elif request.POST['action'] == "download":
            return redirect('App_Board:file_download', args=files)

        elif request.POST['action'] == "delete":
            for id in files:    
                file = Files.objects.get(id=int(id))
                path = os.getcwd()+f'/media/file/자료 취합/취합 파일/{file.get_filename()}'
                file_path = os.path.join(settings.MEDIA_ROOT, path)
                os.remove(path)
                file.delete()
            return redirect("App_Files:File_in_category", "취합-파일")

    return render(request, 'Files_List.html')