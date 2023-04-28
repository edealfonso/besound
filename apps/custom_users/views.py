from apps.custom_users.models import LoginPage, RegisterPage
from apps.custom_users.serializers import LoginPageSerializer, RegisterPageSerializer, RegisterSerializer

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class Register_APIView(APIView):
    permission_classes = [AllowAny]

    def get_object(self):
        return self.request.user

    def get(self, request, format=None, *args, **kwargs):
        page = RegisterPage.objects.first()
        serializer = RegisterPageSerializer(page)
        return Response(serializer.data)
    
    def post(self, request, format=None):        
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class RegisterPage_APIView(APIView):
    def get(self, request, format=None, *args, **kwargs):
        page = RegisterPage.objects.first()
        serializer = RegisterPageSerializer(page)

        return Response(serializer.data)

class LoginPage_APIView(APIView):
    def get(self, request, format=None, *args, **kwargs):
        page = LoginPage.objects.first()
        serializer = LoginPageSerializer(page)

        return Response(serializer.data)