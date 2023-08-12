import smtplib, random, string
from email.mime.text import MIMEText
from config.get_secret import get_secret
from django.shortcuts import render, redirect
from django.views import View

from App_Board.models import Category
from App_Auth.models import EmailVerification, User  


def generate_verification_code():
    characters = string.ascii_letters + string.digits  # 알파벳과 숫자를 조합하여 문자셋 생성
    return ''.join(random.choices(characters, k=6))

def save_verification_code(user, email, code):
    try:
        verification = EmailVerification.objects.create(user=user, email=email, verification_code=code)
    except:
        verification = EmailVerification.objects.get(user = user)
        verification.verification_code = code
        verification.save()
    return verification

def send_email_with_verification_code(email, verification_code, name):
    send_email = "kuksj0312@naver.com"
    recv_email = email
    password = get_secret('Naver_Password')

    smtp_server = "smtp.naver.com" 
    smtp_port = 587

    text = f"인증 코드 : {verification_code}"
    msg = MIMEText(text) 
    if name:
        msg['Subject'] =f"{name}님의 이메일 인증코드입니다."
    else:
        msg['Subject'] =f"Django Website에서 보내는 이메일 인증코드입니다."
    msg['From'] = send_email
    msg['To'] = recv_email

    with smtplib.SMTP(smtp_server, smtp_port) as s:
        s.starttls()
        s.login(send_email, password)
        s.sendmail(send_email, recv_email, msg.as_string())

class EmailVerificationView(View):
    template_name = 'email_verification.html'

    def get_context(self, email=None):
        all_category = Category.objects.all()
        return {'all_category': all_category, 'email': email}

    def get(self, request):
        context = self.get_context()
        return render(request, self.template_name, context)

    def post(self, request):
        action = request.POST.get('action')
        email = request.POST.get('email')
        context = self.get_context(email=email)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            context['error'] = '사용자 Email을 다시 입력해주세요.'
            return render(request, self.template_name, context)

        if action == "send_code":
            verification_code = generate_verification_code()
            save_verification_code(user, email, verification_code)
            send_email_with_verification_code(email, verification_code, name=user)

        elif action == "check_code":
            try:
                user_email_verify = EmailVerification.objects.get(email=email)
                get_code = user_email_verify.verification_code
                input_code = request.POST.get('code')

                if get_code == input_code:
                    user_email_verify.is_verificate = True
                    user_email_verify.save()
                    return redirect('App_Auth:password_change', user.id)
                else:
                    context['error'] = "인증 코드를 다시 확인해주세요"
            except EmailVerification.DoesNotExist:
                context['error'] = "유효하지 않은 인증 코드입니다."


        return render(request, self.template_name, context)
