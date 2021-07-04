from django.db import models

# Create your models here.
from django.db import models

# Create your models here.

from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.forms import ModelForm, TextInput, Textarea


class Setting(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    company = models.CharField(max_length=50)
    address = models.CharField(blank=True, max_length=100)
    phone = models.CharField(blank=True, max_length=50)
    fax = models.CharField(blank=True, max_length=15)
    email = models.CharField(blank=True, max_length=50)
    smtp_server = models.CharField(blank=True, max_length=50)
    smtp_email = models.CharField(blank=True, max_length=50)
    smtp_password = models.CharField(blank=True, max_length=10)
    smtp_port = models.CharField(blank=True, max_length=5)
    icon = models.ImageField(blank=True, upload_to='images/')
    facebook = models.CharField(blank=True, max_length=50)
    instagram = models.CharField(blank=True, max_length=50)
    twitter = models.CharField(blank=True, max_length=50)
    youtube = models.CharField(blank=True, max_length=50)
    about = RichTextUploadingField(blank=True)
    contact = RichTextUploadingField(blank=True)
    references = RichTextUploadingField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Read', 'Read'),
        ('Closed', 'Closed'),
    )
    SUBJECT = (
        ('Not_selected', '-- Select One --'),
        ('Product', 'Product'),
        ('General', 'General'),
        ('Appeal', 'Appeal'),
        ('Сooperation', 'Сooperation'),
    )
    name = models.CharField(null=True, blank=True, max_length=35)
    email = models.CharField(blank=True, max_length=35, null=True)
    phone = models.IntegerField(blank=True, null=True, default=0)
    subject = models.CharField(max_length=50, choices=SUBJECT)
    product_type = models.CharField(blank=True, null=True, max_length=80)
    message = models.TextField(blank=False, null=False, max_length=600)
    status = models.CharField(max_length=10, choices=STATUS)
    ip = models.CharField(blank=True, max_length=20)
    note = models.CharField(blank=True, max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.name == None:
            self.name = '-'
        return self.name

    def short_message(self):
        if len(self.message) > 15:
            self.message = self.message[0:15] + ' ...'
        return self.message


class ContactForm(ModelForm):  # general type
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'product_type', 'message']
        '''
        widgets = {
            'name': TextInput(attrs={
                # 'class': 'sm-form-control',
                # 'for': 'template-contactform-name',
                # 'id': 'template-contactform-name',
                # 'name': 'template-contactform-name',  # тут еще вопрос будет
                'type': 'text',
                'placeholder': 'Name & Surname',
            }),
            'email': TextInput(attrs={
                # 'class': 'sm-form-control',
                # 'for ': 'template-contactform-email',
                # 'id': 'template-contactform-email',
                'type': 'email',
                'placeholder': 'Email Address'
                                }),
            'phone': TextInput(attrs={'class': 'sm-form-control', 'placeholder': 'Phone / Messenger'}),
            'subject': TextInput(attrs={'class': 'sm-form-control', 'placeholder': '-- Select One --'}),
            'product_type': TextInput(attrs={'class': 'sm-form-control', 'placeholder': 'Product / Complectation'}),
            'message': Textarea(attrs={'class': 'required sm-form-control', 'placeholder': 'Your Message', 'rows': '15'}),
        }











        def save(self):
            data = ContactMessage(
                name=self.cleaned_data['name'],
                email=self.cleaned_data['email'],
                phone=self.cleaned_data['phone'],
                subject=self.cleaned_data['subject'],
                product_type=self.cleaned_data['product_type'],
                message=self.cleaned_data['message'],
                )
            return data
        '''

