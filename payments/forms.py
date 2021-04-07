from django.forms import ModelForm, forms

from payments.models import CustomerPayment, SupplierPayment, CustomerCheque, SupplierCheque


class CustomerPaymentForm(ModelForm):
    class Meta:
        model = CustomerPayment

        fields = ['amount', ]


class CustomerChequeForm(ModelForm):
    class Meta:
        model = CustomerCheque

        fields = ['cheque_number', ]


class SupplierPaymentForm(ModelForm):
    class Meta:
        model = SupplierPayment

        fields = ['amount', ]


class SupplierChequeForm(ModelForm):
    class Meta:
        model = SupplierCheque

        fields = ['cheque_number', ]
