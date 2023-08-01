# Generated by Django 4.2.3 on 2023-07-31 16:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App_Board', '0027_files_user'),
        ('App_Files', '0014_integrated_files_rename_s_category_file_category_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='integrated_files',
            name='created_date',
        ),
        migrations.AlterField(
            model_name='integrated_files',
            name='file',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='App_Board.files'),
        ),
    ]
