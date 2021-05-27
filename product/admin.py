from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
# Register your models here.
from product.models import Product


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    pass