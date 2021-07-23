from django import forms
from django.forms import TextInput, EmailInput, Select, FileInput

from .models import NotebookProduct


class NotebookProductForm(forms.ModelForm):
    class Meta:
        model = NotebookProduct
        fields = ['ram', 'drive']