from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate

from .forms import UserCreationForm
from App_Board.models import Category

def signup_view(request):
    all_category = Category.objects.all()
    context = {'all_category' : all_category}

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        context['form'] = form
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            """ 
            authenticate(request=None, **credentials)
            : User 인증 함수. 자격 증명이 유효한 경우 User 객체를, 그렇지 않은 경우 None을 반환 
            """
            user = authenticate(email=email, password=password)
            """ 
            authenticate()에 의해 생성된 user객체를 로그인 하기 위해서는 장고의 login()함수를 사용한다. 
            이 함수는 user의 id와 pw를 장고의 session에 저장한다.
            """ 
            login(request, user)
            return redirect("App_Board:main_page")
    else:
        context['form'] = UserCreationForm()

    return render(request, 'signup.html', context)


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
