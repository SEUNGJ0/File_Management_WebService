# Generated by Django 4.0.6 on 2022-08-01 12:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App_Board', '0004_remove_board_post_writer_board_post_author'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='board',
            options={'ordering': ['-id']},
        ),
    ]
