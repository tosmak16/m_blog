import jwt, os
from django.contrib.auth.models import User
from .models import User
from rest_framework import authentication, permissions, exceptions


class VerifyToken(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_TOKEN') or request.META.get('token')
        key = os.getenv('SECERT_KEY')
        try:
            username=jwt.decode(token, key=key, algorithms=['HS256'], options={
                        'verify_signature': True,
                        'verify_exp': True

            }).get('username')
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired')
        except jwt.InvalidAlgorithmError as error:
            if str(error):
                raise exceptions.AuthenticationFailed('User Authorization failed. Enter a valid token.')
        except jwt.DecodeError as error:
            if str(error) == 'Signature verification failed':
                raise exceptions.AuthenticationFailed('Token Signature verification failed.')
            else:
                raise exceptions.AuthenticationFailed('Authorization failed due to an Invalid token.')

        if not username:
            return None
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')
        return user


class PostPermission(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.method == "POST":
            if VerifyToken().authenticate(request):
                return True
            return False
        return True


class GetAdminPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == "GET":
            authenticated_user = VerifyToken().authenticate(request)
            if authenticated_user is None or not authenticated_user.is_superuser:
                raise exceptions.AuthenticationFailed('Sorry, you do not have the permission'
                                                      ' level to perform this action')
            return True
        return True


class GetAdminAndUserPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == "GET":
            authenticated_user = VerifyToken().authenticate(request)
            if authenticated_user.is_superuser:
                return True
            elif not authenticated_user or not str(authenticated_user.id) in request.path:
                raise exceptions.AuthenticationFailed('Sorry, you do not have the permission'
                                                      ' level to perform this action')
        return True

