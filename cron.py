import schedule
import time

from monitor import monitor_producer
from config import BP_NAME, IS_TOP_21
from bp import BP
from api import get_info

info = get_info()
head_block_num = info['head_block_num']

is_top21 = False
if IS_TOP_21 == "True":
    is_top21 = True

print("is_top_21", is_top21)
bp = BP(BP_NAME, is_top21, head_block_num)
schedule.every(2).seconds.do(monitor_producer, bp)

while True:
    schedule.run_pending()
    time.sleep(1)
