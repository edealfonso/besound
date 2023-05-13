import uuid
from django.db import models
from apps.custom_users.models import CustomUser
from solo.models import SingletonModel
from ckeditor.fields import RichTextField

class RecordPage(SingletonModel):
    step1_instruction = RichTextField(blank=True)
    step2_instruction = RichTextField(blank=True)
    step3_instruction = RichTextField(blank=True)
    step3_back = models.CharField(blank=True, max_length=20)
    step3_forward = models.CharField(blank=True, max_length=20)
    step4_instruction = RichTextField(blank=True)
    step4_back = models.CharField(blank=True, max_length=20)
    step4_forward = models.CharField(blank=True, max_length=20)
    confirmation_pre_title = models.CharField(blank=True, max_length=100)
    confirmation_post_title = models.TextField(blank=True)
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
        
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, unique=True)
    audio = models.FileField(upload_to="audio")
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(to=CustomUser, related_name='post_author', on_delete=models.PROTECT)

    def __str__(self):
        return self.title