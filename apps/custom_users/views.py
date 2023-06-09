from apps.custom_users.models import LoginPage, RegisterPage
from apps.custom_users.serializers import LoginPageSerializer, RegisterPageSerializer, CustomUserSerializer

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class Register_APIView(APIView):

    def get(self, request, format=None, *args, **kwargs):
        page = RegisterPage.objects.first()
        serializer = RegisterPageSerializer(page)

        return Response(serializer.data)
    
    def post(self, request, format=None):        
        serializer = CustomUserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Login_APIView(ObtainAuthToken):

    def get(self, request, format=None, *args, **kwargs):
        page = LoginPage.objects.first()
        serializer = LoginPageSerializer(page)
        
        return Response(serializer.data)


# class checkToken_APIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         content = {'message': 'OK'}
#         return Response(content)
