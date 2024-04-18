from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect

# Create your views here.
from trading_app.forms import DepositForm, WithdrawForm, OrderForm, OrderPurchaseForm
from trading_app.models import Wallet, Order
from trading_app.tools import currency_exchange
from utils_http.auth import auth_required
from utils_http.errors import response_error


@auth_required
def wallet_view(request):
    wallets = Wallet.objects.filter(user=request.user)
    context = {
        "wallets": wallets
    }
    return render(request, "trading_app/wallet-list.html", context)


@auth_required
def wallet_deposit_view(request, pk):
    wallet = Wallet.objects.get(pk=pk)

    if wallet.user != request.user:
        return response_error(request, 403, "User is not owner of this wallet.")

    if request.method == "POST":
        form = DepositForm(request.POST)

        if form.is_valid():
            amount = form.cleaned_data["amount"] * 100
            wallet.balance += amount
            wallet.save()
            return redirect("trading:wallet")
    else:
        form = DepositForm()

    context = {
        "wallet": wallet,
        "form": form,
    }
    return render(request, "trading_app/wallet-deposit.html", context)


@auth_required
def wallet_withdraw_view(request, pk):
    wallet = Wallet.objects.get(pk=pk)

    if wallet.user != request.user:
        return response_error(request, 403, "User is not owner of this wallet.")

    if request.method == "POST":
        form = WithdrawForm(request.POST, wallet=wallet)

        if form.is_valid():
            amount = form.cleaned_data["amount"] * 100
            if wallet.balance >= amount:
                wallet.balance -= amount
                wallet.save()
            return redirect("trading:wallet")

    else:
        form = WithdrawForm(wallet=wallet)

    context = {
        "wallet": wallet,
        "form": form,
    }
    return render(request, "trading_app/wallet-withdraw.html", context)


def order_view(request):
    orders = Order.objects.filter(is_active=True).select_related('wallet_from', 'wallet_to')

    context = {
        "orders": orders,
    }
    return render(request, "trading_app/order-list.html", context)


@auth_required
def order_create_view(request):
    if request.method == "POST":
        form = OrderForm(request.user, request.POST)
        if form.is_valid():
            int_amount = form.cleaned_data["amount"] * 100
            int_price = form.cleaned_data["price"] * 100
            price_option = form.cleaned_data["price_option"]

            if price_option == "total_price":
                print("TOTAL")
                int_price = 100 * (int_price / int_amount)
            else:
                print("ONE")
                int_price = int_price
            print("PRICE", int_price)

            order = Order()
            order.wallet_from = form.cleaned_data["wallet_from"]
            order.wallet_to = form.cleaned_data["wallet_to"]
            order.amount = int_amount
            order.rest = int_amount

            order.price = int_price

            int_cost = int_price * int_amount / 100

            order.wallet_from.balance -= int_cost
            order.deposit = int_cost

            with transaction.atomic():
                order.wallet_from.save()
                order.save()

            return redirect("trading:order")
        
    else:
        form = OrderForm(request.user)

    return render(request, "trading_app/order-create.html", {"form": form})


@auth_required
def order_detail_view(request, pk):
    order = Order.objects.get(pk=pk)
    owner = order.wallet_from.user == request.user

    if not owner:
        form = OrderPurchaseForm(request.user, order)
    else:
        form = None

    if request.method == "POST":
        if not order.is_active:
            return response_error(request, 403, "Order is deactivated.")

        form = OrderPurchaseForm(request.user, order, request.POST)
        if form.is_valid():
            wallet_from = form.cleaned_data["wallet_from"]
            wallet_to = form.cleaned_data["wallet_to"]
            amount = form.cleaned_data["amount"] * 100

            currency_exchange(
                order=order,
                user_wallet_from=wallet_from,
                user_wallet_to=wallet_to,
                amount_int=amount
            )

            return redirect("trading:order-detail", pk=pk)

    return render(
        request,
        "trading_app/order-detail.html",
        context={
            "order": order,
            "owner": owner,
            "form": form,
        }
    )


@auth_required
def order_activate_view(request, pk):
    order = Order.objects.get(pk=pk)

    if order.wallet_from.user == request.user:
        order.is_active = not order.is_active
        order.save()

    return redirect("trading:order-detail", pk=pk)
