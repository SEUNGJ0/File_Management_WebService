from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label='비밀번호', widget=forms.PasswordInput)
    password_check = forms.CharField(label='비밀번호 확인', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'name', 'phone_number', 'company')

    # clean_<Field_name>() : 해당 필드의 유효성을 체크하는 메소드
    # 유효성 검사

    # 입력한 비밀번호의 일치 확인
    def clean_password_check(self):
        # self.cleaned_data['데이터'] : 데이트를 획득
        password = self.cleaned_data.get("password")
        password_check = self.cleaned_data.get("password_check")
        if password and password_check and password != password_check:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다!")
        return password_check

    # 입력한 이메일의 중복존재 여부 확인
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # 이메일 검증시 대소문자를 구별하지 않는다.
        if User.objects.filter(email__iexact = email).exists():
            raise forms.ValidationError('이미 존재하는 이메일입니다. 다시 확인해주세요.')
        return email

    # 비밀번호를 해쉬 암호 방식으로 저장하고, 기존의 save 메소드를 호출하여 사용자를 지정한다.
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    
    class Meta:
        model = User
        fields = ('password', 'name', 'phone_number', 'is_active', 'is_admin')

    def clean_password(self):
        return self.initial["password"]
        
