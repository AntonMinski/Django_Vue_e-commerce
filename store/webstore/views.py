from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
import json

from .models import Setting, ContactForm, ContactMessage
from products.models import Category, Product, Images
from .forms import SearchForm
from user.models import UserProfile
from order.models import ShopCart, ShopCartForm


# category = Category.objects.all()
# setting = Setting.objects.get(pk=1)
# context = {
#     'setting': setting,
#     # 'category': category,
#            }


    # profile = UserProfile.objects.get(user_id=current_user.id)
    # context = {'shop_cart': shop_cart,
    #            'category': category,
    #            'total': int(abs(total)),
    #            'profile': profile
    #            }


def index(request):
    current_user = request.user
    shop_cart = ShopCart.objects.filter(user_id=current_user.id)
    total_price, total_quantity = 0, 0
    for rs in shop_cart:
        total_price += rs.product.price * rs.quantity
        total_quantity += 1

    products_slider = Product.objects.all()
    products_latest = Product.objects.all().order_by('-id')[:4]  # last added 4
    products_picked = Product.objects.all().order_by('?')[:4]  # random 4
    context_index = {
        # 'setting': setting,
        # 'category': category,
        'products_slider': products_slider,
        'products_latest': products_latest,
        'products_picked': products_picked,
        'shop_cart': shop_cart,
        'total_price': total_price,
        'total_quantity': total_quantity,
        'current_user': current_user,
    }
    return render(request, 'index.html', context_index)


def about(request):
    return render(request, 'about.html', context)


class ContactView(View):
    def get(self, request):
        form = ContactForm
        return render(request, 'contact.html', {'form': form})

    def post(self, request):
        if request.method == 'POST':
            form = ContactForm(request.POST)
            if form.is_valid():
                data = ContactMessage()  # create relation with model

                data.name = form.cleaned_data['name']
                data.email = form.cleaned_data['email']
                data.phone = form.cleaned_data['phone']
                data.subject = form.cleaned_data['subject']
                data.product_type = form.cleaned_data['product_type']
                data.message = form.cleaned_data['message']
                data.ip = request.META.get('REMOTE_ADDR')
                data.save()
                message_scs = 'Your message has been sent. We would answer as soon, as possible'
                messages.success(request, message_scs)
                messages_scs = 'Your message has been sent. We would answer as soon, as possible'
                print(messages_scs)
                context = {'form': form,
                           'mess': messages_scs,
                           }
                return render(request, 'contact.html', context)

            return render(request, 'contact.html', {'form': form})


def home(request):
    return HttpResponseRedirect('/')


def category(request, slug):
    products = Product.objects.all()
    print(len(products))
    cat_context = {
        # 'setting': setting,
        # 'category': category,
        'products': products,
    }
    return render(request, 'products/category.html', cat_context)


def search(request):
    if request.method == 'POST':  # check post

        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']  # get form input data
            # SELECT * FROM product WHERE title LIKE '%query%' :
            products = Product.objects.filter(title__icontains=query)
            '''
            catid = form.cleaned_data['catid']
            if catid == 0:
                products = Product.objects.filter(
                    title__icontains=query)  # SELECT * FROM product WHERE title LIKE '%query%'
            else:
                products = Product.objects.filter(title__icontains=query, category_id=catid)
            '''

            # category = Category.objects.all()
            context = {'products': products, 'query': query,
                       }  # 'category': category
            return render(request, 'products/search_products.html', context)

    return HttpResponseRedirect('/')


def search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        products = Product.objects.filter(title__icontains=q)
        results = []
        for rs in products:
            products_json = {}
            products_json = rs.title
            results.append(products_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def product_detail(request, slug):
    # category = Category.objects.all()
    product = Product.objects.get(slug=slug)
    images = Images.objects.filter(product_id=product.id)
    print(len(images))
    # image_id = product.id
    # images = Images.objects.all()

    # comments = Comment.objects.filter(product_i d=id, status="True")
    context = {
        # 'category': category,
        'product': product,
        'images': images,
        # 'comments': comments,
    }
    return render(request, 'products/product_detail.html', context)

    '''
    if product.variant !="None": # Product have variants
        if request.method == 'POST': # if we select color
            variant_id = request.POST.get('variantid')
            variant = Variants.objects.get(id=variant_id) # получить продукт, к которому с формы пришло id="variantid" / selected product by click color radio
            colors = Variants.objects.filter(product_id=id, size_id=variant.size_id )
            sizes = Variants.objects.raw('SELECT * FROM  product_variants  WHERE product_id=%s GROUP BY size_id',[id]) # js language...
            query += variant.title+' Size:' +str(variant.size) +' Color:' +str(variant.color)
        else:
            variants = Variants.objects.filter(product_id=id)
            colors = Variants.objects.filter(product_id=id,size_id=variants[0].size_id )
            sizes = Variants.objects.raw('SELECT * FROM  product_variants  WHERE product_id=%s GROUP BY size_id',[id])
            variant = Variants.objects.get(id=variants[0].id)
        context.update({'sizes': sizes, 'colors': colors,
                        'variant': variant,'query': query
                        })
    '''
    # return render(request, 'products/product_detail.html',context)

