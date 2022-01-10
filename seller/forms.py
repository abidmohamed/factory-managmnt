from django.forms import ModelForm
from django import forms
from seller.models import Seller, NoStockSeller, SellerMoneyInHold


class SellerForm(ModelForm):
    class Meta:
        model = Seller

        fields = ('phone', 'city', 'debt')


class NoStockSellerForm(ModelForm):
    class Meta:
        model = NoStockSeller

        fields = ('phone', 'city', 'debt')


class SubmittingMoneyForm(ModelForm):

    class Meta:
        model = SellerMoneyInHold

        widgets = {
            'pay_date': forms.DateInput(attrs={'class': 'datepicker', 'type': 'date'}),
        }
        fields = ['amount', 'pay_date']