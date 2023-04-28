from django.urls import include, path
from .views import PostCreate_APIView, PostList_APIView

app_name = 'posts_app'

urlpatterns = [
    path('v1/posts', PostList_APIView.as_view()), 
    path('v1/new', PostCreate_APIView.as_view()), 
]