# Generated by Django 4.2.3 on 2023-07-27 16:50

import App_Board.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App_Board', '0024_board_counting'),
    ]

    operations = [
        migrations.RenameField(
            model_name='board',
            old_name='post_context',
            new_name='post_content',
        ),
        migrations.RenameField(
            model_name='board',
            old_name='counting',
            new_name='post_views_counting',
        ),
        migrations.RenameField(
            model_name='editlog',
            old_name='board',
            new_name='post',
        ),
        migrations.RemoveField(
            model_name='board',
            name='file',
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to=App_Board.models.file_dir_path)),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='App_Board.board')),
            ],
        ),
        migrations.CreateModel(
            name='Files',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to=App_Board.models.file_dir_path)),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='App_Board.board')),
            ],
        ),
    ]
