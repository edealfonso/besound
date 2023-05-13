from apps.posts.models import Post, RecordPage
from rest_framework import serializers


class PostSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = Post
        fields = ['id', 'title', 'audio']


class RecordPageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RecordPage
        fields = [
            'phase1_instruction',
            'phase2_instruction',
            'phase3_instruction',
            'phase3_back',
            'phase3_forward',
            'phase4_instruction',
            'phase4_back',
            'phase4_forward' ,
            'confirmation_pre_title',
            'confirmation_post_title',
            'confirmation_regret',
            'confirmation_remember' ,
            'error_text_1',
            'error_text_2',
            'error_back',
            'error_forward',
            'success'
            ]
