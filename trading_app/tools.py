from django.db import transaction

from trading_app.models import Wallet, Order


def order_check_deactivate(order: Order):
    if order.rest == 0 or order.deposit == 0:
        order.is_active = False


def currency_exchange(
        order: Order,
        user_wallet_from: Wallet,
        user_wallet_to: Wallet,
        amount_int: int,
) -> None:

    cost_int = (100 / order.price) * amount_int

    order.deposit -= amount_int
    order.wallet_to.balance += cost_int
    order.rest -= cost_int

    user_wallet_to.balance += amount_int
    user_wallet_from.balance -= cost_int

    order_check_deactivate(order)

    with transaction.atomic():
        order.wallet_to.save()
        order.wallet_from.save()
        user_wallet_from.save()
        user_wallet_to.save()
        order.save()


def order_exchange(
        new_order: Order,
        released_order: Order,
) -> None:
    if new_order.rest <= released_order.deposit:
        amount_int = new_order.rest  # Buy UAH
    else:
        amount_int = released_order.deposit  # Buy UAH

    cost_int = released_order.price_reversed * amount_int / 100  # Sell USD
    print("=== COST", cost_int)
    print("=== AMOUNT", amount_int)

    new_order.deposit -= cost_int
    new_order.rest -= amount_int
    new_order.wallet_to.balance += amount_int

    released_order.deposit -= amount_int
    released_order.rest -= cost_int
    released_order.wallet_to.balance += cost_int

    order_check_deactivate(new_order)
    order_check_deactivate(released_order)

    with transaction.atomic():
        new_order.wallet_to.save()
        new_order.save()

        released_order.wallet_to.save()
        released_order.save()
