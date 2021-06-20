from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json

from products.models import Category, Product, Images
from .models import ShopCart, ShopCartForm


# Create your views here.
def index(request):
    return HttpResponse('order page')

@login_required(login_url='/login') # Check login
def add_to_cart(request, id):
    url = request.META.get('HTTP_REFERER')  # get last url
    current_user = request.user  # Access User Session information
    product = Product.objects.get(pk=id)

    # Check product in ShopCart
    check_in_product = ShopCart.objects.filter(product_id=product.id)
    if check_in_product:
        control = 1  # The product is in the cart
    else:
        control = 0  # The product is not in the cart"""

    if request.method == 'POST':  # if there is a post
        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control == 1:  # Update  ShopCart
                data = ShopCart.objects.get(product_id=product.id)
                data.quantity += form.cleaned_data['quantity']
                data.save()  # save data
            else:  # Insert to ShopCart
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id = id
                data.quantity = form.cleaned_data['quantity']
                data.save()
        messages.success(request, "Product added to ShopCart")
        return HttpResponseRedirect(url)

    else:  # if there is no post
        if control == 1:  # Update  ShopCart
            data = ShopCart.objects.get(product_id=product.id)
            data.quantity += 1
            data.save()  #
        else:  # Insert to ShopCart
            data = ShopCart()  # model ile bağlantı kur
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            data.save()  #
        messages.success(request, "Product added to ShopCart")
        return HttpResponseRedirect(url)

def shopcart(request):
    category = Category.objects.all()
    current_user = request.user  # Access User Session information
    shop_cart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shop_cart:
        total += rs.product.price * rs.quantity
    print(total)
    #return HttpResponse(str(total))
    context = {'shop_cart': shop_cart,
               'category': category,
               'total': int(abs(total)),
               }
    return render(request, 'cart_products.html', context)


@login_required(login_url='/login')  # Check login
def del_from_cart(request, id):
    ShopCart.objects.filter(id=id).delete()

    messages.success(request, "Your item deleted form cart.")
    return HttpResponseRedirect("/shopcart")
