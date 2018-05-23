from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from .serializers import UserSerializer
from .models import User


def index(request):
    return HttpResponse("Hello welcome to my blog")


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=['POST'], detail=False)
    def signup(self, request):
        serialized_user = UserSerializer(data=request.data)
        if serialized_user.is_valid():

            email = request.data.get('email')
            username = request.data.get('email')
            password = request.data.get('password')
            user = User.objects.create_user(email=email, username=username, password=password)
            return Response({'data': UserSerializer(user).data}, status=status.HTTP_201_CREATED)
        return Response({'message': serialized_user.errors}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=False)
    def signin(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email:
            return Response({'message': 'email is required'}, status=status.HTTP_400_BAD_REQUEST)

        if not password:
            return Response({'message': 'password is required'}, status=status.HTTP_400_BAD_REQUEST)
        user_list = list(User.objects.filter(email=email).values())
        user = user_list[0] if user_list else user_list
        if not user or check_password(password, user.get('password')):
            return Response({'message': 'email and password is incorrect'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(user, status=status.HTTP_200_OK)



