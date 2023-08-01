from App_Board.models import *
from django.db import models
from django.urls import reverse

# Create your models here.

class File_Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('App_Files:File_in_category', args=[self.slug])


class Integrated_Files(models.Model):
    file_category = models.ForeignKey(File_Category, on_delete=models.SET_NULL, null=True, related_name='files')
    post = models.ForeignKey(Board, on_delete=models.CASCADE, null=True)
    file = models.ForeignKey(Files, on_delete=models.CASCADE, null=True)
    integrated_file = models.FileField(default= None, null=True)

    def get_filename(self):
        return str(self.file).split('/')[-1]
    
    def get_integrated_filename(self):
        return str(self.integrated_file).split('/')[-1]
    
    def get_filecreatetime(self):
        import os, time
        file_path = os.getcwd()+"/media/"+str(self.integrated_file)
        create_time = time.strftime("%Y년 %m월 %d일 %H:%M", time.localtime(os.path.getctime(file_path)))
        return create_time
    
    class Meta:
        ordering = ['-id']

class ErrorLog(models.Model):
    title = models.CharField(max_length=100)
    error_message = models.JSONField(default=dict)
    created_date = models.DateTimeField(auto_now_add=True, null = True)

    def get_absolute_url(self):
        return reverse('App_Files:ErrorLogDetail', args = [str(self.id)])   

