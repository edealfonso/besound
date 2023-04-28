from django.urls import include, path
from .views import PostCreate_APIView   , PostList_APIView, RecordPage_APIView

app_name = 'posts_app'

urlpatterns = [
    path('v1/post/list', PostList_APIView.as_view()), 
    path('v1/post/new', PostCreate_APIView.as_view()), 
    # path('v1/post/delete/<int:pk>', PostDelete_APIView.as_view()), 
    path('v1/page/record', RecordPage_APIView.as_view()), 
]