from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.custom_users.manager import CustomUserManager
from solo.models import SingletonModel

class LoginPage(SingletonModel):
    intro = models.TextField(blank=True)
    instruction = models.TextField(blank=True)
    button = models.CharField(max_length=255, blank=True)
    signup_intro = models.CharField(max_length=255, blank=True)
    signup_link = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return "Login Page"
    class Meta:
        verbose_name = "Login Page"

class RegisterPage(SingletonModel):
    login_text = models.TextField(blank=True)
    login_link = models.CharField(max_length=255, blank=True)
    text_part1 = models.TextField(blank=True)
    text_part2 = models.TextField(blank=True)
    button_end = models.CharField(max_length=255, blank=True)
    confirmation_pre = models.CharField(max_length=20, blank=True)
    confirmation_post = models.TextField(blank=True)

    def __str__(self):
        return "Register Page"
    class Meta:
        verbose_name = "Register Page"

class CustomUser(AbstractUser):
    username = None
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birth_date = models.DateField()
    nationality = models.CharField(max_length=255)
    email = models.EmailField(unique = True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'birth_date', 'nationality']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    class Meta:
        ordering = ['email']