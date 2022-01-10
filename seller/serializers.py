from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from seller.models import Seller, SellerSellOrder, OrderItem, SellerBuyOrder, BuyOrderItem, SellerStockProduct, \
    SellerCustomer, SellerCustomerPayment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = ['username', 'first_name', 'last_name']


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller

        fields = ['id', 'user', 'phone', 'city', 'debt']


class AddSellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller

        fields = ['user', 'phone', 'city', 'debt']


# Sell Order Serializer
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


class SellerSellOrderSerializer(serializers.ModelSerializer):
    selleritems = SellorderItemSerializer(many=True, read_only=True)
    customer = serializers.CharField(source="customer.__str__")
    customer_id = serializers.IntegerField(source="customer.id")

    # total_cost = serializers.DecimalField(source="get_cost", read_only=True, max_digits=10, decimal_places=2)
    # total_weight = serializers.DecimalField(source="get_weight()", read_only=True, max_digits=10, decimal_places=2)

    class Meta:
        model = SellerSellOrder

        fields = ['id', 'customer_id', 'customer', 'paid', 'selleritems', ]


# Add Seller Sell Order
class AddSellorderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem

        fields = ['product', 'product_type', 'quantity', 'price']


class AddSellerSellOrderSerializer(serializers.ModelSerializer):
    selleritems = AddSellorderItemSerializer(many=True)

    class Meta:
        model = SellerSellOrder

        fields = ['customer', 'paid', 'selleritems']

    def create(self, validated_data):
        print("**Validated Data ======>", **validated_data)
        items_data = validated_data.pop('selleritems')
        # order = SellerSellOrder.objects.create(**validated_data)
        # for item in items_data:
        #     OrderItem.objects.create(order=order, **item)
        # print("Order Item ====>", order_item)
        return items_data


# Buy order Serialzer
class BuyorderItemSerializer(serializers.ModelSerializer):
    product = serializers.CharField(source='product.name')
    product_id = serializers.CharField(source='product.id')
    product_type = serializers.CharField(source='product_type.name')
    product_type_id = serializers.CharField(source='product_type.id')

    class Meta:
        model = BuyOrderItem

        fields = ['product', 'product_id', 'price', 'quantity', 'product_type', 'product_type_id', 'stock']


class SellerBuyOrderSerializer(serializers.ModelSerializer):
    selleritems = BuyorderItemSerializer(many=True, read_only=True)
    seller = serializers.CharField(source="seller.__str__")

    class Meta:
        model = SellerBuyOrder

        fields = ['id', 'seller', 'paid', 'selleritems']


# Add Seller Buy Order
class AddBuyorderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyOrderItem

        fields = ['product', 'price', 'quantity', 'product_type', 'stock']


class AddSellerBuyOrderSerializer(serializers.ModelSerializer):
    selleritems = AddBuyorderItemSerializer(many=True)

    class Meta:
        model = SellerBuyOrder

        fields = ['seller', 'paid', 'selleritems']


# StockProduct

class SellerStockProductSerializer(serializers.ModelSerializer):
    product = serializers.CharField(source='product.name')
    product_type = serializers.CharField(source='product_type.name')
    product_id = serializers.CharField(source='product.id')
    product_type_id = serializers.CharField(source='product_type.id')
    weight = serializers.CharField(source='product_type.weight')
    price1 = serializers.DecimalField(source='product_type.price1', max_digits=10, decimal_places=2)
    price2 = serializers.DecimalField(source='product_type.price2', max_digits=10, decimal_places=2)
    price3 = serializers.DecimalField(source='product_type.price3', max_digits=10, decimal_places=2)
    price4 = serializers.DecimalField(source='product_type.price4', max_digits=10, decimal_places=2)
    price5 = serializers.DecimalField(source='product_type.price5', max_digits=10, decimal_places=2)
    price6 = serializers.DecimalField(source='product_type.price6', max_digits=10, decimal_places=2)

    class Meta:
        model = SellerStockProduct

        fields = ['id', 'product', 'product_id', 'product_type_id',
                  'quantity', 'category', 'product_type', 'weight',
                  'price1', 'price2', 'price3', 'price4', 'price5', 'price6',
                  ]


# Seller Customer
# List
class SellerCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerCustomer

        fields = [
            'id', 'firstname', 'lastname', 'phone', 'customer_type', 'debt'
        ]


# Add
class AddSellerCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerCustomer

        fields = [
            'firstname', 'lastname', 'phone', 'customer_type', 'debt'
        ]


# Seller Customer Payment
# # Add
class AddSellerCustomerPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerCustomerPayment

        fields = [
            'customer', 'amount', 'pay_date'
        ]


# # List
class ListSellerCustomerPaymentSerializer(serializers.ModelSerializer):
    customer = serializers.CharField(source="customer.__str__")
    customer_id = serializers.IntegerField(source="customer.id")

    class Meta:
        model = SellerCustomerPayment

        fields = [
            'id', 'customer', 'customer_id', 'amount', 'pay_date'
        ]
