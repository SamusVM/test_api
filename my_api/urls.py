from django.urls import path

from .views import PostList, PostDetail, PostLike, PostUnlike, Analytics

app_name = 'my_api'
urlpatterns = [
    path('posts/', PostList.as_view(), name='post_list'),
    path('posts/<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('posts/<int:pk>/like', PostLike.as_view(), name='post_like'),
    path('posts/<int:pk>/unlike', PostUnlike.as_view(), name='post_unlike'),
    path('analytics/', Analytics.as_view(), name='analytics'),
]