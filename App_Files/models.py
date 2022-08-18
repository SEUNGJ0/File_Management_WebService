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
        return reverse('App_Board:post_in_category', args=[self.slug])


class Files(models.Model):
    s_category = models.ForeignKey(S_Category, on_delete=models.SET_NULL, null=True, related_name='files')
    l_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    file = models.FileField(upload_to='file/자료 취합/취합 파일')

    def get_filename(self):
        return str(self.file).split('/')[-1]


        
    