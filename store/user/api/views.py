from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_condition import Or

from user.models import UserProfile
from .serializers import UserProfileSerializer, UserSerializer
from .permissions import IsOwner


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsOwner or IsAdminUser]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

