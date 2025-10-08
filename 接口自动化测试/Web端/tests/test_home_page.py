"""
首页
"""
import pytest
from web.api.apicontroller import ApiController


# @pytest.fixture(scope="class")
# def api():
#     return ApiController()


class TestHomePage:
    def setup_class(self):
        self.api = ApiController()

    # 查询用户信心
    def test_GetUserInfo(self):
        res = self.api.GetUserInfo()
        assert res.status_code == 200

    # 查询栏目
    def test_GetColumn(self):
        res = self.api.GetColumn()
        assert res.status_code == 200

    # 首页数据统计
    def test_HomePageData(self):
        res = self.api.HomePageData()
        assert res.status_code == 200

    # 获取家庭
    def test_MapHomesAddress(self):
        res = self.api.GetMapHomesAddress()
        assert res.status_code == 200


