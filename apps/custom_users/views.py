from apps.about.models import AboutPage
from apps.about.serializers import AboutPageSerializer
from apps.custom_users.models import CustomUser, LoginPage, SignupPage
from apps.custom_users.serializers import LoginPageSerializer, SignupPageSerializer, UserCreateSerializer, UserLoginSerializer
from apps.home.models import HomePage
from apps.home.serializers import HomePageSerializer

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# from django.db.models import Q

class Login_APIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None, *args, **kwargs):
        page = LoginPage.objects.first()
        serializer = LoginPageSerializer(page, context={'request': request })

        return Response(serializer.data)
    
    def post (self, request, format=None, *args, **kwargs):
        print(request.data)
        user = CustomUser.objects.filter(email=request.data['email'])
        serializer = UserLoginSerializer(user)

        return Response(serializer.data)


class Signup_APIView(APIView):
    permission_classes = [AllowAny]

    def get_object(self):
        return self.request.user

    def get(self, request, format=None, *args, **kwargs):
        page = SignupPage.objects.first()
        serializer = SignupPageSerializer(page, context={'request': request })

        return Response(serializer.data)
    
    def post(self, request, format=None):        
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
