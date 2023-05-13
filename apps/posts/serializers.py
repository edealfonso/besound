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
            'step1_instruction',
            'step2_instruction',
            'step3_instruction',
            'step3_back',
            'step3_forward',
            'step4_instruction',
            'step4_back',
            'step4_forward' ,
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
