from django.urls import include, path
from .views import PostList_APIView, CreatePost_APIView

app_name = 'posts_app'

urlpatterns = [
    path('v1/posts', PostList_APIView.as_view()), 
    path('v1/post', CreatePost_APIView.as_view()), 
]