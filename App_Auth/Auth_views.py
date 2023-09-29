from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.views import View

from App_Auth.forms import UserCreationForm
from App_Board.models import Category, User
from App_Auth.EmailFunc import EmailVerification

class SignupView(View):
    template_name = 'signup.html'

    def get_context(self, email=""):
        return {'all_category': Category.objects.all(), 'email': email}

    def get(self, request):
        return render(request, self.template_name, self.get_context())
    
    def post(self, request):
        action = request.POST.get('action')
        email = request.POST.get('email')
        context = self.get_context(email=email)

        # 이메일 중복 검사
        if User.objects.filter(email__iexact = email).exists():
            context.update(email="", error="이미 존재하는 이메일입니다. 다시 확인해주세요.")
            return render(request, self.template_name, context)

        # 회원 가입
        if action == 'signup' :
            form = UserCreationForm(request.POST)
            email_verified = request.session.get('email_verified')
            context.update(form=form, email_verified=email_verified)
            
            if form.is_valid() and email_verified:
                form.save()
                email = form.cleaned_data.get('email')
                password = form.cleaned_data.get('password')  # 비밀번호 필드 이름 수정
                # authenticate(request=None, **credentials): User 인증 함수
                user = authenticate(email=email, password=password)

                # login()함수를 사용한다. 이 함수는 user의 id와 pw를 장고의 session에 저장한다.
                login(request, user)
                return redirect("App_Board:main_page")
            
            return render(request, self.template_name, context)
        
        # 회원 가입 시 인증 코드 전송
        elif action == 'signup_send_code':
            # 인증 클래스 인스턴스 및 코드 생성
            email_verification = EmailVerification(request, email)
            # 인증 코드 전송
            email_verification.send_code_email(request, context)
            pass
    
        elif action == "signup_check_code":
            code = request.session.get('verification_code')
            # 인증 클래스 인스턴스 생성(인증 코드 유지)
            email_verification = EmailVerification(request, email, code=code)
            # 인증 코드 검증 성공
            if email_verification.verify_code(request):
                context.update(email_verified=True, success="이메일 인증에 성공했습니다.")
                request.session['email_verified'] = True    

            # 인증 코드 검증 실패
            else:
                context['error'] = "인증 코드를 다시 확인해주세요"

        return render(request, self.template_name, context)

def login_view(request):
    all_category = Category.objects.all()
    context = {'all_category' : all_category}

    if request.method == 'POST' :
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return redirect("App_Board:main_page")
        else:
            context['error'] = '이메일 또는 비밀번호가 일치하지 않습니다.'
            return render(request, 'login.html', context)
    else:
        return render(request, 'login.html', context)

def logout_view(request):
    logout(request)
    return redirect('App_Board:main_page')
