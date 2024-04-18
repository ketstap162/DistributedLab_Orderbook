from django.shortcuts import render

from nbu_api.core import NBU
from trading_app.models import Currency


def get_all_currencies_rate(base_currency, currencies) -> dict:
    rates = {}
    for currency in currencies:
        rate = NBU.get_currency_rate(currency.code)
        rates[currency.name] = f"{rate} {base_currency.name}"

    return rates


def index_view(request):
    data = NBU.get_currency_data_all()

    parsed_data = {}
    for item in data:
        parsed_data[item["cc"]] = f"{item['rate']} UAH"

    return render(request, "index.html", context={"data": parsed_data})
