from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import UserProfile


from products.models import Category, Product, Images  # Comment
from order.models import ShopCart, ShopCartForm

from .forms import SignUpForm
# from order.models import Order, OrderProduct
category = Category.objects.all()



@login_required(login_url='/login')  # Check login
def index(request):
    current_user = request.user
    shop_cart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shop_cart:
        total += rs.product.price * rs.quantity

    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'shop_cart': shop_cart,
               'category': category,
               'total': int(abs(total)),
               'profile': profile
               }
    return render(request, 'user/user_profile.html', context)


def logout_func(request):
    logout(request)
    # if translation.LANGUAGE_SESSION_KEY in request.session:
    # del request.session[translation.LANGUAGE_SESSION_KEY]
    # del request.session['currency']
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
            return HttpResponseRedirect('/')

    return render(request, 'login.html', {'category': category})


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
        'category': category,
        'form': form
    }

    return render(request, 'signup.html', context)

"""

def log_reg(request):
    if request.method == 'POST':
        username = request.POST['login']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            current_user = request.user
            try:
                request.session['userimage'] = current_user.image.url
            except:
                pass
            return HttpResponseRedirect('/')  # redirect to success page
        else:
            messages.warning(request, "Login Error !! Username or Password is incorrect")
            return HttpResponseRedirect('/log_reg')


    return render(request, 'log-reg.html')

def log_reg(request):
    if request.method == 'POST':
        username = request.POST['login']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            current_user = request.user
            userprofile = UserProfile.objects.get(user_id=current_user.id)
            request.session['userimage'] = userprofile.image.url
            return HttpResponseRedirect('/')  # redirect to success page
        else:
            messages.warning(request, "Login Error !! Username or Password is incorrect")
            return HttpResponseRedirect('/log_reg')

    return render(request, 'log-reg.html')

def sign_up(request):
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
            data.image = "images/users/user.png"
            data.save()
            messages.success(request, 'Your account has been created!')
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect('/signup')

    form = SignUpForm()

    return render(request, 'user/signup_form.html', {'form': form})

def logout_func(request):
    logout(request)
    # if translation.LANGUAGE_SESSION_KEY in request.session:
    # del request.session[translation.LANGUAGE_SESSION_KEY]
    # del request.session['currency']
    return HttpResponseRedirect('/')


@login_required(login_url='/login')  # Check login
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)  # request.user is user  data
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated!')
            return HttpResponseRedirect('/user')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(
            instance=request.user.userprofile)  # "userprofile" model -> OneToOneField relatinon with user
        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, 'user/user_update.html', context)


@login_required(login_url='/login')  # Check login
def user_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect('/user')
        else:
            messages.error(request, 'Please correct the error below.<br>' + str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        form = PasswordChangeForm(request.user)
        return render(request, 'user/user_password.html', {'form': form})


@login_required(login_url='/login')  # Check login
def user_orders(request):
    current_user = request.user
    orders = Order.objects.filter(user_id=current_user.id)
    context = {
               'orders': orders,
               }
    return render(request, 'user/user_orders.html', context)


@login_required(login_url='/login')  # Check login
def user_orderdetail(request, id):
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id,
                              id=id)  # чтобы другие пользователи не увидели заказ, вбив в браузере / to prevent from other users
    orderitems = OrderProduct.objects.filter(order_id=id)
    context = {
        'order': order,
        'orderitems': orderitems,
    }
    return render(request, 'user/user_order_detail.html', context)


@login_required(login_url='/login')  # Check login
def user_order_product(request):
    current_user = request.user
    order_product = OrderProduct.objects.filter(user_id=current_user.id).order_by('-id')
    context = {
               'order_product': order_product,
               }
    return render(request, 'user/user_order_products.html', context)


@login_required(login_url='/login')  # Check login
def user_order_product_detail(request, id, oid):
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=oid)
    orderitems = OrderProduct.objects.filter(id=id, user_id=current_user.id)
    context = {
        'order': order,
        'orderitems': orderitems,
    }
    return render(request, 'user/user_order_detail.html', context)


def user_comments(request):
    current_user = request.user
    comments = Comment.objects.filter(user_id=current_user.id)
    context = {
        'comments': comments,
    }
    return render(request, 'user/user_comments.html', context)


@login_required(login_url='/login')  # Check login
def user_deletecomment(request, id):
    current_user = request.user
    Comment.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Comment deleted..')
    return HttpResponseRedirect('/user/comments')
"""
