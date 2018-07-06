import schedule
import time

from monitor import BPMonitor
from config import BP_NAME, IS_TOP_21
from bp import BP
from api import get_info


is_top21 = False
if IS_TOP_21 == "True":
    is_top21 = True

print("is_top_21", is_top21)
bp = BP(BP_NAME, is_top21)
bp_monitor = BPMonitor(bp)

schedule.every(2).seconds.do(bp_monitor.monitor)

while True:
    schedule.run_pending()
    # time.sleep(1)
