from django.db import models
from solo.models import SingletonModel
from autoslug import AutoSlugField

class RecordPage(SingletonModel):
    phase1_instruction = models.CharField(blank=True, max_length=100)
    phase2_instruction = models.CharField(blank=True, max_length=100)
    phase3_instruction = models.CharField(blank=True, max_length=100)
    phase3_back = models.CharField(blank=True, max_length=20)
    phase3_forward = models.CharField(blank=True, max_length=20)
    phase4_instruction = models.CharField(blank=True, max_length=100)
    phase4_back = models.CharField(blank=True, max_length=20)
    phase4_forward = models.CharField(blank=True, max_length=20)
    confirmation_pre_name = models.CharField(blank=True, max_length=100)
    confirmation_post_name = models.TextField(blank=True)
    confirmation_regret = models.TextField(blank=True)
    confirmation_remember = models.TextField(blank=True)
    error_text_1 = models.TextField(blank=True)
    error_text_2 = models.TextField(blank=True)
    error_back = models.TextField(blank=True)
    error_forward = models.TextField(blank=True)
    success = models.TextField(blank=True)

    def __str__(self):
        return "Record Page"
    class Meta:
        verbose_name = "Record Page"

class Effect(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(unique=True, editable=False, populate_from='name')

class Post(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(unique=True, editable=False, populate_from='name')
    audio = models.FileField()
    effect = models.ForeignKey(to=Effect, on_delete=models.SET_NULL, null=True)
