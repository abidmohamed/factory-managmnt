from django.forms import ModelForm, forms
from django import forms
from payments.models import CustomerPayment, SupplierPayment, CustomerCheque, SupplierCheque


class CustomerPaymentForm(ModelForm):
    class Meta:
        model = CustomerPayment
        widgets = {
            'pay_date': forms.DateInput(attrs={'class': 'datepicker', 'type': 'date'}),
        }
        fields = ['amount', 'pay_status', 'pay_date']


class CustomerChequeForm(ModelForm):
    class Meta:
        model = CustomerCheque

        fields = ['cheque_number', ]


class SupplierPaymentForm(ModelForm):
    class Meta:
        model = SupplierPayment
        widgets = {
            'pay_date': forms.DateInput(attrs={'class': 'datepicker', 'type': 'date'}),
        }
        fields = ['amount', 'pay_status', 'pay_date']


class SupplierChequeForm(ModelForm):
    class Meta:
        model = SupplierCheque

        fields = ['cheque_number', ]
