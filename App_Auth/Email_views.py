import smtplib, random, string
from email.mime.text import MIMEText
from config.get_secret import get_secret, input_secret
from django.shortcuts import render, redirect
from django.views import View

from App_Board.models import Category
from App_Auth.models import User  


def generate_verification_code():
    characters = string.ascii_letters + string.digits  # 알파벳과 숫자를 조합하여 문자셋 생성
    return ''.join(random.choices(characters, k=6))

def send_email_with_verification_code(email, verification_code, name):
    send_email = get_secret('Send_Email')
    recv_email = email
    password = get_secret('Naver_Password')
		
    # SMTP 서버 설정
    smtp_server = "smtp.naver.com" 
    smtp_port = 587

    # 이메일 내용 설정    
    text = f"인증 코드 : {verification_code}"
    msg = MIMEText(text) 
    if name:
        msg['Subject'] =f"{name}님의 이메일 인증코드입니다."
    else:
        msg['Subject'] =f"Django Website에서 보내는 이메일 인증코드입니다."
    msg['From'] = send_email
    msg['To'] = recv_email

    # SMTP 서버를 사용하여 이메일 전송
    with smtplib.SMTP(smtp_server, smtp_port) as s:
        s.starttls() # TLS 보안 연결 시작
        s.login(send_email, password) # 이메일 발신자 로그인
        # s.sendmail(send_email, recv_email, msg.as_string()) # 이메일 전송

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

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            context.update(email=False, error='사용자 Email을 다시 입력해주세요.')
            return render(request, self.template_name, context)
        
        if action == "send_code":
            verification_code = generate_verification_code()
            input_secret(email, verification_code)
            send_email_with_verification_code(email, verification_code, name=user)
            context['info'] = f"해당 {email} 주소로 인증 코드가 전송되었습니다."


        elif action == "check_code":
            if self.verify_code(request, email):
                context.update(email_verified=True, success="이메일 인증에 성공했습니다.")
                input_secret(email, True)     
                return redirect('App_Auth:password_change', user.id)
            else:
                context['error'] = "인증 코드를 다시 확인해주세요"
                
        return render(request, self.template_name, context)

    def verify_code(self, request, email):
        get_code = get_secret(email)
        input_code = request.POST.get('code')
        return get_code == input_code


