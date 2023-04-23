from apps.posts.models import Post
from apps.posts.serializers import PostListSerializer, PostCreateSerializer

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import FileUploadParser


class PostList_APIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None, *args, **kwargs):
        post = Post.objects.all()
        serializer = PostListSerializer(post, many=True, context={'request': request})

        return Response(serializer.data)


class CreatePost_APIView(APIView):
    # permission_classes = [IsAuthenticated]
    # parser_classes = [FileUploadParser]

    def post(self, request, format=None):
        file_obj = request.data['file']
        
        serializer = PostCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
