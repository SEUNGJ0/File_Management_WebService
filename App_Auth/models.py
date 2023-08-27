from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import RegexValidator

# 사용자 생성 및 관리 기능을 구현
class UserManager(BaseUserManager):    
    use_in_migrations = True    
    # 파라미터를 받아서 새로운 사용자를 생성하고 저장
    def create_user(self, email, name, phone_number, company, password):        
        if not email:            
            raise ValueError('이메일은 필수입니다.')
        if not password:            
            raise ValueError('비밀번호는 필수입니다.')
 
        user = self.model(            
            email=self.normalize_email(email),
            name = name,       
            phone_number = phone_number,
            company = company
        )        
        user.set_password(password)        
        user.save(using=self._db)        
        return user

    # create_user를 호출하여 관리자 권한을 추가로 설정
    def create_superuser(self, email, name, phone_number, company, password):        
    
        user = self.create_user(            
            email = self.normalize_email(email),
            name = name,       
            phone_number = phone_number,
            company = company,                      
            password = password,        
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user 

class User(AbstractBaseUser, PermissionsMixin):    
    objects = UserManager()
    email = models.EmailField(max_length=255, unique=True, verbose_name='이메일')
    name = models.CharField(max_length=30, verbose_name='이름')
    phoneNumberRegex = RegexValidator(regex = r'^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$')
    phone_number = models.CharField(validators = [phoneNumberRegex], max_length = 11, unique = True, verbose_name='전화번호')
    company = models.CharField(max_length=30, verbose_name='회사명/회사코드')
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
 
    USERNAME_FIELD = 'email'    # -> 사용자 고유 식별 필드 설정
    REQUIRED_FIELDS = ['name','phone_number','company'] # -> 슈퍼유저를 생성할때 필요한 필드 설정
 
    def __str__(self):
        return self.name
 
    @property
    def is_staff(self):
        return self.is_admin