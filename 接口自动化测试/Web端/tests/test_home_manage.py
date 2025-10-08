"""
web 家庭管理列表
"""
import pytest
import requests
from web.config.url import login_url, payload, header
from web.api.apicontroller import ApiController


@pytest.fixture(scope="class")
def GetDeptId():
    res = requests.post(url=login_url, json=payload, headers=header)
    res.raise_for_status()
    return res.json()["data"]["deptId"]


class TestHomeManageList:
    def setup_class(self):
        self.api = ApiController()

    def test_GetHomeList(self):
        payloads = {"pageNum": 1, "pageSize": 20, "name": ""}
        res = self.api.GetHomeList(payloads)
        HomeList = res.json()["data"]["list"]
        # homeId = [int(i["id"]) for i in HomeList]
        assert len(HomeList) > 0
        print(int(HomeList[0]["id"]))

    def test_GetHomeDetails(self):
        homeId = self.test_GetHomeList()
        res = self.api.GetHomeDetails(homeId)
        assert res.status_code == 200

    def test_GetUserConfig(self):
        homeId = self.test_GetHomeList()
        res = self.api.GetUserConfig(homeId)
        assert res.status_code == 200

    def test_PowerStationList(self):
        payloads = {"pageNum": 1, "pageSize": 20, "name": ""}
        res = self.api.PowerStationList(payloads)
        assert res.status_code == 200

    def test_PowerDetails(self):
        payloads = {"timeRange": ["2025-03-17", "2025-03-17"], "pageNum": 1, "pageSize": 10, "psId": "1761299",
                    "startTime": "2025-03-17", "endTime": "2025-03-17"}
        res = self.api.PowerDetails(payloads)
        assert res.status_code == 200 and res.json()["data"]["p13130"][0] == 3848700 or res.json()["data"]["p13134"][0] == 3804700

    def test_ChargingStationList(self):
        payloads = {"pageNum": 1, "pageSize": 20, "name": "", "deptId": "103"}
        res = self.api.ChargingStationList(payloads)
        assert res.status_code == 200 and res.json()["data"]["list"][0]["deviceSn"] == "A241150480301"

    def test_RoomList(self):
        payloads = {"pageNum": 1, "pageSize": 20, "name": ""}
        res = self.api.RoomList(payloads)
        assert res.status_code == 200
