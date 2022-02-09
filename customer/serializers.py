from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from customer.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")

    class Meta:
        model = Customer

        fields = ['id', 'username', 'firstname', 'lastname', 'name', 'phone',
                  'city', 'location', 'customer_type', 'debt'
                  ]