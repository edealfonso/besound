from apps.about.models import AboutPage
from apps.about.serializers import AboutPageSerializer
from apps.home.models import HomePage
from apps.home.serializers import HomePageSerializer

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response

class AboutPage_APIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None, *args, **kwargs):
        page = AboutPage.objects.first()
        serializer = AboutPageSerializer(page, context={'request': request })

        return Response(serializer.data)