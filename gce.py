# Imports the Google Cloud client library
from google.cloud import logging
from google.cloud.logging import DESCENDING
import re


class LogResolver:
    def __init__(self):
        self.logging_client = logging.Client()
        # log_name = 'projects/eoslaomao/logs/nodeos'
        # self.logger = logging_client.logger(log_name)

    def get_latency(self):
        try:
            FILTER = 'logName:nodeos'
            for entry in self.logging_client.list_entries(filter_=FILTER, order_by=DESCENDING):
                print(entry.payload)
                m = re.search(r"latency:\ (.*)\ ms", entry.payload)
                if hasattr(m, 'group'):
                    latency = m.group(0).split(" ")[1]
                    print("latency:" + latency + "ms")
                    return int(latency)
        except Exception as e:
            print(e)
            return -1
