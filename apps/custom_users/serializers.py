from apps.custom_users.models import CustomUser, LoginPage, RegisterPage
from rest_framework import serializers
from django.contrib.auth import authenticate


##### FORMS (post)

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        max_length = 128,
        min_length = 6,
        write_only = True
    )

    class Meta:
        model = CustomUser
        fields = [
            'email', 
            'last_name', 
            'first_name',
            'nationality',
            'birth_date',
            'password',
        ]
    
    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


##### PAGES (get)
class LoginPageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LoginPage
        fields = [
            'instruction', 
            'button',
            ]

class RegisterPageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RegisterPage
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
