from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json

from django.utils.crypto import get_random_string
from user.models import UserProfile

from products.models import Category, Product, Images
from .models import ShopCart, ShopCartForm, OrderForm, Order, OrderProduct


category = Category.objects.all()


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
               'total': round(total),
               }
    return render(request, 'order/cart_products.html', context)


@login_required(login_url='/login')  # Check login
def del_from_cart(request, id):
    ShopCart.objects.filter(id=id).delete()

    messages.success(request, "Your item deleted form cart.")
    return HttpResponseRedirect("/shopcart")


def checkout(request):
    category = Category.objects.all()
    current_user = request.user  # Access User Session information
    shop_cart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    order_total = 0
    for rs in shop_cart:
        total += rs.product.price * rs.quantity

    if request.method == 'POST':  # if there is a post
        form = OrderForm(request.POST)
        # return HttpResponse(request.POST.items())
        if form.is_valid():
            # Send Credit card to bank,  If the bank responds ok, continue,
            # if not, show the error
            # ..............
            data = Order()
            # get product quantity from form:
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.email = form.cleaned_data['email']
            data.address = form.cleaned_data['address']
            data.phone = form.cleaned_data['phone']
            data.user_id = current_user.id
            data.total = total
            data.ip = request.META.get('REMOTE_ADDR')
            order_code = get_random_string(5).upper()
            data.code = order_code  # random code
            data.save()

            for rs in shop_cart:
                detail = OrderProduct()
                detail.order_id = data.id  # Order Id
                detail.product_id = rs.product_id
                detail.user_id = current_user.id
                detail.quantity = rs.quantity
                detail.price = rs.price
                detail.total_price = rs.total_price
                detail.amount = rs.quantity
                detail.save()
                # ***Reduce quantity of sold product from Amount of Product:
                product = Product.objects.get(id=rs.product_id)
                product.amount -= rs.quantity
                product.save()

            # Clear & Delete shop_cart:
            ShopCart.objects.filter(user_id=current_user.id).delete()
            request.session['cart_items'] = 0
            messages.success(request,
                             "Your Order has been completed. Thank you ")
            context = {'order_code': order_code,
                       'category': category,
                       }
            return render(request, 'order/order_completed.html', context
                          )
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect('/order/checkout')

    form = OrderForm()
    shop_cart = ShopCart.objects.filter(user_id=current_user.id)
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'shop_cart': shop_cart,
               'category': category,
               'total': round(total),
               'profile': profile,
               'form': form,
               }
    return render(request, 'order/checkout.html', context)
