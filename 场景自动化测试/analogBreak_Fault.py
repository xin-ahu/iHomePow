import json
from datetime import datetime, timedelta
import random
from SimulatePowerStation.apicontroller.api_controller import Api_Controller
import logging

# 01010  过压告警
# 01011  欠压告警
# 10000  漏电告警   alarm
# 10101  过流告警

# 00010  漏电关断  type： displace


logging.basicConfig(filename='analogBreak_Fault.log', level=logging.INFO, format='%(asctime)s - %(message)s')


def BreakAlarm_payload(statTime):
    payload = {
        "changeBP1": 204.5,
        "changeBP2": "010",
        "changeBP3": 0.0,
        "changeBP4": 0.0,
        "changeBP5": 0.0,
        "changeBP6": 219.60000000000002,
        "changeBP7": 204.5,
        "changeBP8": 219.8,
        "changeBP9": 0.0,
        "deviceId": "865866060290978000",
        "deviceType": "65",   # 64: 常规， 65： 重要
        "displaceType": "01010",
        "displaceRet": "01010",
        "recordNums": 0,
        "recordSeq": 0,
        "startTime": statTime.strftime("%Y-%m-%d %H:%M:%S"),
        "statTime": statTime.strftime("%Y-%m-%d %H:%M:%S"),
        "type": "alarm"
    }
    return payload

#


class BreakFault:
    def __init__(self):
        self.client = Api_Controller()
        self.startTime = datetime.now()

    def request(self):
        res = self.client.BreakFault(payload=BreakAlarm_payload(self.startTime))
        res.raise_for_status()
        logging.info(f"{res.text}")


if __name__ == '__main__':
    bf = BreakFault()
    bf.request()