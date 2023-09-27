import smtplib, random, string
from email.mime.text import MIMEText
from config.get_secret import get_secret, input_secret

class EmailVerification:
    def __init__(self, email, user=None):
        # 초기값 설정
        self.send_email = get_secret('Send_Email')
        self.recv_email = email
        self.password = get_secret('Naver_Password')
        self.code_length = 6

         # SMTP 서버 설정
        self.smtp_server = "smtp.naver.com" 
        self.smtp_port = 587

        if not get_secret(email) or get_secret(email) == True:
            self.verification_code = self.generate_verification_code()
            input_secret(email, self.verification_code)
        else:
            self.verification_code = None

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
    def send_code_email(self):
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as s:
            s.starttls() # TLS 보안 연결 시작
            s.login(self.send_email, self.password) # 이메일 발신자 로그인
            s.sendmail(self.send_email, self.recv_email, self.msg.as_string()) # 이메일 전송

    # 알파벳과 숫자를 조합하여 지정한 길이의 문자셋 생성
    def generate_verification_code(self):
        characters = string.ascii_letters + string.digits  
        return ''.join(random.choices(characters, k=self.code_length))
    
    # 입력한 코드와 생성된 코드를 비교
    def verify_code(self, request, email):
        get_code = get_secret(email)
        input_code = request.POST.get('code')
        return get_code == input_code
