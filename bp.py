from api import get_table
import datetime


class BP:
    def __init__(self, name, is_top21):
        self.name = name
        self.is_top21 = is_top21
        self.is_new_top21 = False
        self.unpaid_blocks = self.get_producer_table()

    def get_producer_table(self):
        prods = get_table()
        bps = [bp for bp in prods if bp['owner'] == self.name]
        if len(bps) != 0:
            return bps[0]['unpaid_blocks']
        else:
            return 0
