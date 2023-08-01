from django.db import models
from django.urls import reverse
from App_Auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True, allow_unicode=True)
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('App_Board:board_render_view', args=[self.slug])
        
class Board(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null = True, related_name='boards')
    post_author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_name = models.CharField(max_length=100)
    post_content = models.TextField(max_length=1000)
    post_views_counting = models.IntegerField(default=0)

    # 글 작성 일을 객체가 추가될 때 자동으로 설정
    created_date = models.DateTimeField(auto_now_add=True)
    # 글 수정 일을 수정될 때 자동으로 설정
    updated_date = models.DateTimeField(auto_now=True)
    
    # 해당 모델의 객체들의 정렬 기준을 설정 [ updated --> 내림차순 ]
    class Meta:
        ordering = ['-id']

    def __str__(self):
        # 객체를 출력할 떄 나타날 값
        return self.post_name 

    ## 객체의 상세화면 주소를 반환하게 만든다. ## 
    def get_absolute_url(self):
        return reverse('App_Board:post_render_view',  args = [str(self.id)])    

class EditLog(models.Model):
    post = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='editlogs')
    editor = models.ForeignKey(User, on_delete=models.CASCADE)
    edit_date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return "게시글 : " + str(self.post) + ", 수정일 : " + str(self.edit_date)

def file_dir_path(instance, file):
    if instance.post.category.id == 3:
        return f'file/{instance.post.category}/{instance.post.post_author.company}/{file}'
    else:
        return f'file/{instance.post.category}/{instance.post.post_author.name}/{instance.post.id}/{file}'

def output_filesize(file):
    import math, os
    size_bytes = os.path.getsize(os.getcwd()+"/media/"+str(file))
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])

class Photo(models.Model):
    post = models.ForeignKey(Board, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to=file_dir_path, blank=True, null=True)

    def get_imagename(self):
        return str(self.image).split('/')[-1]

class Files(models.Model):
    post = models.ForeignKey(Board, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    file = models.FileField(upload_to=file_dir_path, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def get_filename(self):
        return str(self.file).split('/')[-1]
    
    # 파일의 크기 출력
    def get_filesize(self):
        return output_filesize(self.file)

    # 파일의 생성 날짜 출력
    def get_filecreatetime(self):
        import os, time
        file_path = os.getcwd()+"/media/"+str(self.file)
        create_time = time.strftime("%Y년 %m월 %d일 %H:%M", time.localtime(os.path.getctime(file_path)))
        return create_time
    
    def get_filepath(self):
        return str(self.file)
    
    def __str__(self):
        # 객체를 출력할 떄 나타날 값
        return self.get_filename() 