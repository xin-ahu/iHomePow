# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2025/4/17 17:54
# @Author: wangxin16
# @Email: wangxin16@sungrowpower.com

"""
成本计算
"""
import json
import logging
# -*- coding: utf-8 -*-

from datetime import datetime
from get_related_data import GetStationData, sum_hour_power
from get_charge_rate import rate_range, get_rate
from recalculate_no_upgrid import recalculate_no_upgrid

logging.basicConfig(filename='income.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s', encoding='utf-8')


def get_soc(stationData, callTime):
    try:
        for i in stationData["socReality"]:
            if i["dataTime"] >= callTime:
                soc_i = i["realityLoad"]
                return soc_i
    except Exception as e:
        print(f"{e}")


def get_battery_model(BatteryModel):
    device_model = BatteryModel[:3]
    return device_model


def predictionPowerDay(stationData):  # 日预测发电量
    hour_power = sum_hour_power(stationData["pvPrediction"])
    Power_generation = sum(item["forecastPower"] for item in hour_power)
    return Power_generation


def generationPowerAndLoad(stationData, callTime):
    Power_list = []
    Load_list = []

    request_time = datetime.strptime(callTime, "%Y-%m-%d %H:%M:%S")
    hour_power = sum_hour_power(stationData["pvPrediction"])
    for i in range(len(hour_power)):
        dataTime = datetime.strptime(hour_power[i]["dataTime"], "%Y-%m-%d %H:%M:%S")
        if dataTime >= request_time:
            Power_list.append({
                "dataTime": hour_power[i]["dataTime"],
                "forecastPower": hour_power[i]["forecastPower"]
            })
            Load_list.append({
                "dataTime": dataTime.strftime("%Y-%m-%d %H:%M:%S"),
                "forecastLoad": stationData["loadPrediction"][i]["forecastLoad"]
            })

    return Power_list, Load_list


def calculatePowerOutage(temperature, BatteryCapac, pcmax, soc, battery_device_model, PowerList, loadList):
    grid_list = []
    Soc = [soc]
    for i in range(len(PowerList)):
        surplus = PowerList[i]["forecastPower"] - loadList[i]["forecastLoad"]
        if surplus >= 0:
            Pcmax_i = get_rate(temperature, rate_range(battery_device_model)) * pcmax
            max_bess_in_now = min(Pcmax_i, (1 - Soc[i]) * (BatteryCapac * 1000))
            bess = min(max_bess_in_now, surplus)
        else:
            max_bess_in_now = max(-pcmax, -Soc[i] * (BatteryCapac * 1000))
            bess = max(max_bess_in_now, surplus)
        Soc.append(Soc[i] + (bess / (BatteryCapac * 1000)))

        grid = surplus - bess
        if grid > 0:
            grid_list.append(grid)
    return grid_list


def bess_income(stationData, ef, BatteryCapac):
    # 当日00:00点, 23：55分SOC 差值
    actual_soc = stationData["socReality"][-1].get("realityLoad") - stationData["socReality"][0].get("realityLoad")
    submit_soc = stationData["moveSocReality"][-1].get("realityLoad") - stationData["moveSocReality"][0].get(
        "realityLoad")
    if stationData["priceDetail"]["touType"]:
        price = stationData["priceDetail"]["touPrice"][1]["price"][-1]
    else:
        price = stationData["priceDetail"]["price"]
    actual_income = round(((actual_soc * BatteryCapac) * price) * ef, 4)
    submit_income = round(((submit_soc * BatteryCapac) * price) * ef, 4)
    return actual_income, submit_income


