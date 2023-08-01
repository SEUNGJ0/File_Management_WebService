from django import forms
from .models import *


class BoardForm(forms.ModelForm):
    class Meta:
        model = Board  # 사용할 모델
        fields = ["post_name", "post_content"]  # BoardForm에서 사용할 Board 모델의 속성
        labels = {
            'post_name' : '게시글 제목',
            'post_content' : '게시글 내용'
        }
      

class EditLogForm(forms.ModelForm):
    class Meta:
        model = EditLog
        fields = ["editor"]
    


