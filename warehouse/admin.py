from django.contrib import admin

# Register your models here.
from warehouse.models import StockProduct


@admin.register(StockProduct)
class StockProductAdmin(admin.ModelAdmin):
    list_display = ['product','type', 'stock', 'quantity']