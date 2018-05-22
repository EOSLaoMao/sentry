'''
curl  http://127.0.0.1:8888/v1/chain/get_table_rows -X POST -d '{"scope":"eosio", "code":"eosio", "table":"producers", "json": true}'
'''

import requests
import json
import os
import time

HOST = 'http://bp-2.ono.chat:8877'
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

def monitor_producer(name='eoslaomao'):
    prods = get_producers()
    print 'There are %d BPs' % len(prods)
    bps = [bp for bp in prods if bp['owner'] == name]
    if len(bps) == 0:
        print 'bp with name %s NOT FOUND!!!' % name
    else:
        last = int(bps[0]['last_produced_block_time'])
        now = int(time.time())
        # magic number, 946684800 is 2000.1.1 12:00 AM
        last_converted = last/2. + 946684800
        if now - last_converted > 6 * min(21, len(prods)):
            print 'BP DOWN!!!!!'
        else:
            print 'BP is normal'
        print now, last_converted, now - last_converted
