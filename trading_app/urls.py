from django.urls import path

from trading_app.views import wallet_view, wallet_deposit_view, wallet_withdraw_view, order_view, order_create_view, \
    order_detail_view, order_activate_view

app_name = "trading"

urlpatterns = [
    path("wallets/", wallet_view, name="wallet"),
    path("wallets/<int:pk>/deposit", wallet_deposit_view, name="wallet-deposit"),
    path("wallets/<int:pk>/withdraw", wallet_withdraw_view, name="wallet-withdraw"),
    path("orders/", order_view, name="order"),
    path("orders/create", order_create_view, name="order-create"),
    path("orders/<int:pk>/", order_detail_view, name="order-detail"),
    path("order/<int:pk>/activate", order_activate_view, name="order-activate")
]
