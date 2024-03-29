# Generated by Django 4.0.6 on 2022-08-09 09:27

import App_Board.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_Board', '0019_remove_board_file_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=App_Board.models.file_dir_path, verbose_name='파일 경로'),
        ),
        migrations.AlterField(
            model_name='file',
            name='file_name',
            field=models.CharField(max_length=30, verbose_name='파일 이름'),
        ),
    ]