def calculateIncome(stationData, up_grid_price, priceDetail):
    def grid_down_price(data_time_str, touPrice, touType):
        def parse_time(time_str):
            return datetime.strptime(time_str, "%H:%M").time()

        if touType:
            data_time = datetime.strptime(data_time_str, "%Y-%m-%d %H:%M:%S")
            data_time_obj = parse_time(data_time.strftime("%H:%M"))
            for tou_price in touPrice:
                for time in tou_price['time']:
                    start_time, end_time = time.split('-')
                    if end_time == "24:00":
                        end_time = "23:59"
                    start_time_obj = parse_time(start_time)
                    end_time_obj = parse_time(end_time)
                    if start_time_obj <= data_time_obj < end_time_obj:
                        grid_price = tou_price["price"][-1]
                        return grid_price
        else:
            grid_price = priceDetail["price"]
            return grid_price

    return [
        round(((item["realityLoad"] * 0.001) * (grid_down_price(item["dataTime"], priceDetail["touPrice"], priceDetail["touType"]) if item["realityLoad"] >= 0 else up_grid_price)) / 12, 4)
        for item in stationData
    ]


if __name__ == '__main__':
    call_Time = "2025-04-28 08:00:00"
    psId = "1966080"  # 华夏：1729566  阳光T：1761299  湖南：1636317   合肥实证：1913608  北京实证：1966080 苏州实证：1995574
    # homeId = "1859885290689269"
    call_date = call_Time.split(" ")[0]
    dateType = 1
    ef = 0.95
    data = GetStationData()

    # rate = data.GetTotalGenerateRate(call_date, dateType, homeId)
    print(f"调用时间：{call_Time}")
    # print(f"自发自用率：{rate}")

    """ 电池容量"""
    Battery = data.GetBatteryCapac(psId)
    """ 电站数据"""
    station_data = data.GetStationData(call_Time, psId)
    print(station_data['connectType'])
    # 调用无馈网情况下功率计算
    if station_data['connectType'] == 3:
        station_data = recalculate_no_upgrid(station_data)

    """ 温度值 """
    temper = data.get_temperature(call_Time, psId)
    """ 储能型号 """
    BatteryDeviceModel = data.GetBatteryModel(psId)
    battery_model = get_battery_model(BatteryDeviceModel)
    """ 储能最大充电功率"""
    BatteryMaxOutput = data.GetBatteryMaxOutput(psId)

    """ 调用时间SOC"""
    soc = get_soc(station_data, call_Time)
    PowerGeneration = predictionPowerDay(station_data)
    print(f"当日发电量约：{(PowerGeneration / 1000):.2f}")

    power_list, load_list = generationPowerAndLoad(station_data, call_Time)
    sum_grid = calculatePowerOutage(temper, Battery, BatteryMaxOutput, soc, battery_model, power_list, load_list)
    print(f"当日总馈网：{sum(sum_grid) / 1000:.2f}")

    actual_soc_income, submit_soc_income = bess_income(station_data, ef, Battery)

    # 建议前电网功率和储能SOC差值
    # print("建议前电网功率: ", station_data["gridReality"])
    print("建议前SOC差值: ", station_data["socReality"][-1].get("realityLoad") - station_data["socReality"][0].get("realityLoad"))

    # 建议前成本
    sum_income = sum(calculateIncome(station_data["gridReality"], station_data["priceDetail"]["gridPurchasePrice"], station_data["priceDetail"]))
    sum_income -= actual_soc_income
    print(f"建议前成本：{sum_income:.4f}")

    # 建议后电网功率和储能SOC差值
    # print("建议后电网功率: ", station_data["moveGridReality"])
    print("建议后SOC差值: ", station_data["moveSocReality"][-1].get("realityLoad") - station_data["moveSocReality"][0].get("realityLoad"))

    # 建议后成本
    sum_submitAfter_income = sum(calculateIncome(station_data["moveGridReality"], station_data["priceDetail"]["gridPurchasePrice"], station_data["priceDetail"]))
    sum_submitAfter_income -= submit_soc_income
    print(f"建议后成本：{sum_submitAfter_income:.4f}")

    # 降本
    cost_reduction = sum_income - sum_submitAfter_income
    print(f"降本：{cost_reduction:.4f}")
