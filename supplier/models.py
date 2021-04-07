from django.db import models

# Create your models here.
from customer.models import City


class Supplier(models.Model):
    firstname = models.CharField(max_length=200, null=True)
    lastname = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    city = models.ForeignKey(City, null=True, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    credit = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0.0)

    def __str__(self):
        return self.firstname + " " + self.lastname
