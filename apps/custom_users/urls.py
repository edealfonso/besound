from django.urls import path


from .views import *

app_name = 'custom_users_app'

urlpatterns = [
    path('v1/login', LoginPage_APIView.as_view()), 
    path('v1/login/user', UserLogin_APIView.as_view()), 
    path('v1/signup', SignupPage_APIView.as_view()), 
    path('v1/signup/user', UserCreate_APIView.as_view()), 
]
