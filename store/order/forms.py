from django.forms import ModelForm
from .models import Order, ShopCart


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'phone']


class ShopCartForm(ModelForm):
    class Meta:
        model = ShopCart
        fields = ['quantity']
