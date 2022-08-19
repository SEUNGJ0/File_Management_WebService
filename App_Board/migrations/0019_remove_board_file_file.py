# Generated by Django 4.0.6 on 2022-08-09 08:20

import App_Board.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('App_Board', '0018_alter_board_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='board',
            name='file',
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=App_Board.models.file_dir_path, verbose_name='파일 경로')),
                ('file_name', models.CharField(max_length=30, verbose_name='파일명')),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='App_Board.board', verbose_name='게시글')),
                ('uploader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='업로더')),
            ],
        ),
    ]