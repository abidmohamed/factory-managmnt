from django.forms import ModelForm
from django import forms

from category.models import Category
from family.models import Family


class CategoryForm(ModelForm):
    class Meta:
        model = Category

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name...'}),
            'family': forms.Select(attrs={'class': 'form-control '}),
            'image': forms.FileInput(attrs={'class': 'form-control-file', 'placeholder': 'Image...'}),

        }

        fields = ['family', 'name', 'image', ]
