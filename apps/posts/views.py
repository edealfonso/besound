from apps.posts.models import Post, RecordPage
from apps.posts.serializers import PostListSerializer, PostCreateSerializer, RecordPageSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from django.http import Http404


class PostList_APIView(APIView):

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
        print('*****')
        print('*****')
        print(id)
        print('*****')
        print('*****')
        post = self.get_post(id)
        if (post.author == request.user):
            post.delete()
            return Response({
                "message": 'Successfully deleted post with id ' + id
            }, status=status.HTTP_204_NO_CONTENT)
        else:
            Response(status=status.HTTP_401_UNAUTHORIZED)


