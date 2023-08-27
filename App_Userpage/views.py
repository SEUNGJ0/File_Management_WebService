from App_Auth.models import User
from App_Auth.forms import UserChangeForm

from App_Board.models import Category
from App_Board.views.render_views import pagination

from django.contrib.auth.hashers import check_password
from django.contrib import messages, auth
from django.shortcuts import render, redirect, get_object_or_404

def userpage_render_view(request, user_id):
    all_category = Category.objects.all()
    user = User.objects.get(id = user_id)
    page = request.GET.get('page', '1')
    page_obj = pagination(page, user.board_set.all(), 5)
    
    context = {
        'user' : user,
        'all_category' : all_category,
        'boards' : page_obj, 
        'page_obj' : page_obj
    }
    return render(request, "Userpage.html", context)

def user_update_view(request, user_id):
    all_category = Category.objects.all()
    user = get_object_or_404(User, id = user_id)
    if request.user == user:
        if request.method == 'POST':
            form = UserChangeForm(request.POST, instance=user)
            if form.is_valid():
                user_form = form.save(commit=False)
                user_form.save()
                messages.success(request, "수정이 완료되었습니다.")
                return redirect('App_Userpage:userpage_render_view', user.id)
        else:
            form = UserChangeForm(instance=user)
        context = {
            'form' : form,            
            'user' : user,
            'all_category' : all_category
        }
        return render(request, "User_update.html", context)
    else:
        return redirect('App_Board:main_page')
    
def password_update_view(request, user_id):
    # 모든 카테고리 객체를 가져옴
    all_category = Category.objects.all()
    # 사용자 객체를 가져오거나 찾지 못하면 404를 반환
    user = get_object_or_404(User, id = user_id)

    context = {
        'all_category' : all_category,
        'user' : user,
        }
    
    if request.method == 'POST':
        # 옵션 필드에 대해 get() 사용
        origin_password = request.POST.get('origin_password', None) # 기본값 : None

        # 기존 비밀번호가 일치하는 경우
        if check_password(origin_password, user.password):
            new_password = request.POST['new_password']
            password_check = request.POST['password_check']

            if len(new_password) and new_password == password_check :
                # 사용자의 비밀번호를 업데이트하고 로그인
                user.set_password(new_password)
                user.save()
                auth.login(request, user)
                messages.success(request, "비밀번호 수정이 완료되었습니다.")
                return redirect('App_Userpage:userpage_render_view', user.id)
            else:
                messages.error(request, "비밀번호가 일치하지 않습니다.")
        else:
            messages.error(request, "기존의 비밀번호를 다시 확인해주세요.")
        return render(request, 'password_update.html', context)
    else:
        return render(request, 'password_update.html', context)


def user_delete_view(request):
    return

