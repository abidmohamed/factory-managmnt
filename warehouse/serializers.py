from rest_framework import serializers
from django.contrib.auth.models import User

from warehouse.models import StockProduct


class StockProductSerializer(serializers.ModelSerializer):
    product = serializers.CharField(source='product.name')
    product_type = serializers.CharField(source='type.name')
    product_id = serializers.CharField(source='product.id')
    product_type_id = serializers.CharField(source='type.id')
    weight = serializers.CharField(source='type.weight')
    price1 = serializers.DecimalField(source='type.price1', max_digits=10, decimal_places=2)
    price2 = serializers.DecimalField(source='type.price2', max_digits=10, decimal_places=2)
    price3 = serializers.DecimalField(source='type.price3', max_digits=10, decimal_places=2)
    price4 = serializers.DecimalField(source='type.price4', max_digits=10, decimal_places=2)
    price5 = serializers.DecimalField(source='type.price5', max_digits=10, decimal_places=2)
    price6 = serializers.DecimalField(source='type.price6', max_digits=10, decimal_places=2)

    class Meta:
        model = StockProduct

        fields = ['id', 'product', 'product_id', 'product_type_id',
                  'quantity', 'category', 'product_type', 'weight',
                  'price1', 'price2', 'price3', 'price4', 'price5', 'price6',
                  ]
