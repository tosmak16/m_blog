from django.http import HttpResponse
from django.contrib.auth import authenticate, logout, login
from rest_framework import response, status, views
from .serializers import UserSerializer
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
Response = response.Response


class UserLogin(views.APIView):

    def post(self, request):
        user = authenticate(username=request.data.get('username'),
                            password=request.data.get('password'))
        if user is None:
            return Response({
                'status': 'fail',
                'message': 'username and password is incorrect',
            }, status=status.HTTP_401_UNAUTHORIZED)
        login(request, user)

        user_data = UserSerializer(user).data
        payload=jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        return Response({"data": user_data, "token": token})


def index(request):
    return HttpResponse("Hello welcome to my blog")











