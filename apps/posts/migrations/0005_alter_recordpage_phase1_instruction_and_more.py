# Generated by Django 4.2 on 2023-04-23 00:26

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_alter_recordpage_error_back_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recordpage',
            name='phase1_instruction',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='recordpage',
            name='phase2_instruction',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='recordpage',
            name='phase3_instruction',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='recordpage',
            name='phase4_instruction',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
    ]
