# Generated by Django 4.2 on 2023-04-22 23:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('custom_users', '0002_alter_customuser_managers'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'ordering': ['email']},
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='username',
        ),
    ]