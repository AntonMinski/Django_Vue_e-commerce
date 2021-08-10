from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, viewsets

from order.models import ShopCart, Order, OrderProduct
from .serializers import ShopCartSerializer, OrderSerializer, \
    OrderProductSerializer


class ShopCartViewSet(viewsets.ModelViewSet):
    queryset = ShopCart.objects.all()
    serializer_class = ShopCartSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class OrderProductViewSet(viewsets.ModelViewSet):
    queryset = OrderProduct.objects.all()
    serializer_class = OrderProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]