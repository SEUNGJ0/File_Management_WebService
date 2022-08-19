from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView
from .models import *
from App_Board.models import *
from .FileFunc import File_Manager
from django.conf import settings
from django.contrib import messages
import datetime
import os

categories = Category.objects.all()
def File_HomeView(request):
    s_categories = S_Category.objects.all()
    return render(request, "Files_Home.html", {'s_categories':s_categories, 'categories':categories})
    
def File_in_CategoryView(request, s_category_slug = None):
    current_category = None
    s_categories = S_Category.objects.all()
    files = Files.objects.all()
    errorlogs = ErrorLog.objects.all()
    if s_category_slug:
        current_category = get_object_or_404(S_Category, slug=s_category_slug)
        files = files.filter(s_category=current_category)
    context = {'current_category' : current_category, 's_categories' : s_categories, 'files' : files, 'categories':categories, 'errorlogs':errorlogs}
    
    if  s_category_slug == "취합-파일":
        return render(request, 'Files_List.html', context)
    elif s_category_slug == "통합-파일":
        return render(request, 'Files_Sum.html', context)
    else:
        return render(request, 'Files_Error.html', context)

def FileManagerView(request):
    if request.method == "POST":
        files = request.POST.getlist('file_id')
#----------- 불러오기 -----------#
        if request.POST['action'] == "reload":
            posts = Board.objects.filter(category_id=3)
            count = 0
            for post in posts:
    #------- 파일 존재 시 페스 -------#
                if Files.objects.filter(board_id=post.id):
                    break
    #------- 파일 모델에 추가 -------#
                else: 
                    path_re = str(post.file)
                    file_path = os.path.join(settings.MEDIA_ROOT, path_re)
                    File_Manager.CopyAndMove(file_path)
                    count += 1
                    file = f"file/자료 취합/취합 파일/{post.get_filename()}"
                    Files.objects.create(
                        board = post,
                        s_category = S_Category.objects.get(id=1),
                        file = file 
                        )
            messages.success(request, f'{count}개의 파일을 불러왔습니다.')
            return redirect("App_Files:File_in_category", "취합-파일")
#----------- 파일 통합 -----------#
        elif request.POST['action'] == "sum":
    #------- 선택된 파일이 없는 경우 -------#
            if not files:
                messages.error(request, "파일을 선택해주세요.")
                return redirect("App_Files:File_in_category", "취합-파일")
    #------- 선택된 파일 통합 -------#
            file_list = []
            for id in files:
                file = Files.objects.get(id=int(id))
                file_name = file.get_filename()
                file_list.append(file_name)
            result = File_Manager.Absorption(file_list=file_list)

    #------- 파일 통합 실패 -------#
            if type(result) == list :
                date = datetime.datetime.now().strftime("%m월 %d일 %H:%M")
                ErrorLog.objects.create(
                    title = f"{date}_오류 로그",
                    error_message = result
                )
                messages.error(request, '통합 파일 생성에 실패했습니다. 오류 로그를 확인해주세요.')
                return redirect("App_Files:File_in_category", "취합-파일")
    #------- 파일 통합 성공 -------#
            elif type(result) == str :
                messages.success(request, '통합 파일이 생성되었습니다.')
                file_path = result
                Files.objects.create(
                            board = None,
                            s_category = S_Category.objects.get(id=3),
                            file = file_path
                            )
                return redirect("App_Files:File_in_category", "통합-파일")

#----------- 다운로드 -----------#
        elif request.POST['action'] == "download":
            return redirect('App_Board:file_download', args=files)


#----------- 삭 제 -----------#
        elif request.POST['action'] == "delete":
    #------- 선택된 파일이 없는 경우 -------#
            if not files:
                messages.error(request, "파일을 선택해주세요.")
                return redirect("App_Files:File_in_category", "취합-파일")
    #------- 선택된 파일 삭제 -------#
            for id in files: 
                file = Files.objects.get(id=int(id))
                file.delete()
                if file.s_category.name == "취합 파일":
                    path_del = os.getcwd()+f'/media/file/자료 취합/취합 파일/{file.get_filename()}'
                elif file.s_category.name == "통합 파일":
                    path_del = os.getcwd()+f'/media/file/자료 취합/통합 파일/{file.get_filename()}'
                file_path = os.path.join(settings.MEDIA_ROOT, path_del)
                os.remove(file_path)
                messages.success(request, "파일 삭제를 성공했습니다.")
            return redirect("App_Files:File_in_category", file.s_category.slug)

    return render(request, 'Files_List.html')

class ErrorLogDetailView(DetailView):
    model = ErrorLog
    context_object_name = "errorlogs"
    template_name = "Files_ErrorDetail.html"

