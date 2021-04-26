from django.forms import ModelForm
from django import forms

from category.models import Category


class CategoryForm(ModelForm):
    class Meta:
        model = Category

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name...'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file', 'placeholder': 'Image...'}),

        }

        fields = ['name', 'image', ]
