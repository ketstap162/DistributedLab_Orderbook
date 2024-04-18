from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

# Create your models here.


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True


class Currency(models.Model):
    name = models.CharField(max_length=80)
    code = models.CharField(max_length=10)
    base = models.BooleanField(default=False)

    objects = models.Manager()

    def __str__(self):
        return f"{self.name} ({self.code})"


class Wallet(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="wallets",
    )
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, blank=True, null=True)
    balance = models.IntegerField(default=0)

    objects = models.Manager()

    def balance_display(self):
        return self.balance / 100

    def __str__(self):
        return f"({self.id}) {self.user.username} - {self.currency}"

    def display_wallet_info(self):
        return f"({self.id}) {self.currency}"

    def save(self, *args, **kwargs):
        if self.balance < 0:
            raise ValidationError("Balance cannot be negative.")
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-id"]


class Order(TimeStampedModel):
    wallet_from = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="orders_from")
    wallet_to = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="orders_to")
    deposit = models.IntegerField()
    amount = models.IntegerField()
    rest = models.IntegerField()
    price = models.IntegerField()
    is_active = models.BooleanField(default=True)

    objects = models.Manager()

    @property
    def price_reversed(self):
        return int(10000 / self.price)

    @property
    def display_price_reversed(self):
        return self.price_reversed / 100

    @property
    def display_price(self):
        return self.price / 100

    @property
    def display_amount(self):
        return self.amount / 100

    @property
    def display_rest(self):
        return self.rest / 100

    @property
    def display_deposit(self):
        return self.deposit / 100



    def __str__(self):
        return f"({self.id}) {self.wallet_from.user} | {self.wallet_from.currency} -> {self.wallet_to.currency}"

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if self.deposit < 0:
            raise ValidationError("Deposit cannot be negative.")

        super().save(*args, **kwargs)
