from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, viewsets

from user.models import UserProfile
from .serializers import UserProfileSerializer, UserSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAdminUser]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

