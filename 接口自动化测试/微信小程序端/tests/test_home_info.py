
# -*- coding: utf-8 -*-

import pytest
from app.apicontroller.apicontroller import ApiController
from app.config.url import payload


@pytest.fixture(scope="class")
def Api():
    return ApiController()


@pytest.fixture(scope="class")
def user_Id(Api):
    try:
        res = Api.GetUserId(payload)
        assert res.status_code == 200
        data = res.json()['data']
        return data["userId"], data["deptId"], data["loginName"]
    except Exception as e:
        pytest.fail(f"获取用户userId失败: {e}")


@pytest.fixture(scope="class")
def HomeInfo(Api, user_Id):  # 以阳光新能源T电站HomeId
    userId, _, _ = user_Id
    try:
        res = Api.GetHome(userId)
        assert res.status_code == 200 and res.json()["data"][2]["id"] == "1859885290689269"
        data = res.json()['data']
        return data[2]["id"], data[2]["tuyaHomeid"]
    except Exception as e:
        pytest.fail(f"获取用户HomeId, tuyaHomeid失败: {e}")
