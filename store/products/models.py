from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from django.urls import reverse

from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.safestring import mark_safe
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

    class Meta:  # для нормального отображения в админке / for good lookup at admin
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


