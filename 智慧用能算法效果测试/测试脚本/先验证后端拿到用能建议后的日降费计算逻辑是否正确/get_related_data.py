"""
数据
"""
# -*- coding: utf-8 -*-
from datetime import datetime
from collections import defaultdict
import requests
from HttpClient import HttpClient
from connect_database import ConnectMySql
from decimal import Decimal



def payloads(callTime, psId):
    return {
        "callTime": callTime,
        "pageNum": 1,
        "pageSize": 10,
        "psId": psId,
    }


def payloads_app(callDate, dateType, homeId):
    return {
        "date": callDate,
        "dateType": dateType,
        "homeId": homeId
    }


def t_payload(reqrest_time, psId):
    Time = reqrest_time.split(" ")[0]
    return {
        "timeRange": [Time, Time],
        "pageNum": 1,
        "pageSize": 10,
        "psId": psId,
        "startTime": Time,
        "endTime": Time
    }


def sum_hour_power(data):
    sum_power = defaultdict(float)
    for item in data:
        time = datetime.strptime(item["dataTime"], "%Y-%m-%d %H:%M:%S")
        hour = time.strftime("%Y-%m-%d %H")
        sum_power[hour] += item["forecastPower"]

    hour_data = [{'dataTime': f"{hour}:00:00", 'forecastPower': (power / 4)} for hour, power in sum_power.items()]
    return hour_data


class GetStationData:
    def __init__(self):
        self.client = HttpClient()
        self.db = ConnectMySql()
        self.db.connect()

    """ 储能容量 """
    def GetBatteryCapac(self, psId):
        sql = ("select co.value from ihome_prod.sys_power_station pw inner join ihome_prod.sys_user_config co "
               "on pw.home_id = co.home_id where pw.id = '{}' and co.code= 'battery_power'").format(psId)
        results = self.db.query(sql)
        # print(results)
        BatteryCapac = float(results[0]["value"])
        return BatteryCapac

    """ 储能型号"""
    def GetBatteryModel(self, psId):
        sql = "SELECT t.device_model_code FROM ihome_prod.sys_power_device t WHERE ps_id='{}' AND device_name='扩容式储能'".format(psId)
        results = self.db.query(sql)
        BatteryModel = results[0]["device_model_code"]
        return BatteryModel

    """ 储能最大充电功率"""

    def GetBatteryMaxOutput(self, psId):
        sql = (
            "SELECT us.value FROM ihome_prod.sys_user_config us WHERE us.code = 'battery_max_output' AND us.home_id = (SELECT pw.home_id FROM ihome_prod.sys_power_station pw WHERE pw.id = '{}')").format(psId)
        results = self.db.query(sql)
        BatteryMaxOutput = int(float(results[0]["value"]) * 1000)
        return BatteryMaxOutput

    """ 电站数据 """
    def GetStationData(self, callTime, psId):
        try:
            res = self.client.post("/simulate/genSuggestion", json=payloads(callTime, psId))
            res.raise_for_status()
            data = res.json().get("data", {})
            return data
        except requests.RequestException as e:
            print(f"获取数据失败{e}")

    def GetTotalGenerateRate(self, callDate, dateType, homeId):
        try:
            res = self.client.post_app("/admin/ps/query/power", json=payloads_app(callDate, dateType, homeId))
            res.raise_for_status()
            data = res.json()["data"]
            totalGenerateRate = ((Decimal(data["totalGenerate"]) - Decimal(data["feedPower"])) / Decimal(data["totalGenerate"])) * 100
            formatted_rate = f"{totalGenerateRate:.2f}%"
            return formatted_rate
        except requests.RequestException as e:
            print(f"获取数据失败{e}")

    """ 温度 """
    def get_temperature(self, callTime, psId):
        try:
            res = self.client.post("/weatherData/chart", json=t_payload(callTime, psId))
            res.raise_for_status()
            data = res.json().get("data", {})

            temperature_list = [
                {"times": data["times"][i], "temperature2m": data["temperature2m"][i]}
                for i in range(min(96, len(data.get("times", []))))
            ]

            request_time_dt = datetime.strptime(callTime, "%Y-%m-%d %H:%M:%S")

            for i in temperature_list:
                times = i["times"]
                times_dt = datetime.strptime(times, "%Y-%m-%d %H:%M:%S")
                if times_dt >= request_time_dt:
                    temperature = i["temperature2m"] + 10
                    return temperature
                else:
                    continue
        except requests.RequestException as e:
            print(f"获取数据失败{e}")



