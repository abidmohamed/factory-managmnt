from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from customer.models import City


class Delivery(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    phone = models.CharField(max_length=200, null=True)
    city = models.ForeignKey(City, null=True, on_delete=models.CASCADE)
    money = models.DecimalField(max_digits=10, null=True, decimal_places=2, default=0.0)
    point = models.PositiveIntegerField(default=1)
    level = models.PositiveIntegerField(default=1)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name
