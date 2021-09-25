from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from payments.models import CustomerPayment


class CustomerPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerPayment

        fields = ['customer', 'amount', 'pay_date', 'pay_status']
