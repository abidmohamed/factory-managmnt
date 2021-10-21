from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from customer.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer

        fields = ['firstname', 'lastname', 'name', 'phone',
                  'city', 'location', 'customer_type', 'debt'
                  ]