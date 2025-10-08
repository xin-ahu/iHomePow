

from datetime import datetime
from SimulatePowerStation.payloads.ExtremeWeatherDate import ExtremeWeather_payload
from api_controller import Api_Controller
import logging

logging.basicConfig(filename='Extreme_weather_log.log', level=logging.INFO, format='%(asctime)s - %(message)s')


class Extreme:
    def __init__(self):
        self.client = Api_Controller()

    def request(self, status, startTime, psId):
        payload = ExtremeWeather_payload(status, startTime, psId)
        res = self.client.Extreme_weather(payload)
        print(res.request.body.decode('unicode_escape'))
        res.raise_for_status()
        logging.info(f'入参{payload}, {res.text}')


if __name__ == '__main__':
    re = Extreme()
    statu = 2   # 0 发布  1 更新  2 解除
    start_Time = datetime.now()
    ps_Id = '1761299'   # 1660136     # 1761299  # 1913608 别墅实证

    re.request(statu, start_Time, ps_Id)

