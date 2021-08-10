from datetime import datetime
from django.utils.timesince import timesince
from rest_framework import serializers

from order.models import ShopCart, Order, OrderProduct

class ShopCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShopCart
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = "__all__"


class OrderProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderProduct
        fields = "__all__"








