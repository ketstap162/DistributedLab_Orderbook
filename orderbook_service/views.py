from django.shortcuts import render

from nbu_api.core import NBU


def index_view(request):
    data = NBU.get_currency_data_all()

    parsed_data = {}
    for item in data:
        parsed_data[item["cc"]] = f"{item['rate']} UAH"

    return render(request, "index.html", context={"data": parsed_data})
