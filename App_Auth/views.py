from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserCreationForm
from App_Board.models import Category

def signup_view(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect("App_Board:post_all")
    else:
        form = UserCreationForm()
    return render(request, 'sign.html', {'form': form, 'categories':categories})


def login_view(request):
    categories = Category.objects.all()
    if request.method == 'POST' :
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("App_Board:post_all")
        else:
            return render(request, 'login.html', {'error':'이메일 또는 비밀번호가 일치하지 않습니다.','categories':categories})
    else:
        return render(request, 'login.html',{'categories':categories})