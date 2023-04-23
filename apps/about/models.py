from django.db import models
from solo.models import SingletonModel

class AboutPage(SingletonModel):
    intro_text = models.TextField(blank=True)
    ending_text_1 = models.TextField(blank=True)
    ending_text_2 = models.TextField(blank=True)

    def __str__(self):
        return "About Page"
    class Meta:
        verbose_name = "About Page"

class Step(models.Model):
    text = models.TextField()
    image = models.FileField(blank=True)
    page = models.ForeignKey(to=AboutPage, related_name='steps', on_delete=models.PROTECT)

    def __str__(self):
        return self.text[:50]