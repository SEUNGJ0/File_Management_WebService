from App_Auth.forms import UserChangeForm
from App_Auth.models import User
from config.get_secret import get_secret, delete_secret
from App_Board.models import Category
from App_Board.views.render_views import pagination

from django.contrib import messages, auth
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required # 함수형 뷰에서 사용하는 권한 제한


from django.shortcuts import render, redirect

@login_required(login_url='App_Auth:login')
def userpage_render_view(request):
    all_category = Category.objects.all()
    page = request.GET.get('page', '1')
    page_obj = pagination(page, request.user.board_set.all(), 5)
    user_token = default_token_generator.make_token(request.user)
    context = {
        'user' : request.user,
        'all_category' : all_category,
        'boards' : page_obj, 
        'page_obj' : page_obj,
        'user_token' : user_token
    }
    return render(request, "Userpage.html", context)

@login_required(login_url='App_Auth:login')
def user_update_view(request):
    all_category = Category.objects.all()
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            user_form = form.save(commit=False)
            user_form.save()
            messages.success(request, "수정이 완료되었습니다.")
            return redirect('App_Userpage:userpage_render_view')
    else:
        form = UserChangeForm(instance=request.user)
    context = {
        'form' : form,            
        'user' : request.user,
        'all_category' : all_category
    }
    return render(request, "User_update.html", context)

def password_update_view(request, user_id, user_token):
    # 모든 카테고리 객체를 가져옴
    all_category = Category.objects.all()
    user = User.objects.get(id = user_id)
    email_verified = get_secret(user.email)
    context = {
        'all_category' : all_category,
        'user' : user,
        'email' : user.email,
        'user_token':user_token,
        }
    
    if default_token_generator.check_token(user, user_token):
        pass
    else:
        return redirect('App_Board:main_page')

    if request.method == 'POST':
        # 옵션 필드에 대해 get() 사용
        origin_password = request.POST.get('origin_password', None) # 기본값 : None
        is_origin_password_valid = email_verified == True or check_password(origin_password, request.user.password)

        # 기존 비밀번호가 일치하는 경우
        if is_origin_password_valid :
            new_password = request.POST['new_password']
            password_check = request.POST['password_check']

            if len(new_password) and new_password == password_check :
                # 사용자의 비밀번호를 업데이트하고 로그인
                request.user.set_password(new_password)
                request.user.save()
                auth.login(request, request.user)
                delete_secret(request.user.email)
                messages.success(request, "비밀번호 수정이 완료되었습니다.")
                return redirect('App_Userpage:userpage_render_view')
            else:
                messages.error(request, "비밀번호가 일치하지 않습니다.")
        else:
            messages.error(request, "기존의 비밀번호를 다시 확인해주세요.")
        return render(request, 'password_update.html', context)
    else:

        return render(request, 'password_update.html', context)


def user_delete_view(request):
    return

