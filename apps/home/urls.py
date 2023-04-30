from django.urls import include, path

from .views import HomePage_APIView

app_name = 'home_app'

urlpatterns = [
    path('v1/home', HomePage_APIView.as_view()), 
]
