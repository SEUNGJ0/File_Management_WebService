# Generated by Django 4.0.6 on 2022-08-20 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_Files', '0011_rename_error_errorlog_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='errorlog',
            name='error_message',
            field=models.JSONField(default='{}'),
        ),
    ]
