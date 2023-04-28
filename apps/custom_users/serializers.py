from apps.custom_users.models import CustomUser, LoginPage, SignupPage
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

# class LoginSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ['name', 'password']


##### PAGES (get)
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



# class AuthCustomTokenSerializer(serializers.Serializer):
#     email_or_username = serializers.CharField()
#     password = serializers.CharField()

#     def validate(self, attrs):
#         email_or_username = attrs.get('email_or_username')
#         password = attrs.get('password')

#         if email_or_username and password:
#             # Check if user sent email
#             if validateEmail(email_or_username):
#                 user_request = get_object_or_404(
#                     CustomUser,
#                     email=email_or_username,
#                 )

#                 email_or_username = user_request.username

#             user = authenticate(username=email_or_username, password=password)

#             if user:
#                 if not user.is_active:
#                     msg = _('User account is disabled.')
#                     raise exceptions.ValidationError(msg)
#             else:
#                 msg = _('Unable to log in with provided credentials.')
#                 raise exceptions.ValidationError(msg)
#         else:
#             msg = _('Must include "email or username" and "password"')
#             raise exceptions.ValidationError(msg)

#         attrs['user'] = user
#         return attrs