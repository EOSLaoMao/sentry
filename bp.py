from api import *


class BP:
    def __init__(self, name, is_top21, head_block_num):
        self.name = name
        self.is_top21 = is_top21
        self.is_new_top21 = False
        self.last_produce_block_num = head_block_num

    def check_is_top21(self):
        prods = get_producers()
        print('There are %d BPs' % len(prods))
        bps = [bp for bp in prods if bp['owner'] == self.name]
        if len(bps) == 0:
            self.is_top21 = False
        else:  # in top 21 bp list
            if self.is_top21 is False:
                self.is_new_top21 = True
            else:
                self.is_new_top21 = False
            self.is_top21 = True

    def check_is_producing(self):
        if self.is_top21 is True:
            info = get_info()
            head_block_producer = info['head_block_producer']
            head_block_num = info['head_block_num']
            if head_block_producer is self.name:
                self.last_produce_block_num = head_block_num

            if head_block_num - self.last_produce_block_num > 252 * 2:
                return False
            else:
                return True
