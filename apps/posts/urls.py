from django.urls import include, path
from .views import PostCreate_APIView, PostList_APIView

app_name = 'posts_app'

urlpatterns = [
    path('v1/posts/list', PostList_APIView.as_view()), 
    path('v1/posts/new', PostCreate_APIView.as_view()), 
    # path('v1/post/delete/<int:pk>', PostDelete_APIView.as_view()), 
]