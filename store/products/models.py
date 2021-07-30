from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.forms import ModelForm
from django.utils.safestring import mark_safe
from django.urls import reverse

from ckeditor_uploader.fields import RichTextUploadingField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


def get_product_url(obj, view_name):
    ct_model = obj.__class__._meta.model_name
    return reverse(view_name, kwargs={'ct_model': ct_model,
                                      'slug': obj.slug,
                                      })


class Category(MPTTModel):
    STATUS = (
        ('True', 'Active'),
        ('False', 'InActive'),
    )
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    status = models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField(null=False, unique=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    # для нормального отображения в админке / for good lookup at admin:
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title

    class MPTTMeta:
        order_insertion_by = ['title']

    # def __str__(self):                            # __str__ method elaborated later in
    #     full_path = [self.title]                  # post.  use __unicode__ in place of
    #     k = self.parent
    #     while k is not None:
    #         full_path.append(k.title)
    #         k = k.parent
    #     return ' / '.join(full_path[::-1])

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Product(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )

    VARIANTS = (
        ('None', 'None'),
        ('Size', 'Size'),
        ('Color', 'Color'),
        ('Size-Color', 'Size-Color'),

    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name="products")  # many to one relation with Category;  # related_name used in serializers
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    # description = models.TextField(max_length=255)
    image = models.ImageField(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    amount = models.IntegerField(default=0)
    min_amount = models.IntegerField(default=1)
    # variant = models.CharField(max_length=10, choices=VARIANTS, default='None')
    detail = RichTextUploadingField()
    slug = models.SlugField(null=False, unique=True)
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        else:
            return ""

    image_tag_short_description = 'Image'

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    @property
    def product_url(self):
        return f'{self.__class__._meta.model_name}/{self.slug}'


class NotebookProduct(Product):
    RAM = (
        (0, 'without ram'),
        (350, '4 GB'),
        (450, '6 GB'),
        (750, '8 GB'),
        (1100, '12 GB'),
        (1500, '16 GB'),
        (3000, '32 GB'),
    )
    DRIVE = (
        (0, 'without drive'),
        (100, '160 hdd'),
        (200, '250 hdd'),
        (250, '320 hdd'),
        (300, '500 hdd'),
        (400, '1 tb hdd'),
        (1000, '2 tb hdd'),
        (225, '64 ssd'),
        (600, '128 ssd'),
        (800, '256 ssd'),
        (1400, '512 ssd'),
        (2000, '1 tb ssd'),
        (1200, '128 ssd + 1 tb hdd'),
        (1500, '256 ssd + 1 tb hdd'),
    )
    processor = models.CharField(max_length=15)
    graphics = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    diagonal = models.FloatField()
    display_resolution = models.CharField(max_length=30)
    ram = models.IntegerField(choices=RAM)
    drive = models.IntegerField(choices=DRIVE)
    tech_condition = models.FloatField(default=10.0)
    screen_condition = models.FloatField(default=10.0)
    case_condition = models.FloatField(default=10.0)
    battery_wear_level = models.PositiveIntegerField(default=0)
    tech_description = models.CharField(max_length=50, default='')
    screen_description = models.CharField(max_length=50, default='')
    case_description = models.CharField(max_length=50, default='')

    def __str__(self):
        return f'{self.category.slug} {self.title}'

    def get_absolute_url(self):
        return reverse('notebook_detail', kwargs={'slug': self.slug})

    @property
    def fin_price(self):
        return self.price + self.ram + self.drive

    @property
    def product_url(self):
        return f'{self.__class__._meta.model_name}/{self.slug}'


class Specification(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'specification for product {self.name}'


class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank=True, upload_to='images/')

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'

    def __str__(self):
        return f'{self.pk} {self.title}'


class Comment(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
        ('New', 'New'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, blank=True)
    email = models.CharField(max_length=50, blank=True)
    comment = models.CharField(max_length=250, blank=True)
    rate = models.IntegerField(default=5)
    ip = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class LatestProductsManager(models.Model):

    @staticmethod
    def get_products_for_main_page(*args, **kwargs):
        with_respect_to = kwargs.get('with_respect_to')
        products = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.order_by(
                '-id')[2]
            products.extend(model_products)
        if with_respect_to:
            ct_model = ContentType.objects.filter(model=with_respect_to)
            if ct_model.exists():
                if with_respect_to in args:
                    return sorted(products,
                                  key=lambda
                                      x: x.__class__._meta.model_name.
                                  startswith(with_respect_to), reverse=True
                                  )
        return products


class LatestProducts(models.Model):
    object = LatestProductsManager()


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['subject', 'comment', 'rate', 'email']
