from django.db import models
from django.contrib.auth.models import User

from category.models import Category
from customer.models import City, Customer


# Create your models here.
from product.models import Product, ProductType
from warehouse.models import Stock


class Seller(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    phone = models.CharField(max_length=200, null=True)
    city = models.ForeignKey(City, null=True, on_delete=models.CASCADE)
    debt = models.DecimalField(max_digits=10, null=True, decimal_places=2, default=0.0)
    in_hold_money = models.DecimalField(max_digits=10, null=True, decimal_places=2, default=0.0)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name


class SellerStock(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, null=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'stock'
        verbose_name_plural = 'stocks'

    def __str__(self):
        return self.name


class SellerStockProduct(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    stock = models.ForeignKey(SellerStock, null=True, on_delete=models.CASCADE)
    product_type = models.ForeignKey(ProductType, null=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ('product',)
        verbose_name = 'seller stock product'
        verbose_name_plural = 'seller stock products'

    def __str__(self):
        return self.product.name

    def save(self, *args, **kwargs):
        self.category = self.product.category
        # if self.image:
        #    self.image = get_thumbnail(self.image, '570x320').url
        super(SellerStockProduct, self).save(*args, **kwargs)

    def get_types(self):
        types = self.product.types.all()
        return types


class SellerSellOrder(models.Model):
    user = models.IntegerField(default=0)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.selleritems.all())

    def get_total_weight(self):
        return sum(item.get_weight() for item in self.selleritems.all())


class OrderItem(models.Model):
    order = models.ForeignKey(SellerSellOrder,
                              related_name='selleritems',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='sellerorder_item',
                                on_delete=models.CASCADE, null=True, blank=True)
    product_type = models.ForeignKey(ProductType,
                                     related_name='sellerorder_item_type',
                                     on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    weight = models.DecimalField(max_digits=10, null=True, decimal_places=2, default=0.0)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity

    def get_weight(self):
        return self.weight * self.quantity


class SellerBuyOrder(models.Model):
    user = models.IntegerField(default=0)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.selleritems.all())

    def get_total_weight(self):
        return sum(item.get_weight() for item in self.selleritems.all())


class BuyOrderItem(models.Model):
    order = models.ForeignKey(SellerBuyOrder,
                              related_name='selleritems',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='sellerbuyorder_item',
                                on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    product_type = models.ForeignKey(ProductType, null=True, on_delete=models.CASCADE, related_name="seller_type")
    stock = models.ForeignKey(Stock, blank=True, null=True, on_delete=models.CASCADE, related_name="seller_stock")

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity

    def get_weight(self):
        return self.product_type.weight * self.quantity


