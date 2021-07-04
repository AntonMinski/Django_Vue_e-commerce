from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.forms import ModelForm
from django.urls import reverse
from django.utils.safestring import mark_safe

from ckeditor_uploader.fields import RichTextUploadingField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Category(MPTTModel):
    STATUS = (
        ('True', 'Active'),
        ('False', 'InActive'),
    )
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    # parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    # image = models.ImageField(blank=True, upload_to='images')
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
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # many to one relation with Category
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    image = models.ImageField(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    amount = models.IntegerField(default=0)
    min_amount = models.IntegerField(default=1)
    variant = models.CharField(max_length=10, choices=VARIANTS, default='None')
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
        return reverse('category_detail', kwargs={'slug': self.slug})


class NotebookProduct(Product):
    RAM = (
        (0, '0'),
        (4, '4'),
        (6, '6'),
        (8, '8'),
        (12, '12'),
        (16, '16'),
        (32, '32'),

    )
    processor = models.CharField(max_length=15)
    graphics = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    diagonal = models.FloatField()
    display_resolution = models.CharField(max_length=30)
    ram = models.PositiveIntegerField(choices=RAM, default=4)
    disk_drive = models.CharField(max_length=30)

    screen_condition = models.FloatField()
    case_condition = models.FloatField()
    battery_wear_level = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.category.slug} {self.title}'

    @property
    def fin_price(self):
        return self.price + self.ram


class NotebookProductForm(ModelForm):
    class Meta:
        model = NotebookProduct
        fields = ['ram', 'disk_drive']


class Specification(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'specification for product {self.name}'


class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank=True, upload_to='images/')

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'

    def __str__(self):
        return self.title


class Comment(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
        ('New', 'New'), # need to change to true in AdminPanel frontend to publicate the comment
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


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['subject', 'comment', 'rate', 'email']


