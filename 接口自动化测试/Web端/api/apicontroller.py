"""
web端 Api接口地址
"""


from web.common.HttpClient import HttpClient


class ApiController:
    def __init__(self):
        self.client = HttpClient()

    # 查询用户信息
    def GetUserInfo(self):
        return self.client.get("/system/user/getInfo")

    # 查询栏目
    def GetColumn(self):
        return self.client.get("/system/menu/getRouters")

    # 首页数据
    def HomePageData(self):
        return self.client.post("/ps/webIndexInfo")

    # 查询用户地址
    def GetMapHomesAddress(self):
        return self.client.post("/ps/mapHomes")

    # 家庭管理列表
    def GetHomeList(self, payload):
        return self.client.post("/home/list", json=payload)

    # 家庭详情
    def GetHomeDetails(self, homeId):
        return self.client.get(f"/home/getHomeInfoById?homeId={homeId}")

    # 家庭配置
    def GetUserConfig(self, homeId):
        return self.client.get(f"/userConfig/getConfig?homeId={homeId}")

    # 电站列表
    def PowerStationList(self, payload):
        return self.client.post("/home/powerStationList", json=payload)

    # 电站详情功率
    def PowerDetails(self, payload):
        return self.client.post("/ps/power/realtimeChart", json=payload)

    # 充电站列表
    def ChargingStationList(self, payload):
        return self.client.post("/home/chargeStationList", json=payload)

    # 房间列表
    def RoomList(self, payload):
        return self.client.post("/home/roomList", json=payload)

    # 产品管理
    def ProductManageList(self):
        return self.client.post("/product/getAllProd?")

    # 添加产品
    def AddProduct(self, payload):
        return self.client.post("/product/add", json=payload)

    # 编辑产品
    def EditProduct(self, payload):
        return self.client.put("/product/edit", json=payload)

    # 电站设备管理
    def StationDeviceList(self, payload):
        return self.client.post("/pd/getAllDevices", json=payload)

    # 充电设备管理
    def ChargingDeviceList(self, payload):
        return self.client.post("/charge/getAllDevices", json=payload)

    # 房间设备管理
    def RoomDeviceList(self, payload):
        return self.client.post("/roomDevice/getAllDevices", json=payload)

    # 气象数据
    def ProductWeatherCurveData(self, payload):
        return self.client.post("/weatherData/chart", json=payload)

    def ProductWeatherDataList(self, payload):
        return self.client.post("/weatherData/list", json=payload)

    # 功率数据
    def ProductPowerCurveData(self, payload):
        return self.client.post("/powerData/chart", json=payload)

    def ProductPowerDataList(self, payload):
        return self.client.post("/powerData/list", json=payload)

    # 负荷数据
    def ProductLoadCurveData(self, payload):
        return self.client.post("/loadData/chart", json=payload)

    def ProductLoadDataList(self, payload):
        return self.client.post("/loadData/list", json=payload)

    # 电价数据
    def PriceType(self):
        return self.client.get("/system/dict/data/type/price_type")

    def PriceDataList(self, payload):
        return self.client.post("/price/list", json=payload)

    # 智能建议
    def Suggestion(self, payload):
        return self.client.post("/simulate/genSuggestion", json=payload)

    # 用户管理-部门列表
    def DeptMentList(self):
        return self.client.get("/system/user/deptTree")

    # 用户管理-用户列表
    def UserList(self):
        return self.client.get("/system/user/list?pageNum=1&pageSize=10")

    # 新增用户
    def AddUser(self, payload):
        return self.client.post("/system/user", json=payload)

