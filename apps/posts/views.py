from apps.posts.models import Post, RecordPage
from apps.posts.serializers import PostSerializer, RecordPageSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from django.http import Http404


class OptionalPagination(LimitOffsetPagination):
    """Paginate only when ?limit= is given, so the plain list response keeps working."""
    default_limit = None
    max_limit = 100


class PostList_APIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = OptionalPagination


class PostCreate_APIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwrags):        
        serializer = PostSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None, *args, **kwargs):
        post = RecordPage.objects.first()
        serializer = RecordPageSerializer(post, context={'request': request})

        return Response(serializer.data)
    

class PostDelete_APIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_post(self, id):
        try:
            return Post.objects.get(id=id)
        except Post.DoesNotExist:
            raise Http404

    def delete(self, request, id, format=None):
        post = self.get_post(id)

        if post.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        audio = post.audio
        post.delete()
        if audio:
            audio.delete(save=False)  # remove the mp3 from disk too
        return Response({'message': 'OK'}, status=status.HTTP_204_NO_CONTENT)


