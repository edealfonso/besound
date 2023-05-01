from apps.about.models import AboutPage, Step
from rest_framework import serializers


class StepsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = ['text', 'image']


class AboutPageSerializer(serializers.HyperlinkedModelSerializer):
    steps = StepsSerializer(many=True, read_only=True)

    class Meta:
        model = AboutPage
        fields = [
            'intro_text', 
            'ending_text_1', 
            'ending_text_2',
            'steps',
        ]
