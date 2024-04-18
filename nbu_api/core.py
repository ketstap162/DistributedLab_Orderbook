import os
from datetime import datetime

import requests

NBU_API_PATH = os.environ.get("NBU_API_URL", "https://bank.gov.ua/NBUStatService/v1/")
# https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json&valcode=usd


class NBU:
    path = NBU_API_PATH

    @classmethod
    def get_currency_data_all(cls, date: datetime = None):
        if not date:
            date = datetime.now().strftime("%Y%m%d")
        else:
            date = date.strftime("%Y%m%d")

        endpoint_path = cls.path + "statdirectory/exchange"

        response = requests.get(endpoint_path, params={
            "json": "",
            "data": date,
        })

        return response.json()

    @classmethod
    def get_currency_data(cls, currency_code):
        endpoint_path = cls.path + "statdirectory/exchange"
        response = requests.get(endpoint_path, params={
            "json": "",
            "valcode": currency_code,
        })

        return response.json()[0]

    @classmethod
    def get_currency_rate(cls, currency_code):
        currency_data = cls.get_currency_data(currency_code)
        return currency_data["rate"]


if __name__ == "__main__":
    data = NBU.get_currency_data_all()

    parsed_data = {}
    for item in data:
        parsed_data[item["cc"]] = f"{item['rate']} UAH"

    print(parsed_data)
