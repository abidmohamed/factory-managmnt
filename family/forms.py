from django.forms import ModelForm
from django import forms
from family.models import Family


class FamilyForm(ModelForm):
    class Meta:
        model = Family

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name...'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file', 'placeholder': 'Image...'}),
        }

        fields = ['name', 'image', ]
