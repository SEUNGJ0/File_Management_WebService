from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.views import View

from App_Auth.forms import UserCreationForm
from App_Board.models import Category, User
from config.get_secret import get_secret, input_secret
from App_Auth.Email_views import generate_verification_code, send_email_with_verification_code


class SignupView(View):
    template_name = 'signup.html'

    def get_context(self, email=""):
        all_category = Category.objects.all()
        return {'all_category': all_category, 'email': email}

    def get(self, request):
        context = self.get_context()
        return render(request, self.template_name, context)

    def post(self, request):
        action = request.POST.get('action')
        email = request.POST.get('email')
        context = self.get_context(email=email)
        if action == 'signup':
            form = UserCreationForm(request.POST)
            context['form'] = form
            email_verified = get_secret(email)
            context['email_verified'] = email_verified
            
            # 이메일 인증 상태 확인
            if email_verified == True:
                if form.is_valid():    
                    form.save()
                    email = form.cleaned_data.get('email')
                    password = form.cleaned_data.get('password')  # 비밀번호 필드 이름 수정
                    # authenticate(request=None, **credentials): User 인증 함수
                    user = authenticate(email=email, password=password)
                    # login()함수를 사용한다. 이 함수는 user의 id와 pw를 장고의 session에 저장한다.
                    login(request, user)
                    return redirect("App_Board:main_page")
            else:
                context['error'] = "이메일 인증이 필요합니다."
                return render(request, self.template_name, context)
            
            return render(request, self.template_name, context)
        
        elif action == 'signup_send_code':
            # 이메일 중복 검사
            if User.objects.filter(email__iexact = email).exists():
                context['email'] = ""
                context['error'] = '이미 존재하는 이메일입니다. 다시 확인해주세요.'
                return render(request, self.template_name, context)
            
            # 인증 코드 전송
            else:
                verification_code = generate_verification_code()
                input_secret(email, verification_code)
                send_email_with_verification_code(email=email,verification_code=verification_code, name = None)
                context['info'] = f"해당 {email} 주소로 인증 코드가 전송되었습니다."
                return render(request, self.template_name, context)
        
        elif action == "signup_check_code":
            get_code = get_secret(email)
            input_code = request.POST.get('code')
            print(request.POST)
            # 인증 코드 검증 성공
            if get_code == input_code:
                context['email_verified'] = True
                context['success'] = "이메일 인증에 성공했습니다."
                input_secret(email, True)

                return render(request, self.template_name, context)
            
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
