from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
                                        BaseUserManager)
from django.utils import timezone
from django.contrib.auth.hashers import make_password


class UserManager(BaseUserManager):

    def create_user(self, email, username, display_name=None, password=None):

        if email is None:
            raise ValueError("Email is required")

        if not display_name:
            display_name = username

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            display_name=display_name,
            password=make_password(password))
        user.save()
        return user

    def create_superuser(self, email, username, display_name=None, password=None):

        user = self.create_user(email, username, display_name,password)
        user.is_staff = True
        user.is_superuser = True
        user.save
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=40, unique=True)
    display_name = models.CharField(max_length=100)
    phone_number = models.IntegerField(blank=True, default=0)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return f'@{self.username}'

    def get_short_name(self):
        return self.display_name

    def get_long_name(self):
        return f'{self.username} @{self.display_name}'







