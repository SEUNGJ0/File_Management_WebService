# Generated by Django 4.0.6 on 2022-07-27 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_Board', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='post_context',
            field=models.TextField(max_length=2000),
        ),
    ]
