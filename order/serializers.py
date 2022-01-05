from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from order.models import Order, OrderItem


class SellorderItemSerializer(serializers.ModelSerializer):
    product = serializers.CharField(source='product.name')
    product_type = serializers.CharField(source='product_type.name')
    product_id = serializers.CharField(source='product.id')
    product_type_id = serializers.CharField(source='product_type.id')
    weight = serializers.CharField(source='product_type.weight')

    class Meta:
        model = OrderItem

        fields = ['product', 'product_type', 'product_id',
                  'product_type_id', 'price', 'weight', 'quantity',
                  ]


class SellOrderSerializer(serializers.ModelSerializer):
    order_items = SellorderItemSerializer(many=True, read_only=True)
    customer = serializers.CharField(source="customer.__str__")
    customer_id = serializers.IntegerField(source="customer.id")

    class Meta:
        model = Order

        fields = ['customer', 'delivered', 'paid', 'order_items']


# Add Sell Order
class AddSellorderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem

        fields = ['product', 'product_type', 'quantity', 'price']


class AddSellOrderSerializer(serializers.ModelSerializer):
    order_items = AddSellorderItemSerializer(many=True)

    class Meta:
        model = Order

        fields = ['customer', 'delivered', 'paid', 'order_items']

    def create(self, validated_data):
        print("**Validated Data ======>", **validated_data)
        items_data = validated_data.pop('order_items')

        return items_data
