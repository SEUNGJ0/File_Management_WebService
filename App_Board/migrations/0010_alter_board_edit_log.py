# Generated by Django 4.0.6 on 2022-08-03 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_Board', '0009_alter_board_edit_log'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='edit_log',
            field=models.JSONField(default='dict'),
        ),
    ]
