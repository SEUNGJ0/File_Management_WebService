# Generated by Django 4.0.6 on 2022-08-10 05:07

import App_Board.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_Board', '0020_alter_file_file_alter_file_file_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=App_Board.models.file_dir_path, verbose_name='파일 경로'),
        ),
        migrations.DeleteModel(
            name='File',
        ),
    ]
