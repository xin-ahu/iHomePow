"""
web 系统管理
"""

from web.api.apicontroller import ApiController


class TestSystemManage:
    def setup_class(self):
        self.api = ApiController()

    def test_DeptMentList(self):
        res = self.api.DeptMentList()
        assert res.status_code == 200

    def test_userList(self):
        res = self.api.UserList()
        assert res.status_code == 200

    def test_Adduser(self):
        payload = {"deptId": "105", "userName": "测试用户", "loginName": "sungrow-100", "phonenumber": "13500006666",
                   "sex": "0", "status": "0", "postIds": [], "roleIds": ["2"]}
        res = self.api.AddUser(payload)
        assert res.status_code == 200
