# Generated by Django 4.0.6 on 2022-08-02 09:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App_Board', '0006_board_post_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='board',
            name='post_file',
        ),
    ]
