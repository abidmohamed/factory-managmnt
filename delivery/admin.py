from django.contrib import admin

# Register your models here.
from delivery.models import Delivery


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'city']
