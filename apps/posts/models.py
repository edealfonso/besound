from django.db import models
from solo.models import SingletonModel
from autoslug import AutoSlugField
from adminsortable.models import SortableMixin
from ckeditor.fields import RichTextField

class RecordPage(SingletonModel):
    phase1_instruction = RichTextField(blank=True)
    phase2_instruction = RichTextField(blank=True)
    phase3_instruction = RichTextField(blank=True)
    phase3_back = models.CharField(blank=True, max_length=20)
    phase3_forward = models.CharField(blank=True, max_length=20)
    phase4_instruction = RichTextField(blank=True)
    phase4_back = models.CharField(blank=True, max_length=20)
    phase4_forward = models.CharField(blank=True, max_length=20)
    confirmation_pre_name = models.CharField(blank=True, max_length=100)
    confirmation_post_name = models.TextField(blank=True)
    confirmation_regret = models.TextField(blank=True)
    confirmation_remember = models.TextField(blank=True)
    error_text_1 = models.TextField(blank=True)
    error_text_2 = models.TextField(blank=True)
    error_back = models.CharField(blank=True, max_length=20)
    error_forward = models.CharField(blank=True, max_length=20)
    success = models.TextField(blank=True)

    def __str__(self):
        return "Record Page"
    class Meta:
        verbose_name = "Record Page"

class Effect(SortableMixin):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(unique=True, editable=False, populate_from='name')
    the_order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['the_order']
class Post(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(unique=True, editable=False, populate_from='name')
    audio = models.FileField(upload_to="audio")
    effect = models.ForeignKey(to=Effect, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name