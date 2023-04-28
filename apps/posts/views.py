from apps.posts.models import Post, RecordPage
from apps.posts.serializers import PostListSerializer, PostCreateSerializer, RecordPageSerializer

from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from django.http import Http404


class PostList_APIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None, *args, **kwargs):
        post = Post.objects.all()
        serializer = PostListSerializer(post, many=True, context={'request': request})

        return Response(serializer.data)


class PostCreate_APIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwrags):        
        serializer = PostCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDelete_APIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class RecordPage_APIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None, *args, **kwargs):
        post = RecordPage.objects.first()
        serializer = RecordPageSerializer(post, context={'request': request})

        return Response(serializer.data)