from App_Auth.models import User, EmailVerification
from App_Auth.forms import UserChangeForm

from App_Board.models import Category, Board
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
    
def password_change_view(request, user_id):
    all_category = Category.objects.all()
    user = get_object_or_404(User, id = user_id)
    # 이메일 인증 후 페스워드 변경시 필요 코드
    try:
        user_email_verify = EmailVerification.objects.get(user = user)
        user_is_verificate = user_email_verify.is_verificate
        
    except:
        user_is_verificate = False

    context = {
        'all_category' : all_category,
        'user' : user,
        'user_is_verificate' : user_is_verificate
        }
    
    if request.method == 'POST':
        try:
            origin_password = request.POST['origin_password']
        except:
            origin_password = None

        if check_password(origin_password, user.password) or user_is_verificate:
            new_password = request.POST['new_password']
            password_check = request.POST['password_check']
            if len(new_password) and new_password == password_check :
                user.set_password(new_password)
                user.save()
                auth.login(request, user)
                # user_email_verify.is_verificate = False
                # user_email_verify.save()

                messages.success(request, "비밀번호 수정이 완료되었습니다.")
                return redirect('App_Userpage:userpage_render_view', user.id)
            else:
                messages.error(request, "비밀번호가 일치하지 않습니다.")
        else:
            messages.error(request, "기존의 비밀번호를 다시 확인해주세요.")
        return render(request, 'password_change.html', context)
    else:
        return render(request, 'password_change.html', context)


def user_delete_view(request):
    return

