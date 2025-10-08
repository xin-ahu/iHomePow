# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2025/3/5 17:52
# @Author: wangxin16
# @Email: wangxin16@sungrowpower.com
import os
import random
import pandas as pd
import matplotlib.pyplot as plt
from decimal import Decimal
from HttpClient import HttpClient
from datetime import datetime, timedelta
from log import get_logger
from recalculate_no_upgrid import recalculate_no_upgrid

log = get_logger()

api_web = HttpClient()
api_app = HttpClient()

callTime = "2025-04-01 08:00:00"
payload = {"callTime": callTime, "pageNum": 1, "pageSize": 10, "psId": "1966080"}   # 生产北京实证：1966080  # 测试新能源T：1761299
homeId = "1906529306692161536"  # 测试北京实证：1906529306692161536  # 测试新能源T：1859885290689269
# 开始和结束日期
start_date = datetime.strptime("2025-04-01", "%Y-%m-%d")
end_date = datetime.strptime("2025-04-30", "%Y-%m-%d")

Reduce_costs = []

# 循环遍历每一天
current_date = start_date
while current_date <= end_date:
    call_date = str(current_date).split(" ")[0]
    payload_app = {
        "date": call_date,
        "dateType": 1,
        "homeId": homeId
    }

    hour = random.randint(7, 11)
    minute = random.randint(0, 59)

    payload["callTime"] = f"{current_date.strftime('%Y-%m-%d')} 08:00:00"
    dataTime = payload["callTime"]
    psId = payload["psId"]

    res = api_web.post("/simulate/genSuggestion", json=payload)
    res_app = api_app.post_app("/admin/ps/query/power", json=payload_app)
    res.raise_for_status()
    res_app.raise_for_status()
    data = res.json()["data"]

    # 调用无馈网情况下功率计算
    if data['connectType'] == 3:
        data = recalculate_no_upgrid(data)

    data_app = res_app.json()["data"]
    if data_app["totalGenerate"]:
        totalGenerate = data_app["totalGenerate"]
        feedPower = data_app["feedPower"]
        totalGenerateRate = ((Decimal(totalGenerate) - Decimal(feedPower)) / Decimal(totalGenerate)) * 100
        formatted_rate = f"{totalGenerateRate:.2f}%"
    else:
        totalGenerate = 0
        feedPower = 0
        totalGenerateRate = 0
        formatted_rate = "0.00%"
    # totalGenerateRate = ((Decimal(data_app["totalGenerate"]) - Decimal(data_app["feedPower"])) / Decimal(data_app["totalGenerate"])) * 100
    # formatted_rate = f"{totalGenerateRate:.2f}%"
    if data is not None:
        costReality = data.get("costReality")
        moveCostReality = data.get("moveCostReality")
        costReduce = data.get("costReduce")
        suggestion = data.get("detail")
        if costReduce > 0:
            costReduceRate = abs(costReduce / costReality * 100 if costReality != 0 else 0)
        elif costReduce < 0 and suggestion != []:
            costReduceRate = -abs(costReduce / costReality * 100 if costReality != 0 else 0)
            log.error(f"callTime: {dataTime}    psId:{psId}    日降本为负值:{costReduce}")
        else:
            costReduceRate = 0
        formatted_costReduceRate = f"{costReduceRate:.2f}%"
        Reduce_costs.append(
            {
                "psId": payload["psId"],
                "homeId": homeId,
                "测试日期": dataTime,
                "建议前成本": costReality,
                "建议后成本": moveCostReality,
                "降本": costReduce,
                "原始自发自用率": formatted_rate,
                "降本率": formatted_costReduceRate
            }
        )

    current_date += timedelta(days=1)

# 过滤掉 costReduce 为负值的字典项
# Reduce_costs = [item for item in Reduce_costs if item["降本"] > 0]

# 对数据进行排序，确保数据点按沿 x 轴自左向右自发自用率越来越大的顺序展示
Reduce_costs.sort(key=lambda x: float(x["原始自发自用率"].strip('%')))

# 提取数据用于绘图
test_dates = [item["测试日期"] for item in Reduce_costs]
formatted_rates = [float(item["原始自发自用率"].strip('%')) for item in Reduce_costs]
formatted_costReduceRates = [float(item["降本率"].strip('%')) for item in Reduce_costs]

# 绘制曲线
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
fig, ax1 = plt.subplots(figsize=(12, 6))

# 左y轴：降本率（柱形图）
ax1.set_xlabel(f'测试站点ID：{payload["psId"]}    测试日期：{str(start_date).split(" ")[0]}---{str(end_date).split(" ")[0]}', fontsize=12, fontweight='bold')
ax1.set_ylabel('降本率 (%)')
ax1.bar(test_dates, formatted_costReduceRates, color='tab:orange', alpha=0.6)
ax1.tick_params(axis='y')

# 右y轴：自发自用率（折线图）
ax2 = ax1.twinx()
ax2.set_ylabel('原始自发自用率 (%)')
ax2.plot(test_dates, formatted_rates, color='tab:green', marker='o', linestyle='-', linewidth=2)
ax2.tick_params(axis='y')

# 添加标题
fig.suptitle('降本率和原始自发自用率的负相关性', fontsize=16, fontweight='bold', y=0.95)

# 隐藏x轴的具体测试日期
plt.xticks([])

# 添加y轴提示
text1 = '柱形图：降本率'
text2 = '折线图：原始自发自用率'

# 计算文本的总长度
total_length = len(text1) + len(text2) + 10  # 10个字符的间隔

# 计算每个文本的起始位置
x1 = (0.5 - (total_length / 200.0))  # 假设每个字符宽度约为1/3000
x2 = (0.5 + (total_length / 200.0)) - (len(text2) / 3000)

fig.text(x1, 0.02, text1, color='tab:orange', fontsize=11, fontweight='bold', ha='left')
fig.text(x2, 0.02, text2, color='tab:green', fontsize=11, fontweight='bold', ha='right')

# 设置x轴标签旋转
plt.xticks(rotation=45)
plt.tight_layout(rect=[0, 0.05, 1, 0.95])  # 调整rect以适应提示信息

# 检查并创建目录
output_dir = f'./test_data/real/{payload["psId"]}'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 保存图表
plt.savefig(f'{output_dir}/{payload["psId"]}_result.png')
plt.close()

# 生成Excel文件
df = pd.DataFrame(Reduce_costs)
df.to_excel(f'{output_dir}/{payload["psId"]}_result.xlsx', index=False)





