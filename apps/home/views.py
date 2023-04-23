from apps.home.models import HomePage
from apps.home.serializers import HomePageSerializer

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response

class HomePage_APIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None, *args, **kwargs):
        post = HomePage.objects.first()
        serializer = HomePageSerializer(post, context={'request': request})

        return Response(serializer.data)