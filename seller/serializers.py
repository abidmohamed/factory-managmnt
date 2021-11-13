from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from seller.models import Seller, SellerSellOrder, OrderItem, SellerBuyOrder, BuyOrderItem, SellerStockProduct


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

    # total_cost = serializers.DecimalField(source="get_cost", read_only=True, max_digits=10, decimal_places=2)
    # total_weight = serializers.DecimalField(source="get_weight()", read_only=True, max_digits=10, decimal_places=2)

    class Meta:
        model = SellerSellOrder

        fields = ['id', 'customer', 'paid', 'selleritems', ]


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
    product_type = serializers.CharField(source='product_type.name')

    class Meta:
        model = BuyOrderItem

        fields = ['product', 'price', 'quantity', 'product_type', 'stock']


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

    class Meta:
        model = SellerStockProduct

        fields = ['id', 'product', 'product_id', 'product_type_id', 'quantity', 'category', 'product_type']
