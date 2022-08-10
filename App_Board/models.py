from django.db import models
from django.urls import reverse
from App_Auth.models import User
import os

def file_dir_path(instance, file):
    return f'file/{instance.post_author.company}/{instance.post_name}/{file}'

class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True, allow_unicode=True)
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('App_Board:post_in_category', args=[self.slug])
        
class Board(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null = True, related_name='boards')
    post_author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_name = models.CharField(max_length=100)
    post_context = models.TextField(max_length=1000)

    # 글 작성 일을 객체가 추가될 때 자동으로 설정
    created_date = models.DateTimeField(auto_now_add=True)
    # 글 수정 일을 수정될 때 자동으로 설정
    updated_date = models.DateTimeField(auto_now=True)

    file = models.FileField(upload_to=file_dir_path, null=True, blank=True, verbose_name='파일 경로')
    # 해당 모델의 객체들의 정렬 기준을 설정 [ updated --> 내림차순 ]
    class Meta:
        ordering = ['-id']

    def __str__(self):
        # 객체를 출력할 떄 나타날 값
        return self.post_name 

    ## 객체의 상세화면 주소를 반환하게 만든다. ## 
    def get_absolute_url(self):
        return reverse('App_Board:post_detail', args = [str(self.id)])    

    def get_filename(self):
        return str(self.file).split('/')[-1]
        
class EditLog(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='editlogs')
    editor = models.ForeignKey(User, on_delete=models.CASCADE)
    edit_date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return "게시글 : " + str(self.board) + ", 수정일 : " + str(self.edit_date)




