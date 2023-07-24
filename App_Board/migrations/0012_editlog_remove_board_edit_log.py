# Generated by Django 4.0.6 on 2022-08-03 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_Board', '0011_alter_board_edit_log'),
    ]

    operations = [
        migrations.CreateModel(
            name='EditLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('edit_date', models.DateTimeField()),
            ],
        ),
        migrations.RemoveField(
            model_name='board',
            name='edit_log',
        ),
    ]
