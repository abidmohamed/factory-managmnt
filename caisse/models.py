from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
# verbose_name is for transaction
class Transaction(models.Model):
    Transaction_name = models.CharField(verbose_name=_("Transaction Name"),max_length=200, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type_choices = (
        ('Income', _('Income')),
        ('Expense', _('Expense'))
    )
    trans_date = models.DateField(verbose_name=_("Transaction Date"), null=True, blank=True)
    Transaction_type = models.CharField(verbose_name=_("Transaction Type"), max_length=8, choices=type_choices, blank=True)
    date_created = models.DateTimeField(verbose_name=_("Transaction Date"), auto_now_add=True, null=True)
