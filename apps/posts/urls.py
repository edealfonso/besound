from django.urls import include, path
from .views import PostCreate_APIView, PostDelete_APIView, PostList_APIView, RecordPage_APIView

app_name = 'posts_app'

urlpatterns = [
    path('v1/posts', PostList_APIView.as_view()), 
    path('v1/new', PostCreate_APIView.as_view()), 
    path('v1/delete/<int:pk>', PostDelete_APIView.as_view()), 
    path('v1/page/record', RecordPage_APIView.as_view()), 
]