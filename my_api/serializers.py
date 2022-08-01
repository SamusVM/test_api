from django.contrib.auth import authenticate

from rest_framework import serializers

from .models import Post, Like
from my_auth.models import User


class PostSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Post
        fields = ['pk', 'text', 'created_by', ]


class LikeSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')
    post = serializers.ReadOnlyField(source='post.text')

    class Meta:
        model = Like
        fields = ['post', 'created_by', 'created_at', ]
