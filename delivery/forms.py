from django.forms import ModelForm

from delivery.models import Delivery


class DeliveryFrom(ModelForm):
    class Meta:
        model = Delivery

        fields = ('phone', 'city')
