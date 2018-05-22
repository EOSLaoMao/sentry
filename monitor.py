'''
curl  http://127.0.0.1:8888/v1/chain/get_table_rows -X POST -d '{"scope":"eosio", "code":"eosio", "table":"producers", "json": true}'
'''

import requests
import json
import os
import time

HOST = 'http://127.0.0.1:8888'
PATH = 'v1/chain/get_table_rows'

def get_producers():
    data = {
        "scope": "eosio",
        "code":"eosio",
        "table":"producers",
        "json": True
    }
    res = requests.post(os.path.join(HOST, PATH), data=json.dumps(data))
    prods = res.json()['rows']
    return prods

if __name__ == '__main__':
    prods = get_producers()
    print 'There are %d BPs' % len(prods)
    name = 'bp1'
    bps = [bp for bp in prods if bp['owner'] == name]
    if len(bps) == 0:
        print 'bp with name %s NOT FOUND!!!' % name
    else:
        last = int(bps[0]['last_produced_block_time'])
        now = int(time.time())
        last_converted = last/2. + 946684800
        if now - last_converted > 6*len(prods):
            print 'BP DOWN!!!!!'
        else:
            print 'BP is normal'
        print now, last_converted, now - last_converted
