from django.forms import ModelForm, modelformset_factory
from buyorder.models import BuyOrder, BuyOrderItem
from product.models import ProductType, Product
from django import forms
from dal import autocomplete


class BuyOrderForm(ModelForm):
    class Meta:
        model = BuyOrder

        fields = ['supplier', ]


# create a form and put it in a formset so you can control some fields property and init the form
class BuyOrderItemForm(forms.ModelForm):
    class Meta:
        model = BuyOrderItem
        product = forms.ModelChoiceField(queryset=Product.objects.all(),
                                         widget=autocomplete.ModelSelect2(url='autocomplete_product'))
        widgets = {
            'product': forms.Select(attrs={'class': 'chosen form-control'}),
            # forms.TextInput(attrs={'class': 'form-control product_name'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
        }

        fields = ['product', 'quantity', 'price', 'type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].queryset = ProductType.objects.none()

        # if the user hit submit but didn't choose a color & type we fill it directly from product field
        if 'product' in self.data:
            try:
                requestproduct = int(self.data.get('product'))
                splitedproduct = requestproduct.split()
                product = Product.objects.get(id=splitedproduct[0])
                self.fields['type'].queryset = ProductType.objects.filter(product=product).order_by('name')
                self.fields['price'].queryset = product.buyprice
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        # elif self.instance.pk:
        #     self.fields['city'].queryset = self.instance.country.city_set.order_by('name')


BuyOrderItemFormset = modelformset_factory(
    BuyOrderItem,
    form=BuyOrderItemForm,
    extra=1,
)
