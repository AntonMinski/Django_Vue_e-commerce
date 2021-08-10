from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'shopcart', views.ShopCartViewSet)
router.register(r'order', views.OrderViewSet)
router.register(r'order_product', views.OrderProductViewSet)

shopcart_list = views.ShopCartViewSet.as_view({'get': 'list'})
shopcart_detail = views.ShopCartViewSet.as_view({'get': 'retrieve'})

order_list = views.OrderViewSet.as_view({'get': 'list'})
order_detail = views.OrderViewSet.as_view({'get': 'retrieve'})

order_product_list = views.OrderProductViewSet.as_view({'get': 'list'})
order_product_detail = views.OrderProductViewSet.as_view({'get': 'retrieve'})


urlpatterns = [
    path('', include (router.urls)),
]

