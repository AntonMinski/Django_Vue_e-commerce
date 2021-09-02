import json

from itertools import chain

from django.http import HttpResponse
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import View, DetailView, UpdateView, FormView, CreateView


from .models import Setting, ContactMessage
from .forms import SearchForm, ContactForm
from products.models import Category, Product, Images, NotebookProduct
from products.forms import NotebookProductForm
from user.models import UserProfile
from order.models import ShopCart, Order
from order.forms import OrderForm, ShopCartForm


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def choose_laptop(request):
    return render(request, 'choose_laptop.html')


def contact_info(request):
    return render(request, 'contact_info.html')


def faq(request):
    return render(request, 'faq.html')


class ContactView(CreateView):
    model = ContactMessage
    fields = ['name', 'email', 'phone', 'subject', 'product_type',
                  'message']
    template_name = 'contact.html'
    success_url = '/contact/'
    success_message = 'your question has been sent'

    def form_valid(self, form):
        reverse_lazy
        form.instance.created_by = self.request.user
        print(form.cleaned_data)
        messages.success(self.request, 'Your message has been sent. We would answer as soon, as possible')
        return super().form_valid(form)


def home(request):
    return HttpResponseRedirect('/')


def shop(request):
    category_list = Category.objects.all()
    context = {'category_list': category_list}
    return render(request, 'products/shop.html', context)


def category(request, slug):
    category_current = Category.objects.get(slug=slug)
    notebook_products = NotebookProduct.objects.filter(category=category_current.id)
    category_products = Product.objects.filter(category=category_current.id)
    category_products = category_products.exclude(pk__in=notebook_products)

    context = {
        'notebook_products': notebook_products,
        'category_current': category_current,
        'category_products': category_products,
    }
    return render(request, 'products/category.html', context)


def search_result(request):

    if request.method == 'POST':

        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            products = Product.objects.filter(title__icontains=query)
            context = {'products': products,
                       'query': query,
                       }
            return render(request, 'search_result.html', context)

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


# вариант на функциях:
def productFunc(request, slug):
    product = Product.objects.get(slug=slug)
    images = Images.objects.filter(product_id=product.id)
    form = ContactForm
    context = {
        'product': product,
        'images': images,
        'form': form,
    }
    return render(request, 'products/products_detail.html', context)


# вариант на чистом DetalView
class ProductView(DetailView):
    model = Product
    template_name = 'products/products_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['slug']
        product = Product.objects.get(slug=slug)
        context['product'] = product
        context['images'] = Images.objects.filter(product_id=product.id)

        return context


class NotebookView(UpdateView):
    model = NotebookProduct
    form_class = NotebookProductForm
    template_name = 'products/notebook_product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['slug']
        product = NotebookProduct.objects.get(slug=slug)
        context['product'] = product
        context['images'] = Images.objects.filter(product_id=product.id)
        context['basic_template'] = 'products/products_detail.html'

        return context

    def form_valid(self, form):
        request = super().get_context_data(request)
        data = json.loads(request.body)
        product.ram = data['ram']
        product.drive = data['drive']
        print(product, data)
        product.save()
        reverse_lazy
        print(form.cleaned_data)
        return super().form_valid(form)

class NotebookView2(DetailView):
    model = NotebookProduct
    template_name = 'products/notebook_product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['slug']
        product = NotebookProduct.objects.get(slug=slug)
        context['product'] = product
        context['images'] = Images.objects.filter(product_id=product.id)
        context['basic_template'] = 'products/products_detail.html'

        return context


def submit_form_laptop(request, slug):

    if request.method == "POST":
        product = NotebookProduct.objects.get(slug=slug)

        data = json.loads(request.body)
        print(data, product, slug)
        product.ram = data['ram']
        product.drive = data['drive']
        product.save()

        return JsonResponse({'status': 200, 'data': 'abc' })




