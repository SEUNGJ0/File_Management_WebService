# Generated by Django 4.0.6 on 2022-08-10 05:19

import App_Board.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_Board', '0021_board_file_delete_file'),
    ]

    operations = [
        migrations.RenameField(
            model_name='board',
            old_name='file',
            new_name='file_1',
        ),
        migrations.AddField(
            model_name='board',
            name='file_2',
            field=models.FileField(blank=True, null=True, upload_to=App_Board.models.file_dir_path, verbose_name='파일 경로'),
        ),
        migrations.AddField(
            model_name='board',
            name='file_3',
            field=models.FileField(blank=True, null=True, upload_to=App_Board.models.file_dir_path, verbose_name='파일 경로'),
        ),
    ]
