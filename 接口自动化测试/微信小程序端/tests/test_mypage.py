
# -*- coding: utf-8 -*-

from .test_home_info import *


class TestMyPage:
    """电站配置"""
    def test_GetStationConfig(self, Api, user_Id, HomeInfo):
        userId, _, _ = user_Id
        HomeId, _ = HomeInfo
        res = Api.GetStationConfig(userId, HomeId)
        assert res.status_code == 200 and res.json()["data"][0]["value"] == "15"

    """问题反馈"""
    def test_ProblemFeedback(self, Api, user_Id, HomeInfo):
        userId, _, _ = user_Id
        HomeId, _ = HomeInfo
        payloads = {"userId": userId, "content": "输入反馈问题内容",
                    "picList": [
                        "https://ihome-sungrow.oss-cn-hangzhou.aliyuncs.com/iHome/feedback/WkxUolkUuDx9e0637554f93c454b0c84b72ebe8a47c2.jpg"],
                    "homeId": HomeId}
        res = Api.ProblemFeedback(payloads)
        assert res.status_code == 200

    """反馈列表"""
    def test_ProblemFeedbackList(self, Api, user_Id):
        userId, _, _ = user_Id
        res = Api.ProblemFeedbackList(userId)
        assert res.status_code == 200

    """权限"""
    def test_DevicePurviewConfig(self, Api, user_Id, HomeInfo):
        userId, _, _ = user_Id
        HomeId, _ = HomeInfo
        payloads = {"userId": userId, "homeId": HomeId, "code": "device_permission", "value": "true"}
        res = Api.DevicePurviewConfig(payloads)
        assert res.status_code == 200

    """退出"""
    def test_Logout(self, Api, user_Id):
        userId, _, loginName = user_Id
        payloads = {"loginName": loginName}
        res = Api.Logout(payloads)
        assert res.status_code == 200
