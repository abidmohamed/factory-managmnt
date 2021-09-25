from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from order.models import Order


class SellOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order

        fields = ['customer', 'delivered', 'paid']
