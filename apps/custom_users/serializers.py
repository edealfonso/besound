from apps.custom_users.models import CustomUser, LoginPage, RegisterPage
from rest_framework import serializers
from django.contrib.auth import authenticate


##### FORMS (post)

class CustomUserSerializer(serializers.ModelSerializer):
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
        user = CustomUser.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


##### PAGES (get)
class LoginPageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LoginPage
        fields = [
            'intro', 
            'instruction', 
            'button',
            'signup_intro',
            'signup_link',
            ]


class RegisterPageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RegisterPage
        fields = [
            'login_text',
            'login_link',
            'text_part1',
            'text_part2',
            'button_end',
            'confirmation_pre',
            'confirmation_post',
            ]
