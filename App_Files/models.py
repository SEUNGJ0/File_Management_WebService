from App_Board.models import *
from django.db import models
from django.urls import reverse

# Create your models here.

class S_Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('App_Files:File_in_category', args=[self.slug])


class Files(models.Model):
    s_category = models.ForeignKey(S_Category, on_delete=models.SET_NULL, null=True, related_name='files')
    board = models.ForeignKey(Board, on_delete=models.CASCADE, null=True)
    file = models.FileField(upload_to='file/자료 취합/취합 파일', null=True)
    created_date = models.DateTimeField(auto_now_add=True, null = True)

    def get_filename(self):
        return str(self.file).split('/')[-1]
    
    class Meta:
        ordering = ['-id']

class ErrorLog(models.Model):
    title = models.CharField(max_length=100)
    error_message = models.JSONField(default=dict)
    created_date = models.DateTimeField(auto_now_add=True, null = True)

    def get_absolute_url(self):
        return reverse('App_Files:ErrorLogDetail', args = [str(self.id)])   

