# Generated by Django 4.2 on 2023-04-23 00:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('custom_users', '0003_alter_customuser_options_remove_customuser_username'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='signuppage',
            options={'verbose_name': 'Signup Page'},
        ),
    ]