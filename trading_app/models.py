from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.


class Currency(models.Model):
    name = models.CharField(max_length=80)
    code = models.CharField(max_length=10)
    base = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Wallet(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, blank=True, null=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.IntegerField()


class Order(models.Model):
    OPERATION_CHOICES = {
        "B": "Buy",
        "S": "Sell",
    }

    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.IntegerField()
    price = models.IntegerField()
    operation = models.CharField(max_length=10, choices=OPERATION_CHOICES)
