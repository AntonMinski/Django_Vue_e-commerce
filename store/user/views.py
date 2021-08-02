import random
import string
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import View
from django.core.mail import send_mail



from .models import UserProfile
from products.models import Category, Product, Images  # Comment
from order.models import ShopCart, Order, OrderProduct
from .forms import SignUpForm, UserUpdateForm, ProfileUpdateForm
# from order.models import Order, OrderProduct


# category = Category.objects.all()


@login_required(login_url='/login')  # Check login
def index(request):
    current_user = request.user
    shop_cart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shop_cart:
        total += rs.product.price * rs.quantity
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'shop_cart': shop_cart,
               'total': int(abs(total)),
               'profile': profile
               }
    return render(request, 'user/user_profile.html', context)


def logout_func(request):
    logout(request)
    return HttpResponseRedirect('/')


def login_form(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            current_user = request.user
            print(current_user.id)
            print(current_user.username)
            # userprofile = UserProfile.objects.get(user_id=current_user.id)
            # request.session['userimage'] = userprofile.image.url
            return HttpResponseRedirect('/')  # redirect to success page
        else:
            messages.warning(request, "Login Error !! Username or Password is incorrect")
            return HttpResponseRedirect('/login_form')

    return render(request, 'user/login.html')  # {'category': category}


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()  # completed sign up
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            # Create data in profile table for user
            current_user = request.user
            data = UserProfile()
            data.user_id = current_user.id
            data.image = "images/users/Sample_User_Icon.png"
            data.save()
            messages.success(request, 'Your account has been created!')

            return HttpResponseRedirect('/')
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect('/signup')

    form = SignUpForm()
    context = {
        'form': form
    }

    return render(request, 'user/signup.html', context)


@login_required(login_url='/login')  # Check login
def user_update(request):
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    if request.method == 'POST':
        # request.user is user data:
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES,
                                         instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated!')
            return HttpResponseRedirect('/user')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(
            instance=request.user.userprofile)
        context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'profile': profile,
        }
        return render(request, 'user/user_update.html', context)


@login_required(login_url='/login')  # Check login
def user_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # importanta part; need to logout without it
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect('/user')
        else:
            messages.error(request, 'Please correct the error below.<br>'
                           + str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        form = PasswordChangeForm(request.user, request.POST)
        context = {
            'form': form,
        }
        return render(request, 'user/user_password.html', context)


# @login_required(login_url='/user/login_form')
def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            new_password = "".join(random.sample(string.printable, 10))
            user_email = form.cleaned_data['email']
            # print(f':{new_password}:')
            # print(user_email)
            try:
                user = User.objects.get(email=user_email)
                user.set_password(new_password)
                user.save()
                send_mail(
                    subject='Password change',
                    message=f'Here is your new password:{new_password}',
                    from_email='anton_minski5@ukr.net',
                    recipient_list=[user_email])
                messages.success(request, f'New password has been sent to {user_email}. '
                                          f'Now, You can login and change it')
                return HttpResponseRedirect('/login_form')
            except User.DoesNotExist:
                messages.error(request, 'no such email in system, please try again')
    form = PasswordResetForm
    context = {
            'form': form,
        }
    return render(request, 'user/user_password_reset.html', context)


@login_required(login_url='/login')  # Check login
def user_orders(request):
    current_user = request.user
    orders = Order.objects.filter(user_id=current_user.id)
    context = {  # 'category': category,
               'orders': orders
               }
    return render(request, 'user/user_orders.html', context)


@login_required(login_url='/login')  # Check login
def user_order_detail(request, id):
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id,
                              id=id)
    # to prevent from other users)
    order_items = OrderProduct.objects.filter(order_id=id)
    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'user/order_detail.html', context)


@login_required(login_url='/login')  # Check login
def user_order_product(request):
    current_user = request.user
    order_product = OrderProduct.objects.filter(
        user_id=current_user.id).order_by('-id')
    context = {'order_product': order_product,}
    return render(request, 'user/order_products.html', context)


@login_required(login_url='/login')  # Check login
def user_order_product_detail(request, id, oid):
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=oid)
    order_items = OrderProduct.objects.filter(id=id, user_id=current_user.id)
    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'user/order_product_detail.html', context)

