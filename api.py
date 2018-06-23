import json
import os
import requests
from config import HOST


def get_info():
    endpoint = 'v1/chain/get_info'
    res = requests.get(os.path.join(HOST, endpoint))
    return res.json()


def get_producers():
    endpoint = 'v1/chain/get_producers'
    data = {
        "lower_bound": "",
        "limit": 21,
        "json": True
    }
    res = requests.post(os.path.join(HOST, endpoint), data=json.dumps(data))
    print(res)
    prods = res.json()['rows']
    return prods
