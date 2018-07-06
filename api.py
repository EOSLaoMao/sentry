import json
import os
import requests
from config import HOST


def get_table():
    try:
        endpoint = 'v1/chain/get_table_rows'
        data = {
            "json": True,
            "code": "eosio",
            "scope": "eosio",
            "table": "producers",
            "table_key": "",
            "lower_bound": "",
            "upper_bound": "",
            "limit": 1000}
        res = requests.post(os.path.join(HOST, endpoint),
                            data=json.dumps(data))
        prods = res.json()['rows']
        return prods
    except Exception as e:
        print("get table", e)


def get_info():
    try:
        endpoint = 'v1/chain/get_info'
        res = requests.get(os.path.join(HOST, endpoint))
        return res.json()
    except Exception as e:
        print("get_info", e)


def get_producers():
    try:
        endpoint = 'v1/chain/get_producers'
        data = {
            "lower_bound": "",
            "limit": 21,
            "json": True
        }
        res = requests.post(os.path.join(HOST, endpoint),
                            data=json.dumps(data))
        print(res)
        prods = res.json()['rows']
        return prods
    except Exception as e:
        print("get_info", e)
