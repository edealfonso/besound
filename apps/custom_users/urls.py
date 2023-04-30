from django.urls import path

from .views import *
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'custom_users_app'

urlpatterns = [
    path('v1/login', Login_APIView.as_view()), 
    path('v1/register', Register_APIView.as_view()), 
]
