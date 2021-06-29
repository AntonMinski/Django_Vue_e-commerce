from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('update/', views.user_update, name='user_update'),
    path('password/', views.user_password, name='user_password'),
    path('orders/', views.user_orders, name='orders'),
    path('order_detail/<int:id>', views.user_order_detail, name='order_detail'),
    path('order_product/', views.user_order_product, name='order_product'),
    path('order_product_detail/<int:id>/<int:oid>',
         views.user_order_product_detail, name='order_product_detail'),

]



