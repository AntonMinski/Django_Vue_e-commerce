from datetime import datetime
from django.utils.timesince import timesince
from rest_framework import serializers

from order.models import ShopCart, Order, OrderProduct
from products.api.serializers import ProductSerializer

class ShopCartSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    # product = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ShopCart
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):


    user = serializers.StringRelatedField(read_only=True)
    product = serializers.StringRelatedField(read_only=True)
    order = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = "__all__"


class OrderProductSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = OrderProduct
        fields = "__all__"








