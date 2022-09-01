import base64
import json
import logging
import os
import sys
from datetime import datetime
from time import sleep

import requests
from bs4 import BeautifulSoup
from twocaptcha import TwoCaptcha

from utils import telegram


class Sim:
    def __init__(self, country, product):
        self.s = requests.Session()
        config_file = os.path.dirname(os.path.dirname(__file__)) + "/config.json"
        with open(config_file) as json_file:
            self.api_key = json.load(json_file)['sim_key']
        self.sim_id, self.sim_phone = self.get_new_number(country, product)

    def get_new_number(self, country, product):
        r = self.s.get(f'https://5sim.net/v1/guest/prices?country={country}&product={product}')
        if r.status_code == 200:
            prices = r.json()[country][product]
        else:
            raise RuntimeError(f'Ошибка 5sim({r.status_code}): {r.text}')
        valid_operators = {k: v for k, v in prices.items() if v['count'] and v['cost'] < 10}
        operator = list(valid_operators.keys())[0]

        headers = {'Authorization': f"Bearer {self.api_key}", 'Accept': 'application/json', }
        r = self.s.get(f'https://5sim.net/v1/user/buy/activation/{country}/{operator}/{product}', headers=headers)
        return r.json()['id'], r.json()['phone']

    def get_new_code(self, latest_code=None):
        code = None
        for _ in range(6):
            headers = {'Authorization': f"Bearer {self.api_key}", 'Accept': 'application/json', }
            r = self.s.get(f'https://5sim.net/v1/user/check/{self.sim_id}', headers=headers)
            if r.json()['sms']:
                new_code = r.json()['sms'][-1]['code']
            else:
                new_code = None
            if new_code != latest_code:
                code = new_code
                break
            sleep(10)
        return code

    def ban_sim(self):
        headers = {'Authorization': f"Bearer {self.api_key}", 'Accept': 'application/json', }
        self.s.get(f'https://5sim.net/v1/user/ban/{self.sim_id}', headers=headers)
