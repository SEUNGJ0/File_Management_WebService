import smtplib, random, string
from email.mime.text import MIMEText
from config.get_secret import get_secret

class EmailVerification:
    def __init__(self, request, email, user=None, code=False):
        # 초기값 설정
        self.send_email = get_secret('Send_Email')
        self.recv_email = email
        self.password = get_secret('Naver_Password')
        self.code_length = 6

        if code :
            self.verification_code = code
        else:
            self.verification_code = self.generate_verification_code()
            
        session_dict = {'email':email, 'verification_code': self.verification_code, "email_verified":False}
        for key, value in session_dict.items():
            request.session[key] = value

         # SMTP 서버 설정
        self.smtp_server = "smtp.naver.com" 
        self.smtp_port = 587

        # 이메일 내용 설정    
        self.text = f"인증 코드 : {self.verification_code}"
        self.msg = MIMEText(self.text) 
        
        if user:    
            self.msg['Subject'] = f"Django Website에서 보내는 {user}님의 이메일 인증코드입니다."
        else:
            self.msg['Subject'] = f"Django Website에서 보내는 회원가입 이메일 인증코드입니다."

        self.msg['From'] = self.send_email
        self.msg['To'] = self.recv_email

    # SMTP 서버를 사용하여 이메일 전송
    def send_code_email(self, request, context):
        for key, value in request.session.items():
            print(key," : ",value)
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as s:
            s.starttls() # TLS 보안 연결 시작
            s.login(self.send_email, self.password) # 이메일 발신자 로그인
            # s.sendmail(self.send_email, self.recv_email, self.msg.as_string()) # 이메일 전송
        context['info'] = f"해당 {self.recv_email} 주소로 인증 코드가 전송되었습니다."
        return context

    # 알파벳과 숫자를 조합하여 지정한 길이의 문자셋 생성
    def generate_verification_code(self):
        characters = string.ascii_letters + string.digits
        verification_code = ''.join(random.choices(characters, k=self.code_length))
        return verification_code
    
    # 입력한 코드와 생성된 코드를 비교
    def verify_code(self, request):
        get_code = request.session.get('verification_code')
        input_code = request.POST.get('code')
        for key, value in request.session.items():
            print(key," : ",value)
        return get_code == input_code
