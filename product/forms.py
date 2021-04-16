from django.forms import ModelForm, modelformset_factory
from django import forms
from product.models import Product, ProductType


class ProductForm(ModelForm):
    class Meta:
        model = Product

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name...'}),
            'ref': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'REF...'}),
            'desc': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Desc...'}),
            'category': forms.Select(attrs={'class': 'form-control '}),
            'stock': forms.Select(attrs={'class': 'form-control '}),
            'image': forms.FileInput(attrs={'class': 'form-control-file', 'placeholder': 'Image...'}),
            # 'price1': forms.NumberInput(attrs={'class': 'form-control ', 'onkeyup': 'fill_prices()'}),
            # 'price2': forms.NumberInput(attrs={'class': 'form-control '}),
            # 'price3': forms.NumberInput(attrs={'class': 'form-control '}),
            # 'price4': forms.NumberInput(attrs={'class': 'form-control '}),
            # 'price5': forms.NumberInput(attrs={'class': 'form-control '}),
            # 'price6': forms.NumberInput(attrs={'class': 'form-control '}),
            'alert_quantity': forms.NumberInput(attrs={'class': 'form-control '}),
            'box_quantity': forms.NumberInput(attrs={'class': 'form-control '}),
            'weight': forms.NumberInput(attrs={'class': 'form-control '}),

        }

        fields = ['category', 'name', 'ref', 'desc', 'image', 'stock', 'buyprice', 'alert_quantity', 'box_quantity',
                  'weight']


ProductTypeFormset = modelformset_factory(
    ProductType,
    widgets={'price1': forms.NumberInput(attrs={'class': 'form-control ', 'onkeyup': 'fill_prices()'})},
    fields=('name', 'price1', 'price2', 'price3', 'price4', 'price5', 'price6'),
    extra=1,
)
