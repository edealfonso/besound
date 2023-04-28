from django.urls import path

from .views import *
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'custom_users_app'

urlpatterns = [
    path('v1/user/login', obtain_auth_token),
    path('v1/user/new', Register_APIView.as_view()), 
    path('v1/page/login', LoginPage_APIView.as_view()), 
    path('v1/page/register', Register_APIView.as_view()), 
]
