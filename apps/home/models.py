from django.db import models
from solo.models import SingletonModel

class HomePage(SingletonModel):
    logo = models.FileField(blank=True)
    motto = models.CharField(blank=True, max_length=100)
    instruction = models.CharField(blank=True, max_length=100)
    error_not_found = models.TextField(blank=True)

    def __str__(self):
        return "Home Page"
    class Meta:
        verbose_name = "Home Page"
