from cProfile import label
from django import forms
from .models import *


class BoardForm(forms.ModelForm):
    class Meta:
        model = Board  # 사용할 모델
        fields = ["post_name", "post_context","file"]  # BoardForm에서 사용할 Board 모델의 속성
      

class EditLogForm(forms.ModelForm):
    class Meta:
        model = EditLog
        fields = ["editor"]
    


