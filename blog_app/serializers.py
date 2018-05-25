from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueTogetherValidator
from django.db.models import Avg


from .models import Post, Rating


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'password',)


class PostSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'user', 'url', 'created_date',
                  'published_date', 'is_published', 'average_rating',)

    @classmethod
    def get_average_rating(cls, post_object):
        average = Rating.objects.filter(post=post_object).aggregate(Avg('score')).get('score__avg')

        if average is None:
            return 0
        return round(average*2)/2


class RatingSerializer(serializers.ModelSerializer):
    validators = [
        UniqueTogetherValidator(
            queryset=Rating.objects.all(),
            fields=('user', 'post')
        )
    ]

    @classmethod
    def validate_score(cls, score_data):
        if score_data > 5 or score_data < 1:
            raise serializers.ValidationError("score should be between 1 and 5")
        return score_data

    class Meta:
        model = Rating
        fields = ('id', 'score', 'user', 'post', 'created_at')
