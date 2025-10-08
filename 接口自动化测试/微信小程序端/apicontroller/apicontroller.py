
from app.common.Http import HttpClient


class ApiController:
    def __init__(self):
        self.apiclient = HttpClient()

    def GetUserId(self, payload):
        return self.apiclient.post('/admin/user/apLogin', json=payload)

    """用户家庭列表"""
    def GetHome(self, userId):
        return self.apiclient.get(f'/admin/home/getHomeListByUserId?userId={userId}')

    """排行榜"""
    def GetUserRanking(self, HomeId):
        return self.apiclient.get(f"/admin/userRanking/getRanking?homeId={HomeId}")

    def GetStormDetail(self, payload):
        return self.apiclient.post("/admin/stormwatch/getStromDetail", json=payload)

    def GetRefreshIndexInfo(self, HomeId):
        return self.apiclient.post(f"/admin/ps/refreshIndexInfo?homeId={HomeId}")

    def IntelligentExperience(self, HomeId):
        return self.apiclient.post(f"/admin/device/exist/device?homeId={HomeId}")

    def IntelligentAssistant(self, payload):
        return self.apiclient.post("/admin/qa/recommendKnowledge", json=payload)

    def message(self, HomeId):
        return self.apiclient.post(f"/admin/qa/message?homeId={HomeId}&pageNum=1&pageSize=20")

    def GetHomeDeviceList(self, HomeId):
        return self.apiclient.get(f"/admin/device/getDevicesByHomeId?homeId={HomeId}")

    def GetDeviceDetail(self):
        return self.apiclient.get("/admin/charge/getDevDetail?equipmentId=A2411504803")

    """组件详情"""
    def GetDevDetail(self):
        return self.apiclient.post("/admin/ps/getDevDetail?pskey=1761299_22_247_1")

    """添加自定义"""
    def AddSceneRule(self, payload):
        return self.apiclient.post("/admin/sceneRule/add", json=payload)

    """自定义"""
    def GetSceneRule(self, payload):
        return self.apiclient.post('/admin/sceneRule/list', json=payload)

    """智能建议-能源预测"""
    def PowerLoadChart(self, HomeId):
        return self.apiclient.get(f"/admin/suggestion/selectPowerLoadChart?homeId={HomeId}")

    def GetSuGGestion(self, HomeId):
        return self.apiclient.get(f"/admin/suggestion/getSuggestion?homeId={HomeId}")

    """智能建议-数据统计"""
    def ElectricityStatistics(self, payload):
        return self.apiclient.post("/admin/ps/query/power", json=payload)

    """曲线图数据"""
    def ElectricPowerTrendChart(self, payload):
        return self.apiclient.post("/admin/ps/power/trend", json=payload)

    """收益"""
    def Income(self, payload):
        return self.apiclient.post("/admin/ps/power/income", json=payload)

    """分析报告"""
    def GetMonthReportTitle(self, payload):
        return self.apiclient.post("/admin/report/getMonthReportTitle", json=payload)

    """我的-电站配置"""
    def GetStationConfig(self, userId, HomeId):
        return self.apiclient.get(f"/admin/userConfig/getConfig?userId={userId}&homeId={HomeId}&codes=pv_power")

    """我的-问题反馈"""
    def ProblemFeedback(self, payload):
        return self.apiclient.post("/admin/cust/feedback", json=payload)

    """我的-问题反馈列表"""
    def ProblemFeedbackList(self, userId):
        return self.apiclient.post(f"/admin/cust/getFeedBack?userId={userId}&pageNumber=1&pageSize=10")

    """权限"""
    def DevicePurviewConfig(self, payload):
        return self.apiclient.put("/admin/userConfig/updateConfig", json=payload)

    def Logout(self, payload):
        return self.apiclient.post("/admin/user/logout", json=payload)









