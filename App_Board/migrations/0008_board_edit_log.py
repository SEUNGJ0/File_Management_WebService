# Generated by Django 4.0.6 on 2022-08-03 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_Board', '0007_remove_board_post_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='edit_log',
            field=models.JSONField(default={'time': 'name'}, verbose_name={}),
            preserve_default=False,
        ),
    ]
