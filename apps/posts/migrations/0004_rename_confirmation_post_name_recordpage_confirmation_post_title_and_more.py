# Generated by Django 4.2 on 2023-05-01 17:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_rename_name_post_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recordpage',
            old_name='confirmation_post_name',
            new_name='confirmation_post_title',
        ),
        migrations.RenameField(
            model_name='recordpage',
            old_name='confirmation_pre_name',
            new_name='confirmation_pre_title',
        ),
    ]