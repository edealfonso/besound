from apps.posts.models import Post
from rest_framework import serializers


class PostListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ['name', 'slug', 'audio' ]

class PostCreateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ['name', 'audio', 'effect']
