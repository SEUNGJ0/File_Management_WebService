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
    
    context = {
        'current_category' : current_category, 
        's_categories' : s_categories, 
        'files' : files, 
        'categories':categories, 
        'errorlogs':errorlogs, 
        'request':request
    }
    template_name = {
        "취합-파일" : 'Files_List.html',
        "통합-파일" : 'Files_Sum.html',
        "오류-로그" : 'Files_Error.html'
    }
    return render(request, template_name[s_category_slug], context)


def FileManagerView(request, cate_id):
    if request.method == "POST":
        current_category = S_Category.objects.get(id=cate_id)
        cate_slug = current_category.slug
        files = request.POST.getlist('file_id')
        errors = request.POST.getlist('errorlog_id')

        action = request.POST.get('action')

        if action == "reload": # 첨부파일 파일 불러오기
            return handle_reload(request, cate_slug)

        elif action == "sum": # 자료 통합
            return handle_sum(request, cate_slug, files)

        elif action == "download": # 자료 다운로드
            return handle_download(request, cate_slug, files)

        elif action == "delete": # 자료 삭제
            return handle_delete(request, cate_slug, files, errors)

    return render(request, 'Files_List.html')

def ErrorLogDetailView(request, error_id):
    errorlogs = get_object_or_404(ErrorLog, id = error_id)
    context = {
        'categories':categories,
        'errorlogs': errorlogs,
    }
    return render(request, "Files_ErrorDetail.html", context)


# 자료 취합 게시판에서 첨부된 파일들을 불러와서 새로운 파일의 경우 해당 앱의 Files 모델에 추가하여 저장한다.
def handle_reload(request, cate_slug):
    posts = Board.objects.filter(category_id=3)
    count = 0
    for post in posts:
        if Files.objects.filter(board_id=post.id): # Files 모델에 존재하는 인스턴스인지 확인
            break
        else: # 새로운 인스턴스인 경우
            path_re = str(post.file)
            file_path = os.path.join(settings.MEDIA_ROOT, path_re)
            File_Manager.CopyAndMove(file_path)
            count += 1
            file = f"file/관리/취합 파일/{post.get_filename()}"
            Files.objects.create(
                board=post,
                s_category=S_Category.objects.get(id=1),
                file=file
            )

    messages.success(request, f'{count}개의 파일을 불러왔습니다.')
    return redirect("App_Files:File_in_category", cate_slug)

def handle_sum(request, cate_slug, files):
    if not files:
        messages.error(request, "파일을 선택해주세요.")
        return redirect("App_Files:File_in_category", cate_slug)

    file_list = [Files.objects.get(id=int(id)).get_filename() for id in files]
    result = File_Manager.Absorption(file_list=file_list)

    if isinstance(result, dict):
        date = datetime.datetime.now().strftime("%m월 %d일 %H:%M")
        ErrorLog.objects.create(
            title=f"{date}_오류 로그",
            error_message=result
        )
        messages.error(request, '통합 파일 생성에 실패했습니다. 오류 로그를 확인해주세요.')
        return redirect("App_Files:File_in_category", cate_slug)

    elif isinstance(result, str):
        messages.success(request, '통합 파일이 생성되었습니다.')
        file_path = result
        Files.objects.create(
            board=None,
            s_category=S_Category.objects.get(id=3),
            file=file_path
        )
        return redirect("App_Files:File_in_category", cate_slug)

def handle_download(request, cate_slug, files):
    if not files:
        messages.error(request, "파일을 선택해주세요.")
        return redirect("App_Files:File_in_category", cate_slug)

    file_list = [str(Files.objects.get(id=int(id)).get_filename()) for id in files]
    File_Manager.ZipDownload(file_list)
    return redirect("App_Board:file_download", board_id=0)

def handle_delete(request, cate_slug, files, errors):
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

    for id in files:
        file = Files.objects.get(id=int(id))
        file.delete()
        try:
            if file.s_category.name == "취합 파일":
                path_del = os.path.join(settings.MEDIA_ROOT, f'file/관리/취합 파일/{file.get_filename()}')
            elif file.s_category.name == "통합 파일":
                path_del = os.path.join(settings.MEDIA_ROOT, f'file/관리/통합 파일/{file.get_filename()}')
            os.remove(path_del)
            messages.success(request, "파일 삭제를 성공했습니다.")
        except:
            messages.success(request, "파일 삭제를 성공했습니다.")

    return redirect("App_Files:File_in_category", cate_slug)
