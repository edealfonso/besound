from apps.custom_users.models import CustomUser, LoginPage, SignupPage
from rest_framework import serializers


class UserCreateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'email', 
            'last_name', 
            'first_name',
            'nationality',
            'birth_date',
            'password1',
            'password2',
        ]

class UserLoginSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['name', 'password']

class LoginPageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LoginPage
        fields = [
            'instruction', 
            'button',
            ]


class SignupPageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SignupPage
        fields = [
            'text_1', 
            'text_2',
            'button_login',
            'text_3',
            'text_4',
            'button_end',
            'confirmation_pre',
            'confirmation_post',
            ]
