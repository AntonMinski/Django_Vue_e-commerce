from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm

from products.models import Product


class ShopCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    # variant = models.ForeignKey(Variants, on_delete=models.SET_NULL,
    # blank=True, null=True) # relation with varinat

    def __str__(self):
        return self.product.title

    @property  # получить цену продукта / this decorator returns it price
    def price(self):
        return self.product.price

    @property  # подсчитать цену за количество / calculate final price
    def total_price(self):
        return self.quantity * self.product.price

    # @property
    # def varamount(self):
    #     return self.quantity * self.variant.price


class ShopCartForm(ModelForm):
    class Meta:
        model = ShopCart
        fields = ['quantity']


class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Preparing', 'Preparing'),
        ('Shipped', 'Shipped'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    code = models.CharField(max_length=5, editable=False )
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone = models.CharField(blank=True, max_length=20)
    address = models.CharField(blank=True, max_length=150)
    city = models.CharField(blank=True, max_length=30)
    country = models.CharField(blank=True, max_length=30)
    total = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    admin_note = models.CharField(blank=True, max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'address', 'phone', 'city',
                  'country']


class OrderProduct(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Canceled', 'Canceled'),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # variant = models.ForeignKey(Variants, on_delete=models.SET_NULL,
    # blank=True, null=True)  # relation with varinat
    quantity = models.IntegerField()
    price = models.FloatField()
    amount = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.title
