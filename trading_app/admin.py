from django.contrib import admin

# Register your models here.
from trading_app.models import Currency, Wallet, Order

admin.site.register(Currency)
admin.site.register(Wallet)
admin.site.register(Order)
