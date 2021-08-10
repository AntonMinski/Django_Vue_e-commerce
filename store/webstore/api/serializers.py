from rest_framework import serializers

from webstore.models import Setting, ContactMessage


class SettingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Setting
        fields = "__all__"


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = "__all__"



