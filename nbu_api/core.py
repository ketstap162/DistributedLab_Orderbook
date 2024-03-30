import os

import requests

NBU_API_PATH = os.environ.get("NBU_API_URL", "https://bank.gov.ua/NBUStatService/v1/")
# https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json&valcode=usd


class NBU:
    path = NBU_API_PATH

    @classmethod
    def get_currency_data(cls, currency_code):
        endpoint_path = cls.path + "statdirectory/exchange"
        response = requests.get(endpoint_path, params={
            "json": "",
            "valcode": currency_code,
        })

        return response.json()[0]


if __name__ == "__main__":
    print("National bank of Ukraine")
    data = NBU.get_currency_data("usd")
    print("Type", type(data))
    print(data)
