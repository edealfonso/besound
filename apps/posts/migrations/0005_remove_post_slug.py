# Generated by Django 4.2 on 2023-05-01 17:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_rename_confirmation_post_name_recordpage_confirmation_post_title_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='slug',
        ),
    ]
