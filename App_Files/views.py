from unicodedata import category
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from App_Board.models import *
from .FileFunc import File_Manager
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import datetime
import os

categories = Category.objects.all()

@login_required(login_url='App_Auth:login')
def File_HomeView(request):
    s_categories = S_Category.objects.all()
    return render(request, "Files_Home.html", {'s_categories':s_categories, 'categories':categories})

@login_required(login_url='App_Auth:login')
def File_in_CategoryView(request, s_category_slug = None):
    if request.user.company != "admin" :
        return redirect('App_Board:post_all')
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

def FileManagerView(request, cate_id):
    if request.method == "POST":
        current_category = S_Category.objects.get(id=cate_id)
        cate_slug = current_category.slug
        files = request.POST.getlist('file_id')
        errors = request.POST.getlist('errorlog_id')
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
                    file = f"file/관리/취합 파일/{post.get_filename()}"
                    Files.objects.create(
                        board = post,
                        s_category = S_Category.objects.get(id=1),
                        file = file 
                        )
            messages.success(request, f'{count}개의 파일을 불러왔습니다.')
            return redirect("App_Files:File_in_category", cate_slug)
#----------- 파일 통합 -----------#
        elif request.POST['action'] == "sum":
    #------- 선택된 파일이 없는 경우 -------#
            if not files:
                messages.error(request, "파일을 선택해주세요.")
                return redirect("App_Files:File_in_category", cate_slug)
    #------- 선택된 파일 통합 -------#
            file_list = []
            for id in files:
                file = Files.objects.get(id=int(id))
                file_name = file.get_filename()
                file_list.append(file_name)
            result = File_Manager.Absorption(file_list=file_list)
            print(result)
    #------- 파일 통합 실패 -------#
            if type(result) == dict :
                date = datetime.datetime.now().strftime("%m월 %d일 %H:%M")
                ErrorLog.objects.create(
                    title = f"{date}_오류 로그",
                    error_message = result
                )
                messages.error(request, '통합 파일 생성에 실패했습니다. 오류 로그를 확인해주세요.')
                return redirect("App_Files:File_in_category", cate_slug)
    #------- 파일 통합 성공 -------#
            elif type(result) == str :
                messages.success(request, '통합 파일이 생성되었습니다.')
                file_path = result
                Files.objects.create(
                            board = None,
                            s_category = S_Category.objects.get(id=3),
                            file = file_path
                            )
                return redirect("App_Files:File_in_category", cate_slug)
#----------- 다운로드 -----------#
        elif request.POST['action'] == "download":
            if not files:
                print(cate_id)
                messages.error(request, "파일을 선택해주세요.")
                return redirect("App_Files:File_in_category", cate_slug)
            file_list = []
            for id in files:
                file = Files.objects.get(id=int(id))
                file_list.append(str(file.get_filename()))
            print(file_list)
            File_Manager.ZipDownload(file_list) # 선택한 파일들의 리스트를 보내줌
            return redirect("App_Board:file_download", board_id=0)
#----------- 삭 제 -----------#
        elif request.POST['action'] == "delete":
    #------- 선택된 파일이 없는 경우 -------#
            if not files:
                if not errors:
                    messages.error(request, "파일을 선택해주세요.")
                    return redirect("App_Files:File_in_category", cate_slug)
                elif errors:
                    for id in errors:
                        error = ErrorLog.objects.get(id=int(id))
                        error.delete()
                        messages.success(request, "파일 삭제를 성공했습니다.")
                        return redirect("App_Files:File_in_category", cate_slug)
    #------- 선택된 파일 삭제 -------#
            for id in files: 
                file = Files.objects.get(id=int(id))
                file.delete()
                try:
                    if file.s_category.name == "취합 파일":
                        path_del = os.getcwd()+f'/media/file/관리/취합 파일/{file.get_filename()}'
                    elif file.s_category.name == "통합 파일":
                        path_del = os.getcwd()+f'/media/file/관리/통합 파일/{file.get_filename()}'
                    file_path = os.path.join(settings.MEDIA_ROOT, path_del)
                    os.remove(file_path)
                    messages.success(request, "파일 삭제를 성공했습니다.")
                except:
                    messages.success(request, "파일 삭제를 성공했습니다.")
            return redirect("App_Files:File_in_category", cate_slug)

    return render(request, 'Files_List.html')

def ErrorLogDetailView(request, error_id):
    errorlogs = get_object_or_404(ErrorLog, id = error_id)
    print(errorlogs.error_message)
    print(type(errorlogs.error_message))

    context = {
        'categories':categories,
        'errorlogs': errorlogs,
    }
    return render(request, "Files_ErrorDetail.html", context)
