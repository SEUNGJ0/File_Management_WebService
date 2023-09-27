from App_Auth.forms import UserChangeForm
from App_Auth.models import User
from App_Auth.EmailFunc import *
from App_Board.models import Category
from App_Board.views.render_views import pagination
from config.get_secret import delete_secret

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, login
from django.contrib.auth.tokens import default_token_generator
# from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required 


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
    all_category = Category.objects.all()
    user = get_object_or_404(User, id=user_id)

    # 토큰 검증
    if not default_token_generator.check_token(user, user_token):
        return redirect('App_Board:main_page')

    if request.method == 'POST':
        origin_password = request.POST.get('origin_password', None)
        new_password = request.POST.get('new_password')
        password_check = request.POST.get('password_check')

        # 기존 비밀번호 검증
        if not user.check_password(origin_password) and request.user.is_authenticated :
            messages.error(request, "기존 비밀번호를 다시 확인해주세요.")
        elif new_password != password_check:
            messages.error(request, "비밀번호가 일치하지 않습니다.")
        elif len(new_password) < 3:
            messages.error(request, "비밀번호가 너무 짧습니다.")
        else:
            # 비밀번호 업데이트
            user.set_password(new_password)
            user.save()
            login(request, user)
            # 세션 유지 및 세션 해시 업데이트
            update_session_auth_hash(request, user)
            messages.success(request, "비밀번호 수정이 완료되었습니다.")
            return redirect('App_Userpage:userpage_render_view')

    context = {
        'all_category' : all_category,
        'user': user,
        'email': user.email,
        'user_token': user_token,
    }

    return render(request, 'password_update.html', context)

class EmailVerificationView(View):
    template_name = 'email_verification.html'

    def get_context(self, email=None):
        return {'all_category': Category.objects.all(), 'email': email}

    def get(self, request):
        return render(request, self.template_name, self.get_context())

    def post(self, request):
        action = request.POST.get('action')
        email = request.POST.get('email')
        context = self.get_context(email=email)
        
        # 이메일 유무 검사
        if User.objects.filter(email__iexact = email).exists():
            user = User.objects.get(email=email)
            email_verification = EmailVerification(email, user = user)
            
        # 입력한 이메일의 회원이 없음
        else:
            context.update(email=False, error='사용자 Email을 다시 입력해주세요.')
            return render(request, self.template_name, context) 

        if action == "send_code":            
            email_verification.send_code_email()
            context['info'] = f"해당 {email} 주소로 인증 코드가 전송되었습니다."

        elif action == "check_code":
            if email_verification.verify_code(request, email):
                user_token = default_token_generator.make_token(user)
                delete_secret(email)
                return redirect('App_Userpage:password_update_view', user.id, user_token)
            else:
                context['error'] = "인증 코드를 다시 확인해주세요"
                
        return render(request, self.template_name, context)


def user_delete_view(request):
    return
