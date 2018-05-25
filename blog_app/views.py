from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import UserSerializer, PostSerializer, RatingSerializer
from .models import User, Post
import jwt, os
from .helper import VerifyToken, PostPermission, GetAdminPermissions, GetAdminAndUserPermissions
from datetime import datetime, timedelta


from django.contrib.auth import authenticate


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (PostPermission,)

    @action(methods=['PATCH'], detail=True)
    def publish(self, request, **kwargs):
        return self.publish_handler(request)

    @action(methods=['PATCH'], detail=True)
    def unpublish(self, request, **kwargs):
        return self.publish_handler(request,publish_type=False,
                                    success_message='post unpublish successfully',
                                    error_message='Sorry, you can not unpublish this post')

    @action(methods=['POST'], detail=True, url_path='rate')
    def rate_post(self, request, **kwargs):
        authenticated_user = VerifyToken().authenticate(request)
        post = self.get_object()
        serialized_new_rating = RatingSerializer(data=dict(post=post.id, user=authenticated_user.id,
                                                           score=request.data.get('score')))
        if serialized_new_rating.is_valid():
            serialized_new_rating.save()
            return Response(dict(data=serialized_new_rating.data, message='Rated successfully'),
                            status=status.HTTP_200_OK)
        return Response(dict(message=serialized_new_rating.errors), status=status.HTTP_400_BAD_REQUEST)

    def publish_handler(self, request, publish_type=True, success_message=None, error_message=None):
        authenticated_user=VerifyToken().authenticate(request)
        post = self.get_object()
        if post.user_id != authenticated_user.id or post.is_published == publish_type:
            return Response({'message': error_message or 'Sorry, you can not publish this post'},
                            status=status.HTTP_403_FORBIDDEN)
        post.published_date = datetime.utcnow()
        post.is_published = publish_type
        post.save()
        post_content = {'id': post.id, 'title': post.title, 'body': post.body, 'user':post.user_id,
                        'created_date': post.created_date, 'published_date': post.published_date,
                        'is_published': post.is_published}
        return Response({"message": success_message or 'post publish successfully', 'data': post_content},
                        status=status.HTTP_200_OK)


class UserViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (GetAdminPermissions,)


class UserDetailViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (GetAdminAndUserPermissions,)
    lookup_field = 'id'

    @action(methods=['POST'], detail=False)
    def signup(self, request):
        serialized_user = UserSerializer(data=request.data)
        if serialized_user.is_valid():

            email = request.data.get('email')
            username = request.data.get('username')
            password = request.data.get('password')
            User.objects.create_user(email=email, username=username, password=password)
            return self.signin(request, status.HTTP_201_CREATED)
        return Response({'message': serialized_user.errors}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=False)
    def signin(self, request, status_type=status.HTTP_200_OK):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email:
            return Response({'message': 'email is required'}, status=status.HTTP_400_BAD_REQUEST)

        if not password:
            return Response({'message': 'password is required'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(email=email, password=password)
        if user is None:
            return Response({'message': 'email and password is incorrect'}, status=status.HTTP_401_UNAUTHORIZED)
        token = jwt.encode({'email': user.email, 'username': user.username,
                            'exp': datetime.utcnow() + timedelta(days=1)},
                           os.getenv('SECERT_KEY'), algorithm='HS256')
        return Response({'message': 'you have logged in successfully', 'token': token}, status=status_type)

    @action(methods=['get'], detail=True, url_path='posts')
    def get_single_user_post(self, request, **kwargs):
        VerifyToken().authenticate(request)
        user = self.get_object()
        post=list(Post.objects.filter(user_id=user).values())
        PostSerializer(post)
        return Response({'data': post}, status.HTTP_200_OK)




