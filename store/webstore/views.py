from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View

from .models import Setting, ContactForm, ContactMessage
from products.models import Category, Product


category = Category.objects.all()
setting = Setting.objects.get(pk=1)
context = {
    'setting': setting,
    'category': category,
           }

def index(request):
    # setting = Setting.objects.get(pk=1)
    # context = {'setting': setting}
    products_slider = Product.objects.all().order_by('id')[:4]  # first 4
    products_latest = Product.objects.all().order_by('-id')[:4]  # last added 4
    products_picked = Product.objects.all().order_by('?')[:4]  # random 4
    context_index = {
        'setting': setting,
        'category': category,
        'products_slider': products_slider,
        'products_latest': products_latest,
        'products_picked': products_picked,
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

def category(request, id, slug):
    products = Product.objects.filter(category_id=id)
    return HttpResponse(products)
    # return render(request, '.html', context)

