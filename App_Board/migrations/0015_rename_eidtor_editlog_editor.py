# Generated by Django 4.0.6 on 2022-08-03 16:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App_Board', '0014_editlog_eidtor'),
    ]

    operations = [
        migrations.RenameField(
            model_name='editlog',
            old_name='eidtor',
            new_name='editor',
        ),
    ]
