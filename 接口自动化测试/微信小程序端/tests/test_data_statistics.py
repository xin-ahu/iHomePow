
# -*- coding: utf-8 -*-

from .test_home_info import *


class TestDataStatistics:
    """能源预测"""
    def test_EnergyProductChart(self, Api, HomeInfo):
        HomeId, _ = HomeInfo
        res = Api.PowerLoadChart(HomeId)
        assert res.status_code == 200

    def test_GetSuggestion(self, Api, HomeInfo):
        HomeId, _ = HomeInfo
        res = Api.GetSuGGestion(HomeId)
        assert res.status_code == 200

    """数据统计"""
    def test_ElectricityStatistics(self, Api, HomeInfo):
        HomeId, _ = HomeInfo
        payloads = {"date": "2025-03-17", "dateType": 1, "homeId": HomeId}
        res = Api.ElectricityStatistics(payloads)
        assert res.json()["data"]["totalGenerate"] == "69800.00" and res.json()["data"]["totalUse"] == "28300.00"

        resp = Api.ElectricPowerTrendChart(payloads)
        response = Api.Income(payloads)
        assert resp.status_code == 200 and response.json()["data"]["incomeList"][-1]["income"] == "36.83"

    """分析报告"""
    def test_GetMonthReportTitle(self, Api, HomeInfo):
        HomeId, _ = HomeInfo
        payloads = {"homeId": HomeId}
        res = Api.GetMonthReportTitle(payloads)
        assert res.status_code == 200







