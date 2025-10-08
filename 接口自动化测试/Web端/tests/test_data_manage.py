"""
web 数据管理
"""

from web.api.apicontroller import ApiController


class TestDeviceManageList:
    def setup_class(self):
        self.api = ApiController()

    def test_ProductWeatherData(self):
        payload = {"timeRange": ["2025-02-18", "2025-02-18"], "pageNum": 1, "pageSize": 10, "psId": "1913608",
                   "startTime": "2025-02-18", "endTime": "2025-02-18"}
        res = self.api.ProductWeatherCurveData(payload)
        assert res.status_code == 200

        resp = self.api.ProductWeatherDataList(payload)
        assert len(res.json()["data"]) == 12 and len(resp.json()["data"]) == 96

    def test_ProductPowerData(self):
        payload = {"timeRange": ["2025-02-18", "2025-02-18"], "pageNum": 1, "pageSize": 10, "psId": "1913608",
                   "forecastEndTime": "", "startTime": "2025-02-18", "endTime": "2025-02-18"}
        res = self.api.ProductPowerCurveData(payload)
        assert res.status_code == 200

        resp = self.api.ProductPowerDataList(payload)
        assert resp.json()["data"][48]["forecastPower"] == 7835.892 and res.json()["data"]["accuracy"][1][
            "accuracy"] == 97.79

    def test_ProductLoadData(self):
        payload = {"timeRange": ["2025-02-18", "2025-02-18"], "pageNum": 1, "pageSize": 10, "psId": "1913608",
                   "forecastEndTime": "", "startTime": "2025-02-18", "endTime": "2025-02-18"}

        res = self.api.ProductLoadCurveData(payload)
        assert res.status_code == 200

        resp = self.api.ProductLoadDataList(payload)
        assert resp.json()["data"][0]["forecastLoad"] == 4998.5996 and res.json()["data"]["accuracy"][1][
            "accuracy"] == 85.03

    def test_PriceType(self):
        res = self.api.PriceType()
        assert len(res.json()["data"]) == 13

    def test_PriceDataList(self):
        payload = {"pageNum": 1, "pageSize": 10}
        res = self.api.PriceDataList(payload)
        assert res.json()["data"]["total"] == "62"

    def test_Suggestion(self):  # 入参已别墅实证为例
        payload = {"callTime": "2025-02-18 08:00:00", "pageNum": 1, "pageSize": 10, "psId": "1913608"}
        res = self.api.Suggestion(payload)
        assert res.json()["data"]["costReduce"] == 3.99
