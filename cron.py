import schedule
import time

from monitor import monitor_producer
from config import BP_NAME
from bp import BP
from api import get_info

info = get_info()
head_block_num = info['head_block_num']

bp = BP(BP_NAME, False, False, head_block_num)
schedule.every(2).seconds.do(monitor_producer, bp)

while True:
    schedule.run_pending()
    time.sleep(1)
