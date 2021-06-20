from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_to_cart/<int:id>', views.add_to_cart, name='add_to_cart'),
    path('del_from_cart/<int:id>', views.del_from_cart,
         name='del_from_cart'),
    path('checkout/', views.checkout, name='checkout'),


]