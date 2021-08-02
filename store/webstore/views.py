from itertools import chain

from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import View, DetailView, UpdateView, FormView, CreateView
import json


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

    # def get_success_message(self, cleaned_data):
    #     return self.success_message % dict(
    #         cleaned_data,
    #         calculated_field=self.object.calculated_field,
    #     )
#
#
#     # form_class = ContactForm
#     # template_name = 'contact.html'
#     # success_url = '/'
#
#     # def form_valid(self, form):
#     #     # reverse_lazy
#     #     print(form.cleaned_data)
#     #     return super().form_valid(form)
#
#     # def post(self, request):
#     #     if request.method == 'POST':
#     #         form = ContactForm(request.POST)
#     #         if form.is_valid():
#     #             data = ContactMessage()  # create relation with model
#     #
#     #             data.name = form.cleaned_data['name']
#     #             data.email = form.cleaned_data['email']
#     #             data.phone = form.cleaned_data['phone']
#     #             data.subject = form.cleaned_data['subject']
#     #             data.product_type = form.cleaned_data['product_type']
#     #             data.message = form.cleaned_data['message']
#     #             data.ip = request.META.get('REMOTE_ADDR')
#     #             data.save()
#     #             message_scs = 'Your message has been sent. We would answer as soon, as possible'
#     #             messages.success(request, message_scs)
#     #             messages_scs = 'Your message has been sent. We would answer as soon, as possible'
#     #             print(messages_scs)
#     #             context = {'form': form,
#     #                        'mess': messages_scs,
#     #                        }
#     #             return render(request, 'contact.html', context)
#     #
#     #         return render(request, 'contact.html', {'form': form})


# class ContactView(View):
#     template_name = 'contact.html'
#     form_class = ContactForm
#     success_url = '/thanks/'
#
#
#     def get(self, request):
#         form = ContactForm
#         return render(request, 'contact.html', {'form': form})
#
#     def post(self, request):
#         if request.method == 'POST':
#             form = ContactForm(request.POST)
#             if form.is_valid():
#                 data = ContactMessage()  # create relation with model
#
#                 data.name = form.cleaned_data['name']
#                 data.email = form.cleaned_data['email']
#                 data.phone = form.cleaned_data['phone']
#                 data.subject = form.cleaned_data['subject']
#                 data.product_type = form.cleaned_data['product_type']
#                 data.message = form.cleaned_data['message']
#                 data.ip = request.META.get('REMOTE_ADDR')
#                 data.save()
#                 message_scs = 'Your message has been sent. We would answer as soon, as possible'
#                 messages.success(request, message_scs)
#                 messages_scs = 'Your message has been sent. We would answer as soon, as possible'
#                 print(messages_scs)
#                 context = {'form': form,
#                            'mess': messages_scs,
#                            }
#                 return render(request, 'contact.html', context)
#
#             return render(request, 'contact.html', {'form': form})
#

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
            context = {'products': products,
                       'query': query,
                       }
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
class ProductView2(DetailView):
    model = Product
    template_name = 'products/products_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['slug']
        product = Product.objects.get(slug=slug)
        context['product'] = product
        context['images'] = Images.objects.filter(product_id=product.id)

        return context


# изначальный колхозный вариант
class ProductView(DetailView):

    def get(self, request, slug):
        product = Product.objects.get(slug=slug)
        images = Images.objects.filter(product_id=product.id)
        form = ContactForm
        context = {
            'product': product,
            'images': images,
            'form': form,
        }
        return render(request, 'products/products_detail.html', context)


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
        reverse_lazy
        print(form.cleaned_data)
        return super().form_valid(form)


#старый вариант, лишние поля, чуток колхоз:

# class NotebookView_old(UpdateView):
#
#     def get(self, request, slug):
#         product = NotebookProduct.objects.get(slug=slug)
#         images = Images.objects.filter(product_id=product.id)
#         form = ContactForm
#         context = {
#             'product': product,
#             'images': images,
#             'form': form,
#         }
#         return render(request, 'products/notebook_product_detail.html', context)
#
#     model = NotebookProduct
#     form_class = NotebookProductForm
#     template_name = 'products/product_detail_old.html'
#
#     def form_valid(self, form):
#         reverse_lazy
#         print(form.cleaned_data)
#         return super().form_valid(form)
#
#
#     #
#     #
#     # product = NotebookProduct.objects.get(slug=slug)
#     # images = Images.objects.filter(product_id=product.id)
#     # form = ContactForm
#     # context = {
#     #     'product': product,
#     #     'images': images,
#     #     'form': form,
#     # }
#     # return render(request, 'products/product_detail_old.html', context)























# class ProductDetailView(UpdateView):
#
#     CT_MODEL_MODEL_CLASS = {
#         'product': Product,
#         'notebookproduct': NotebookProduct,
#     }
#
#     def dispatch(self, request, slug, *args, **kwargs, ):
#         self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
#         product = self.model.objects.get(slug=slug)
#         images = Images.objects.filter(product_id=product.id)
#         form = ContactForm
#         context = {
#             'product': product,
#             'images': images,
#             'form': form,
#         }
#         return render(request, 'products/product_detail_old.html', context)
#
#         # self.queryset = self.model._base_manager.all()
#         # return super().dispatch(request, *args, **kwargs)
#
#     # model = Model
#     # queryset = Model.objects.all()
#     context_object_name = 'product'
#     template_name = 'products/product_detail_old.html'
#     slug_url_kwarg = 'slug'
#     form_class = NotebookProductForm
#     category = Category.objects.all()
#
#     def form_valid(self, form):
#
#         reverse_lazy
#         print(form.cleaned_data)
#         return super().form_valid(form)




# def product_detail(request, slug):

    # image_id = product.id
    # images = Images.objects.all()


    # def post(self, request, slug):
    #     if request.method == 'POST':
    #         form = ContactForm(request.POST)
    #         if form.is_valid():
    #             data = ContactMessage()  # create relation with model
    #
    #             data.name = form.cleaned_data['name']
    #             data.email = form.cleaned_data['email']
    #             data.phone = form.cleaned_data['phone']
    # def form_valid(self, form):
    #     product = NotebookProduct.objects.get(slug=slug)
    #     images = Images.objects.filter(product_id=product.id)
    #     form = ContactForm
    #     context = {
    #         'product': product,
    #         'images': images,
    #         'form': form,
    #     }
    #     return render('products/product_detail_old.html', context)
    #
    #         context = {
    #             'product': product,
    #             'images': images,
    #             'form': form,
    #         }
    #         return render(request, 'products/product_detail_old.html', context)


