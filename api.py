import json
import os
import requests
from config import HOSTS

def multi_request(func, endpoint, **kwargs):
    for host in HOSTS:
        try:
            return func(os.path.join(host, endpoint), **kwargs)
        except Exception as e:
            print('multi_request', host, e)
    raise Exception('run out of host list')


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
        res = multi_request(requests.post, endpoint, data=json.dumps(data))
        prods = res.json()['rows']
        return prods
    except Exception as e:
        print("get table", e)


def get_info():
    try:
        endpoint = 'v1/chain/get_info'
        res = multi_request(requests.get, endpoint)
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
        res = multi_request(requests.post, endpoint, data=json.dumps(data))
        print(res)
        prods = res.json()['rows']
        return prods
    except Exception as e:
        print("get_info", e)
