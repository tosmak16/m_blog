from django.urls import path
from . import views
from django.conf.urls import url, include


urlpatterns = [
    path('', views.index, name='index'),
    url('login', views.UserLogin.as_view(), name='login'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]