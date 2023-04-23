from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = (
            'email', 
            'last_name', 
            'first_name',
            'nationality',
            'birth_date',
            'password1',
            'password2'
        )


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = (
            'last_name', 
            'first_name',
            'nationality',
            'birth_date',
            "email", 
            )