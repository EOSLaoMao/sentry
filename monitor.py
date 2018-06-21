'''
curl  http://127.0.0.1:8888/v1/chain/get_table_rows -X POST -d '{"scope":"eosio", "code":"eosio", "table":"producers", "json": true}'
'''

import datetime

from telegram import send_message
from config import BP_NAME


def monitor_producer(bp):
    bp.check_is_bp()
    if bp.is_bp is False:
        msg = 'bp with name %s NOT FOUND!!!' % BP_NAME
        print(msg)
        send_message(msg)

    if bp.is_new is True:
        msg = 'congratulation! You become the new BP'
        print(msg)
        send_message(msg)

    if bp.check_is_producing():
        current_time = str(datetime.datetime.now())
        msg = '%s in good condition :)%s' % (BP_NAME, current_time)
        print(msg)
        send_message(msg)
