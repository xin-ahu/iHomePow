
# -*- coding: utf-8 -*-


from .test_home_info import *


class TestDeviceList:
    """设备列表"""
    def test_GetHomeDeviceList(self, Api, HomeInfo):
        HomeId, _ = HomeInfo
        res = Api.GetHomeDeviceList(HomeId)
        res.raise_for_status()
        assert res.status_code == 200

    """充电桩详情 入参暂时固定A2411504803"""
    def test_ChargingDetail(self, Api):
        res = Api.GetDeviceDetail()
        assert res.status_code == 200 and res.json()["data"]["status"] == "Y"

    """组件详情"""
    def test_DevDetail(self, Api):
        res = Api.GetDevDetail()
        assert res.status_code == 200 and res.json()["data"]["ps_key"] == "1761299_14_1_1" and res.json()["data"]["ratedPower"] == 15

    """添加自动化"""
    def test_AddSceneRule(self, Api):
        payloads = {"homeId": "1859885290689269", "userId": "15", "name": "ceshi", "conditionsObject": [
            {"entityType": "power",
             "expr": {"comparator": "==", "powerCode": "surplusPower", "powerValue": "0.01-0.2"}}],
                    "actionsObject": [
                        {"entityId": "6cac23292ba2e9a1c2barh", "actionExecutor": "device_issue",
                         "executorProperty": {"durationSeconds": "0", "functionCode": "switch_1",
                                              "functionValue": False}}],
                    "effectiveTimeObject": None, "status": "Y"}
        res = Api.AddSceneRule(payloads)
        res.raise_for_status()
        assert res.status_code == 200

    """自定义列表"""
    def test_GetSceneRuleList(self, Api, HomeInfo):
        HomeId, _ = HomeInfo
        payloads = {"homeId": HomeId}
        res = Api.GetSceneRule(payloads)
        assert res.status_code == 200

    






