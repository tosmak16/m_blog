from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import User
import jwt, os
from .helper import VerifyToken
from rest_framework.views import APIView
from datetime import datetime, timedelta

from django.contrib.auth import authenticate


class IndexViewSet(APIView):
    authentication_classes = (VerifyToken,)

    def get(self, request):
        return HttpResponse("Hello welcome to my blog")


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

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
                            'exp': datetime.utcnow() + timedelta(minutes=30)},
                           os.getenv('SECERT_KEY'), algorithm='HS256')
        return Response({'message': 'you have logged in successfully', 'token': token}, status=status_type)



