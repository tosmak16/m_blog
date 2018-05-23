from django.urls import path
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register(r'users', views.UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    path(r'index', views.IndexViewSet.as_view(), name='index'),

]