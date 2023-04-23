from apps.home.models import HomePage
from rest_framework import serializers


class HomePageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = HomePage
        fields = ['logo', 'motto', 'instruction', 'error_not_found']