from django.http import Http404
from django.db.models import Count, Q
from dateutil import parser

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Post, Like
from .serializers import PostSerializer, LikeSerializer
from .permissions import IsOwner, IsOwnerOrReadOnly


def get_post_object(pk):
    try:
        return Post.objects.get(id=pk)
    except Like.DoesNotExist:
        raise Http404


class PostList(APIView):
    permission_classes = (IsAuthenticated,)

    # def perform_create(self, serializer):
    #     serializer.save(created_by=self.request.user.id)

    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetail(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostLike(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        likes = Like.objects.filter(post_id=pk)
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        post_object = get_post_object(pk)
        serializer = LikeSerializer(data=request.data)
        like_list = Like.objects.filter(post=post_object, created_by=self.request.user)
        if len(like_list) > 0:
            data = LikeSerializer(like_list[0]).data
            data['message'] = 'The post already has like'
            return Response(data, status=status.HTTP_409_CONFLICT)
        if serializer.is_valid():
            serializer.save(created_by=self.request.user, post=post_object)
            data = serializer.data
            data['message'] = 'The like for the post has been addedd'
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostUnlike(APIView):
    permission_classes = (IsAuthenticated, IsOwner)

    def delete(self, request, pk):
        post_object = get_post_object(pk)
        like_list = Like.objects.filter(post=post_object, created_by=self.request.user)
        if len(like_list) > 0:
            like_object = like_list[0]
            like_object.delete()
            message = {'message': 'The like for the post has been deleted'}
            return Response(message, status=status.HTTP_200_OK)
        message = {'message': 'No likes found for this post'}
        return Response(message, status=status.HTTP_404_NOT_FOUND)


class Analytics(APIView):
    permission_classes = (IsAuthenticated,)

    def get_data_params(self, param_name):
        param_value = self.request.GET.get(param_name)
        if param_value:
            if parser.parse(param_value):
                return parser.parse(param_value)

    def get(self, request):
        date_from = self.get_data_params('date_from')
        date_to = self.get_data_params('date_to')

        criterion = ~Q(pk__in=[])
        if date_from:
            criterion = criterion & Q(created_at__gte=date_from)
        if date_to:
            criterion = criterion & Q(created_at__lt=date_to)

        data = Like.objects.filter(criterion)\
            .values('created_at__date')\
            .annotate(count=Count('id'))\
            .values('created_at__date', 'count').order_by(
            'created_at__date')
        formatted_data = [{str(item.get('created_at__date')): item.get('count')} for item in data]
        return Response(formatted_data, status=status.HTTP_200_OK)
