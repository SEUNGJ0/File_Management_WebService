# Generated by Django 4.2.3 on 2023-09-25 09:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App_Auth', '0011_user_is_verificate_alter_user_company_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_verificate',
        ),
    ]