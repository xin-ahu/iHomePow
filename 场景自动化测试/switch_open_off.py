import schedule
import time
from datetime import datetime
import logging
from app.common.Http import Http

logging.basicConfig(filename='switch_log.log', level=logging.INFO, format='%(asctime)s - %(message)s')


class Socket_switch:
    def __init__(self):
        self.client = Http()

    def request(self, payload, devId):
        try:
            res = self.client.post(f'/tuya/device/control/{devId}', json=payload)
            if res.status_code == 200:
                return True
            else:
                logging.error(f"状态码:{res.status_code}")
                return False

        except Exception as e:
            logging.error(f"请求异常: {e}")
            return False


if __name__ == '__main__':
    re = Socket_switch()
    # 插座设备Id
    deviceId = '6c8f630fa0af335c0aznoo'

    deviceId_list = ['6c8cda9347b47a2c9bpgf8', '6c8f630fa0af335c0aznoo', '6c23c6caa51afd297atavq']

    open_payload = [{"code": "switch_1", "value": True}]
    off_payload = [{"code": "switch_1", "value": False}]
    open_count = 0
    off_count = 0

    # schedule.every(1).minutes.do(job)

    while True:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # for deviceId in deviceId_list:
        # 开启
        re.request(open_payload, deviceId)
        open_count += 1
        logging.info(f"设备Id：{deviceId}, 开启时间{datetime.now()}, 带载累计次数: {open_count}")

        time.sleep(30)

        # 关闭
        re.request(off_payload, deviceId)
        off_count += 1
        logging.info(f"关闭时间{datetime.now()}, 累计次数: {off_count}")

        time.sleep(30)

