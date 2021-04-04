from django.contrib.auth.models import User
from django.contrib.gis.db import models


class City(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=200, null=True)
    lastname = models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    city = models.ForeignKey(City, null=True, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    location = models.PointField(null=True)

    type_choice = (
        ('type1', 'type1'),
        ('type2', 'type2'),
        ('type3', 'type3'),
        ('type4', 'type4'),
        ('type5', 'type5'),
        ('type6', 'type6'),
    )
    customer_type = models.CharField(max_length=9, choices=type_choice, blank=True, default="type1")

    debt = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return self.name
        # return self.firstname + " " + self.lastname

# define signals so our Customer model will be automatically created/updated when we create/update User instances.
# @receiver(post_save, sender=User)
# def create_user_customer(sender, instance, created, **kwargs):
#   if created:
#      Customer.objects.create(user=instance)


# Update
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#   instance.customer.save()
