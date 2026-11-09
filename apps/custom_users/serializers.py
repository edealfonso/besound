from apps.custom_users.models import CustomUser, LoginPage, RegisterPage
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password


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
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        user = CustomUser(**{k: v for k, v in attrs.items() if k != 'password'})
        validate_password(attrs['password'], user)
        return attrs

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


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
