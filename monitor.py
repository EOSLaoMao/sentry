import datetime
from telegram import send_message
from config import BP_NAME
from phone import call
from api import get_producers, get_table


def get_current_time():
    current_time = str(datetime.datetime.now())
    return current_time


class BPMonitor:
    def __init__(self, bp):
        self.bp = bp
        self.count = 0

    def check_is_top21(self):
        prods = get_producers()
        print('There are %d BPs' % len(prods))
        bps = [bp for bp in prods if bp['owner'] == self.bp.name]
        if len(bps) == 0:
            self.bp.is_top21 = False
        else:  # in top 21 bp list
            if self.bp.is_top21 is False:
                self.bp.is_new_top21 = True
            else:
                self.bp.is_new_top21 = False
            self.bp.is_top21 = True

    def check_is_producing(self):
        self.count += 1
        prods = get_table()
        bps = [bp for bp in prods if bp['owner'] == self.bp.name]
        current_unpaid_blocks = 0
        if len(bps) != 0:
            current_unpaid_blocks = bps[0]['unpaid_blocks']
        if self.count % 64 == 0:
            if current_unpaid_blocks - self.bp.unpaid_blocks >= 12:
                self.bp.unpaid_blocks = current_unpaid_blocks
                self.count = 0
                return True
            elif current_unpaid_blocks - self.bp.unpaid_blocks < 0:
                self.bp.unpaid_blocks = current_unpaid_blocks
                self.count = 0
                return True
            else:
                self.count = 0
                return False
        return True

    def monitor(self):
        self.check_is_top21()
        self.send_message()

        if self.bp.is_top21 is True:
            if self.check_is_producing():
                msg = '%s in good condition :) @%s' % (
                    BP_NAME, get_current_time())
                print('produing....', get_current_time())
                send_message(msg)
            else:
                msg = '%s DOWN :( @%s' % (BP_NAME, get_current_time())
                print('down...', get_current_time())
                send_message(msg)
                call()

    def send_message(self):
        if self.bp.is_top21 is False:
            msg = 'bp with name %s NOT FOUND!!! @ %s' % (
                BP_NAME, get_current_time())
            print("in is top21 ", get_current_time())
            send_message(msg)
        if self.bp.is_new_top21 is True:
            msg = 'Congratulations! %s become the new top 21 ! @ %s' % (
                BP_NAME, get_current_time())
            print('in is new top21', get_current_time())
            send_message(msg)
            call()
