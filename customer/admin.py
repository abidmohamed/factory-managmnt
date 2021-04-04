from django.contrib import admin

# Register your models here.
from django.contrib.gis.admin import OSMGeoAdmin

from customer.models import Customer


@admin.register(Customer)
class CustomerAdmin(OSMGeoAdmin):
    list_display = ('firstname', 'lastname', 'location', 'customer_type')