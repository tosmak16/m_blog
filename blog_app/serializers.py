from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import User, Post


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'password', 'url')
    url = serializers.HyperlinkedIdentityField(view_name='user-detail', lookup_field='id')


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'user', 'url', 'created_date', 'published_date', 'is_published')