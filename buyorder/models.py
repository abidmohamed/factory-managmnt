from django.db import models

# Create your models here.
from customer.models import City
from product.models import Product, ProductType
from supplier.models import Supplier
from warehouse.models import Stock


class BuyOrder(models.Model):
    user = models.IntegerField(default=0)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
    factured = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_total_weight(self):
        return sum(item.get_weight() for item in self.items.all())


class BuyOrderItem(models.Model):
    order = models.ForeignKey(BuyOrder,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='buyorder_item',
                                on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    type = models.ForeignKey(ProductType, null=True, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity

    def get_weight(self):
        return self.type.weight * self.quantity
