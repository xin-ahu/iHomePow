
# -*- coding: utf-8 -*-


from .test_home_info import *


class TestHomeData:
    """排行榜"""
    def test_GetRanking(self, Api, HomeInfo):
        HomeId, _ = HomeInfo
        res = Api.GetUserRanking(HomeId)
        assert res.status_code == 200

    """获取电站风暴模式"""
    def test_GetStormDetail(self, Api, HomeInfo):
        HomeId, _ = HomeInfo
        payloads = {"homeId": HomeId}
        res = Api.GetStormDetail(payloads)
        res.raise_for_status()
        assert res.status_code == 200

    """刷新首页数据"""
    def test_GetRefreshIndexInfo(self, Api, HomeInfo):
        HomeId, _ = HomeInfo
        res = Api.GetRefreshIndexInfo(HomeId)
        res.raise_for_status()
        assert res.status_code == 200

    """是否存在6大类设备"""
    def test_IntelligentExperience(self, Api, HomeInfo):
        HomeId, _ = HomeInfo
        res = Api.IntelligentExperience(HomeId)
        res.raise_for_status()
        assert res.status_code == 200

    # 智能助手问题推荐查询
    def test_IntelligentAssistant(self, Api, HomeInfo):
        HomeId, _ = HomeInfo
        payloads = {"homeId": HomeId, "pageNum": 1, "pageSize": 10}
        res = Api.IntelligentAssistant(payloads)
        res.raise_for_status()
        assert res.status_code == 200 and res.json()["data"]["total"] == "12"

    # 智能助手消息推送
    def test_message(self, Api, HomeInfo):
        HomeId, _ = HomeInfo
        res = Api.message(HomeId)
        res.raise_for_status()
        assert res.status_code == 200


    
