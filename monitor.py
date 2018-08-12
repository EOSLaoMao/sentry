import datetime
from telegram import send_message
from config import BP_NAME
from phone import call
from api import get_producers, get_table
from gce import LogResolver


def get_current_time():
    current_time = str(datetime.datetime.now())
    return current_time


class BPMonitor:
    def __init__(self, bp):
        self.bp = bp
        self.producing_count = 0
        self.notify_count = 0
        self.latency_count = 0
        self.lr = LogResolver()

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
        self.producing_count += 1
        prods = get_table()
        bps = [bp for bp in prods if bp['owner'] == self.bp.name]
        current_unpaid_blocks = 0
        if len(bps) != 0:
            current_unpaid_blocks = bps[0]['unpaid_blocks']
        if self.producing_count % 64 == 0:
            if current_unpaid_blocks - self.bp.unpaid_blocks >= 12:
                self.bp.unpaid_blocks = current_unpaid_blocks
                self.producing_count = 0
                return True
            elif current_unpaid_blocks - self.bp.unpaid_blocks < 0:
                self.bp.unpaid_blocks = current_unpaid_blocks
                self.producing_count = 0
                return True
            else:
                self.producing_count = 0
                return False
        return True

    def check_latency(self):
        self.latency_count += 1
        if self.latency_count % 30 == 0:  # call every one minute
            latency = self.lr.get_latency()
            if latency != -1:
                if 2000 < latency <= 4000:
                    msg = "bp %s's latency %s ms is too high !!! @ %s" % (
                        BP_NAME, latency, get_current_time())
                    print(msg)
                    send_message(msg)
                    self.latency_count = 0
                elif latency > 4000:
                    msg = "bp %s is stucking now. The latency is %s ms !!! @ %s" % (
                        BP_NAME, latency, get_current_time())
                    print(msg)
                    send_message(msg)
                    self.latency_count = 0
                    call()
                elif 0 < latency <= 2000:
                    msg = "bp %s has normal latency %s ms!!! @ %s" % (
                        BP_NAME, latency, get_current_time())
                    print(msg)
                    send_message(msg)
                    self.latency_count = 0
                else:
                    self.latency_count = 0

    def monitor(self):
        self.check_is_top21()
        self.check_latency()

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
        if self.bp.is_top21 is True:
            self.notify_count += 1
            if self.notify_count % 64 == 0:
                if self.check_is_producing():
                    msg = '%s in good condition :) @%s' % (
                        BP_NAME, get_current_time())
                    print('produing....', get_current_time())
                    self.notify_count = 0
                    send_message(msg)
                else:
                    msg = '%s DOWN :( @%s' % (BP_NAME, get_current_time())
                    print('down...', get_current_time())
                    send_message(msg)
                    call()
