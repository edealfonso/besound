from apps.custom_users.models import CustomUser, LoginPage, RegisterPage
from rest_framework import serializers
from django.contrib.auth import authenticate


##### FORMS (post)

class RegisterSerializer(serializers.ModelSerializer):
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
