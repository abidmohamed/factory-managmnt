from django.db import models

# Create your models here.

from category.models import Category


class Product(models.Model):
    # add buy price or production price
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, null=True)
    ref = models.CharField(max_length=250, null=True)
    desc = models.CharField(max_length=250, null=True, blank=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, )
    stock = models.ForeignKey('warehouse.Stock', null=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ('name',)
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return self.name

    def have_types(self):
        return self.types.all().count()

    def get_types(self):
        return self.types.all().filter(product=self)


class ProductType(models.Model):
    product = models.ForeignKey(Product,
                                related_name='types',
                                on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=250, null=True)
    # Sell price
    price1 = models.DecimalField(max_digits=10, null=True, decimal_places=2, default=0)
    price2 = models.DecimalField(max_digits=10, null=True, decimal_places=2, default=0)
    price3 = models.DecimalField(max_digits=10, null=True, decimal_places=2, default=0)
    price4 = models.DecimalField(max_digits=10, null=True, decimal_places=2, default=0)
    price5 = models.DecimalField(max_digits=10, null=True, decimal_places=2, default=0)
    price6 = models.DecimalField(max_digits=10, null=True, decimal_places=2, default=0)

    buyprice = models.DecimalField(max_digits=10, null=True, decimal_places=2, default=0)
    alert_quantity = models.PositiveIntegerField(default=1)
    box_quantity = models.PositiveIntegerField(default=1)
    weight = models.DecimalField(max_digits=10, null=True, decimal_places=2, default=0.0)

    def __str__(self):
        return self.name

    def get_product(self):
        return self.product
