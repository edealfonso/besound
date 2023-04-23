from django.urls import path

from apps.about.views import AboutPage_APIView


app_name = 'about__app'

urlpatterns = [
    path('v1/about', AboutPage_APIView.as_view()), 
]
