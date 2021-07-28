from django import forms


from .models import ContactMessage


class SearchForm(forms.Form):
    query = forms.CharField(max_length=100)
    # catid = forms.IntegerField()  # if i want to search by category too


# class ContactForm(forms.ModelForm):
#     class Meta:
#         model = ContactMessage
#         fields = ['name', 'email', 'phone', 'subject', 'product_type',
#                   'message']


class ContactForm(forms.Form):
    name = forms.CharField()
    # message = forms.CharField(widget=forms.Textarea)



