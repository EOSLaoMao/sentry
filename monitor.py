'''
curl  http://127.0.0.1:8888/v1/chain/get_table_rows -X POST -d '{"scope":"eosio", "code":"eosio", "table":"producers", "json": true}'
'''

import datetime

from telegram import send_message
from config import BP_NAME
from phone import call


def get_current_time():
    current_time = str(datetime.datetime.now())
    return current_time


def monitor_producer(bp):
    check_is_top21(bp)
    check_is_new_top21(bp)

    if bp.is_top21 is True:
        check_is_producing(bp)


def check_is_top21(bp):
    bp.check_is_top21()
    if bp.is_top21 is False:
        msg = 'bp with name %s NOT FOUND!!! @ %s' % (
            BP_NAME, get_current_time())
        print("in check_is_top21 ", get_current_time())
        send_message(msg)


def check_is_new_top21(bp):
    if bp.is_new_top21 is True:
        msg = 'Congratulations! %s become the new top 21 ! @ %s' % (
            BP_NAME, get_current_time())
        print('in is_new_top21 function', get_current_time())
        send_message(msg)
        call()


def check_is_producing(bp):
    if bp.check_is_producing():
        msg = '%s in good condition :) @%s' % (BP_NAME, get_current_time())
        print('produing....', get_current_time())
        send_message(msg)
    else:
        msg = '%s DOWN :( @%s' % (BP_NAME, get_current_time())
        print('down...', get_current_time())
        send_message(msg)
        call()
