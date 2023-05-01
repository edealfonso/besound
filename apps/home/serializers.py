from apps.home.models import HomePage
from rest_framework import serializers


class HomePageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = HomePage
        fields = ['motto', 'instruction', 'error_not_found']