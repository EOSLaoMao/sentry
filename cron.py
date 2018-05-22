import schedule
import time

from monitor import monitor_producer

schedule.every(2).seconds.do(monitor_producer)

while True:
    schedule.run_pending()
    time.sleep(1)
