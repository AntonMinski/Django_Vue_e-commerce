from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, viewsets

from webstore.models import Setting, ContactMessage
from .serializers import SettingSerializer, ContactMessageSerializer


class SettingViewSet(viewsets.ModelViewSet):
    queryset = Setting.objects.all()
    serializer_class = SettingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ContactMessageViewSet(viewsets.ModelViewSet):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [permissions.IsAdminUser]







