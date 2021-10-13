from django.contrib import admin

# Register your models here.
from seller.models import Seller, SellerSellOrder, OrderItem, BuyOrderItem, SellerBuyOrder, SellerStock, \
    SellerStockProduct


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'city', 'debt', 'date_created']


@admin.register(SellerSellOrder)
class SellerSellOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'paid']


@admin.register(OrderItem)
class SellerSellOrderItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'product_type', 'price', 'weight', 'quantity']


@admin.register(SellerBuyOrder)
class SellerBuyOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'seller', 'paid']


@admin.register(BuyOrderItem)
class SellerBuyOrderItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'product_type', 'price', 'quantity', 'stock']


@admin.register(SellerStock)
class SellerStockAdmin(admin.ModelAdmin):
    list_display = ['seller', 'name', ]


@admin.register(SellerStockProduct)
class SellerStockProductAdmin(admin.ModelAdmin):
    list_display = ['product', 'product_type', 'quantity', 'stock', 'category']
