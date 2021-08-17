from datetime import datetime
from django.utils.timesince import timesince
from django.contrib.auth.models import User
from rest_framework import serializers


from user.models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = UserProfile
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']












