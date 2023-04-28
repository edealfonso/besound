from django.urls import path

from .views import *

app_name = 'custom_users_app'

urlpatterns = [
    path('v1/page/login', Login_APIView.as_view()), 
    path('v1/page/register', Register_APIView.as_view()), 
]
