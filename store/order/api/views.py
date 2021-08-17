from rest_framework.viewsets import ModelViewSet
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly

from order.models import ShopCart, Order, OrderProduct
from .serializers import ShopCartSerializer, OrderSerializer, \
    OrderProductSerializer
from user.api.permissions import IsOwner


class ShopCartViewSet(viewsets.ModelViewSet):
    queryset = ShopCart.objects.all()
    serializer_class = ShopCartSerializer
    permission_classes = [IsOwner or IsAdminUser]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsOwner or IsAdminUser]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class OrderProductViewSet(viewsets.ModelViewSet):
    queryset = OrderProduct.objects.all()
    serializer_class = OrderProductSerializer
    permission_classes = [IsOwner or IsAdminUser]