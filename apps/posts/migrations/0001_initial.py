# Generated by Django 4.2 on 2023-04-22 23:15

import autoslug.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Effect',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='RecordPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phase1_instruction', models.CharField(blank=True, max_length=100)),
                ('phase2_instruction', models.CharField(blank=True, max_length=100)),
                ('phase3_instruction', models.CharField(blank=True, max_length=100)),
                ('phase3_back', models.CharField(blank=True, max_length=20)),
                ('phase3_forward', models.CharField(blank=True, max_length=20)),
                ('phase4_instruction', models.CharField(blank=True, max_length=100)),
                ('phase4_back', models.CharField(blank=True, max_length=20)),
                ('phase4_forward', models.CharField(blank=True, max_length=20)),
                ('confirmation_pre_name', models.CharField(blank=True, max_length=100)),
                ('confirmation_post_name', models.TextField(blank=True)),
                ('confirmation_regret', models.TextField(blank=True)),
                ('confirmation_remember', models.TextField(blank=True)),
                ('error_text_1', models.TextField(blank=True)),
                ('error_text_2', models.TextField(blank=True)),
                ('error_back', models.TextField(blank=True)),
                ('error_forward', models.TextField(blank=True)),
                ('success', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'Record Page',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name', unique=True)),
                ('audio', models.FileField(upload_to='')),
                ('effect', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='posts.effect')),
            ],
        ),
    ]
