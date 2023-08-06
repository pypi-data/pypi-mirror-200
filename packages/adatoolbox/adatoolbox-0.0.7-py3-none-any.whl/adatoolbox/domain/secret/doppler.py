import requests
from adatoolbox.domain.secret.settings import DOPPLER_TOKEN


class Doppler(object):
    __url: str = "https://api.doppler.com/v3/configs/config/secrets/download?format=json&include_dynamic_secrets=true&dynamic_secrets_ttl_sec=1800"

    def __init__(self):
        self.__headers = {
            "accept": "application/json",
            "authorization": f"Bearer {DOPPLER_TOKEN}"
        }
        response = requests.get(self.__url, headers=self.__headers)
        self.__environment = response.json()
        for key, value in self.__environment.items():
            if isinstance(value, dict):
                self.__dict__[key] = Doppler(**value)
            else:
                self.__dict__[key] = value
