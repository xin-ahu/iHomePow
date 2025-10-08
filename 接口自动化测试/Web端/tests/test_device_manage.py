"""
web 设备管理
"""
import time
from web.api.apicontroller import ApiController


class TestDeviceManageList:
    def setup_class(self):
        self.api = ApiController()

    def test_ProductManageList(self):
        res = self.api.ProductManageList()
        res.raise_for_status()
        assert res.status_code == 200

    def test_AddProduct(self):  # 按需调
        payload = {
            "parentId": "1850047367035707394", "productName": "测试",
            "productCode": "1000000", "model": "SH6.0RR", "ratedPower": "6000",
            "price": "555", "type": "2", "scene": "1", "status": "Y", "pic": ""
        }
        res = self.api.AddProduct(payload)
        assert res.status_code == 200

    def test_EditProduct(self):
        current_timestamp = int(time.time())
        payload = {
            "searchValue": None, "dataScope": None, "pageNum": 0, "pageSize": 0, "orderByColumn": None, "isAsc": None,
            "startTime": None, "endTime": None, "createBy": "1", "createUser": None, "createTime": 1741831358000,
            "updateBy": "1", "updateTime": current_timestamp, "remark": None, "id": "1900004542068858881",
            "productName": "测试", "productCode": "1000000", "price": 555, "parentId": "1850047367035707394",
            "spec": None,
            "ratedPower": 6000, "model": "SH6.0RR", "type": "2", "scene": "1", "pic": "", "metadata": None,
            "protocol": None,
            "createName": None, "updateName": None, "status": "Y"
        }
        res = self.api.EditProduct(payload)
        assert res.status_code == 200

    def test_StationDeviceList(self):  # deptId 按需调整
        payload = {"pageNum": 1, "pageSize": 10, "homeId": "", "deviceName": "", "deptId": "103"}
        res = self.api.StationDeviceList(payload)
        assert res.status_code == 200

    def test_ChargingDeviceList(self):
        payload = {"pageNum": 1, "pageSize": 10, "homeId": "", "equipmentName": "", "deptId": "103"}
        res = self.api.ChargingDeviceList(payload)
        assert res.status_code == 200

    def test_RoomDeviceList(self):
        payload = {"pageNum": 1, "pageSize": 10, "homeId": "", "name": "", "deptId": "103"}
        res = self.api.RoomDeviceList(payload)
        assert res.status_code == 200
