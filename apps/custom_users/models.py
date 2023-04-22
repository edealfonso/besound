from django.contrib.auth.models import AbstractUser
from django.db import models
from solo.models import SingletonModel

class LoginPage(SingletonModel):
    instruction = models.CharField(max_length=255)
    button = models.CharField(max_length=255)

    def __str__(self):
        return "Login Page"
    class Meta:
        verbose_name = "Login Page"

class SignupPage(SingletonModel):
    text_1 = models.CharField(max_length=255)
    text_2 = models.CharField(max_length=255)
    button_login = models.CharField(max_length=255)
    text_3 = models.CharField(max_length=255)
    text_4 = models.CharField(max_length=255)
    button_end = models.CharField(max_length=255)

    def __str__(self):
        return "Login Page"
    class Meta:
        verbose_name = "Login Page"

# class CustomUser(AbstractUser):
#     first_name = models.CharField(max_length=255)
#     last_name = models.CharField(max_length=255)
#     birth_date = models.DateField()
#     nationality = models.CharField(max_length=255)
#     email = models.EmailField(unique = True)
