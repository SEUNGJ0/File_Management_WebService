from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from App_Files.models import Integrated_Files, File_Category, ErrorLog
from App_Files.FileFunc import File_Manager
from App_Board.models import *
from App_Board.views.render_views import pagination

import datetime
import os

all_category = Category.objects.all()

@login_required(login_url='App_Auth:login')
def File_HomeView(request):
    all_file_category = File_Category.objects.all()
    return render(request, "Files_Home.html", {'all_file_category':all_file_category, 'all_category':all_category})

@login_required(login_url='App_Auth:login')
def File_in_CategoryView(request, File_Category_slug = None):
    if request.user.company != "admin" :
        return redirect('App_Board:post_all')
    
    all_file_category = File_Category.objects.all()
    errorlogs = ErrorLog.objects.all()

    if File_Category_slug:
        select_category = get_object_or_404(File_Category, slug=File_Category_slug)
        all_file = Integrated_Files.objects.filter(file_category=select_category)
        page = request.GET.get('page', '1')
        page_obj = pagination(page, all_file, 5)

    else:
        select_category = None
        all_file = Integrated_Files.objects.all()

    context = {
        'select_category' : select_category, 
        'all_file_category' : all_file_category, 
        'all_file' : page_obj, 
        'all_category':all_category, 
        'errorlogs':errorlogs, 
        'request':request,
        'page_obj' : page_obj
    }
    template_name = {
        "취합-파일" : 'Files_List.html',
        "통합-파일" : 'Files_Sum.html',
        "오류-로그" : 'Files_Error.html'
    }
    return render(request, template_name[File_Category_slug], context)


def FileManagerView(request, cate_id):
    if request.method == "POST":
        select_category = File_Category.objects.get(id=cate_id)
        cate_slug = select_category.slug
        all_file = request.POST.getlist('file_id')
        errors = request.POST.getlist('errorlog_id')

        action = request.POST.get('action')

        if action == "reload": # 첨부파일 파일 불러오기
            return handle_reload(request, cate_slug)

        elif action == "sum": # 자료 통합
            return handle_sum(request, cate_slug, all_file)

        elif action == "download": # 자료 다운로드
            return handle_download(request, cate_slug, all_file)

        elif action == "delete": # 자료 삭제
            return handle_delete(request, cate_slug, all_file, errors)

    return render(request, 'all_file_List.html')

def ErrorLogDetailView(request, error_id):
    errorlogs = get_object_or_404(ErrorLog, id = error_id)
    context = {
        'all_category':all_category,
        'errorlogs': errorlogs,
    }
    return render(request, "Files_ErrorDetail.html", context)


# 자료 취합 게시판에서 첨부된 파일들을 불러와서 새로운 파일의 경우 해당 앱의 all_file 모델에 추가하여 저장한다.
def handle_reload(request, cate_slug):
    posts = Board.objects.filter(category_id=3)
    count = 0
    for post in posts:
        files = Files.objects.filter(post = post)
        for file in files:
            if Integrated_Files.objects.filter(file=file): # all_file 모델에 존재하는 인스턴스인지 확인
                break
            else: # 새로운 인스턴스인 경우
                path_re = file.get_filepath()
                file_path = os.path.join(settings.MEDIA_ROOT, path_re)
                File_Manager.CopyAndMove(file_path)
                count += 1
                # file = f"file/관리/취합 파일/{file.get_filename()}"
                Integrated_Files.objects.create(
                    post=post,
                    file_category=File_Category.objects.get(id=1),
                    file=file
                )
    if count:
        output_message = f'{count}개의 파일을 불러왔습니다.'
    else:
        output_message = '파일을 전부 불러왔습니다.'
    messages.success(request, output_message)
    return redirect("App_Files:File_in_category", cate_slug)

def handle_sum(request, cate_slug, all_file):
    if not all_file:
        messages.error(request, "파일을 선택해주세요.")
        return redirect("App_Files:File_in_category", cate_slug)

    file_list = [Integrated_Files.objects.get(id=int(id)).get_filename() for id in all_file]
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
        Integrated_Files.objects.create(
            post=None,
            file_category=File_Category.objects.get(id=3),
            file=None,
            integrated_file = file_path
        )
        return redirect("App_Files:File_in_category", cate_slug)

def handle_download(request, cate_slug, all_file):
    if not all_file:
        messages.error(request, "파일을 선택해주세요.")
        return redirect("App_Files:File_in_category", cate_slug)

    file_list = [str(Integrated_Files.objects.get(id=int(id)).get_filename()) for id in all_file]
    print(file_list)
    File_Manager.ZipDownload(file_list)
    return redirect("App_Board:file_download", file_id=0)

def handle_delete(request, cate_slug, all_file, errors):
    if not all_file:
        if not errors:
            messages.error(request, "파일을 선택해주세요.")
            return redirect("App_Files:File_in_category", cate_slug)
        elif errors:
            for id in errors:
                error = ErrorLog.objects.get(id=int(id))
                error.delete()
                messages.success(request, "파일 삭제를 성공했습니다.")
            return redirect("App_Files:File_in_category", cate_slug)

    for id in all_file:
        file = Integrated_Files.objects.get(id=int(id))
        file.delete()
        try:
            if file.File_Category.name == "취합 파일":
                path_del = os.path.join(settings.MEDIA_ROOT, f'file/관리/취합 파일/{file.get_filename()}')
            elif file.File_Category.name == "통합 파일":
                path_del = os.path.join(settings.MEDIA_ROOT, f'file/관리/통합 파일/{file.get_filename()}')
            os.remove(path_del)
            messages.success(request, "파일 삭제를 성공했습니다.")
        except:
            messages.success(request, "파일 삭제를 성공했습니다.")

    return redirect("App_Files:File_in_category", cate_slug)
