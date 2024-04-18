from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from trading_app.models import Wallet, Currency, Order
from trading_app.tools import order_exchange


@receiver(post_save, sender=get_user_model())
def register_user(sender, instance, created, **kwargs):

    if created:
        for currency in Currency.objects.all():
            wallet = Wallet()
            wallet.user = instance
            wallet.currency = currency
            wallet.save()


@receiver(post_save, sender=Order)
def create_order(sender, instance, created, **kwargs):

    if created:
        print("CREATED")
        base = instance.wallet_from.currency
        quote = instance.wallet_to.currency
        reversed_price = instance.price_reversed
        print("PRICE:", reversed_price)

        orders = Order.objects.filter(wallet_from__currency=quote, wallet_to__currency=base)
        for order in orders:
            print(f"ORDER-{order.id} - PRICE: {order.price} - REVERSED: {order.price_reversed}",)

        orders = orders.filter(price__gte=reversed_price)
        print("STOP")
        orders = orders.filter(is_active=True)
        orders = orders.order_by("-price")

        if orders:
            print("ORDER")
            for order in orders:
                order_exchange(instance, order)
                if instance.rest <= 0:
                    break
