from django.forms import ModelForm

from billingorder.models import OrderBilling


class BillingOrderForm(ModelForm):
    class Meta:
        model = OrderBilling

        fields = ['delivery', ]
