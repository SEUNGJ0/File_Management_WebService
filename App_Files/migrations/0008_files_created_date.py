# Generated by Django 4.0.6 on 2022-08-18 16:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('App_Files', '0007_alter_files_options_alter_files_board'),
    ]

    operations = [
        migrations.AddField(
            model_name='files',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
