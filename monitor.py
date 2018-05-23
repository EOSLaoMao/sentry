'''
curl  http://127.0.0.1:8888/v1/chain/get_table_rows -X POST -d '{"scope":"eosio", "code":"eosio", "table":"producers", "json": true}'
'''

import requests
import json
import os
import time
import datetime

from config import HOST, BP_NAME, ENABLE_TWILIO
from telegram import send_message

PATH = 'v1/chain/get_table_rows'
count = 0


def notify(msg):
    send_message(msg)
    if ENABLE_TWILIO:
        from phone import call
        call()


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

def monitor_producer():
    global count
    prods = get_producers()
    print 'There are %d BPs' % len(prods)
    bps = [bp for bp in prods if bp['owner'] == BP_NAME]
    if len(bps) == 0:
        msg = 'bp with name %s NOT FOUND!!!' % BP_NAME
        notify(msg)
        print msg
    else:
        last = int(bps[0]['last_produced_block_time'])
        now = int(time.time())
        # magic number, 946684800 is 2000.1.1 12:00 AM
        last_converted = last/2. + 946684800
        if now - last_converted > 6 * min(21, len(prods)):
            msg = 'BP DOWN!!!!!'
            send_message(msg)
            print msg
        else:
            if count%120 == 0:
                current_time = str(datetime.datetime.now())
                msg = 'BP in good condition :) @ %s'%current_time
                send_message(msg)
                print msg
                count=0
            count+=1
        print now, last_converted, now - last_converted
