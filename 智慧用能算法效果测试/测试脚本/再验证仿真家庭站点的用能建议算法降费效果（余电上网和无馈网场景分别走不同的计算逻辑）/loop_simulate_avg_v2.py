# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2025/4/23 20:30
# @Author: wangxin16
# @Email: wangxin16@sungrowpower.com
import os
import pandas as pd
import matplotlib.pyplot as plt
from recalculate_no_upgrid import recalculate_no_upgrid
from HttpClient import HttpClient
from datetime import datetime, timedelta
from log import get_logger

log = get_logger()

api_web = HttpClient()
api_app = HttpClient()


psId_l = [
1289550,
531800,
405609,
579390,
1289546,
779446,
747614,
712365,
475194,
1383298,
737548,
531771,
579399,
1286145,
1026261,
1334983,
1199502,
1341980,
1190145,
696670,
1287709,
1385589,
697027,
1016227,
1247254,
1286572
]
psId_l1 = ['1761299']  # 生产北京实证别墅psId：1966080  新能源T：1761299
# psId_li = ['1289550', '531800', '405609', '579390', '1289546', '779446', '747614', '712365', '475194', '1383298', '737548', '531771', '579399', '1286145', '1026261', '1334983', '1199502', '1341980', '1190145', '696670', '1287709', '1385589', '697027', '1016227', '1247254', '1286572', '1286143', '1326266', '703315', '579425', '405743', '579448', '1272909', '405710', '943569', '1323317', '405625', '1287702', '696652', '828906', '1316421', '1392710', '777892', '1374845', '1091836', '1392723', '968141', '988686', '1003591', '1003886', '716493', '1286137', '745410', '1289855', '779527', '1303592', '1330837', '778751', '1334919', '405497', '712134', '531465', '556611', '745391', '934579', '1283482', '724608', '1025074', '1395019', '695600', '1343176', '1178690', '739460', '1247260', '1246500', '716567', '766416', '1228879', '1343575', '1181057', '1392743', '747616', '694542', '1286144', '696910', '1274044', '1280225', '1175122', '1286141', '737554', '816062', '968613', '694598', '1286147', '1304345', '472767', '1343511', '767007', '1385462', '1286531']
# callTime = "2025-04-01 08:00:00"
# start_date = datetime.strptime("2025-04-01", "%Y-%m-%d")
# end_date = datetime.strptime("2025-04-18", "%Y-%m-%d")

callTime = "2025-04-17 08:00:00"
start_date = datetime.strptime("2025-04-17", "%Y-%m-%d")
end_date = datetime.strptime("2025-04-18", "%Y-%m-%d")

# 全天用电-空调季（26户16kw）
psId_ac_16kw = [1289550,531800,405609,579390,1289546,779446,747614,712365,475194,1383298,737548,531771,579399,1286145,1026261,1334983,1199502,1341980,1190145,696670,1287709,1385589,697027,1016227,1247254,1286572]
# 晚高峰用电-空调季（24户16kw）
psId_night_ac_16kw = [716493,1286137,745410,1289855,779527,1303592,1330837,778751,1334919,405497,712134,531465,745391,934579,1283482,724608,1025074,1395019,695600,1343176,1178690,739460,1247260,1246500]
# 全天用电-非空调季（12户10kw）
psId_noac_10kw = [1286143,1326266,703315,579425,405743,579448,1272909,405710,943569,1323317,405625,1287702]
# 全天用电-非空调季（12户22kw）
psId_noac_22kw = [696652,828906,1316421,1392710,777892,1374845,1091836,1392723,968141,988686,1003591,1003886]

# 晚高峰用电-非空调季（13户22kw）
psId_night_noac_22kw =[716567,766416,1228879,1343575,1181057,1392743,747616,694542,1286144,696910,1274044,1280225,1175122]

# 晚高峰用电-非空调季（13户10kw）
psId_night_noac_10kw =[556611,1286141,737554,816062,968613,694598,1286147,1304345,472767,1343511,767007,1385462,1286531]


avg_Reduce_costs = []   # 存储所有站点的日均数据

index = 0
# 循环遍历每个psId
for psId in psId_l1:
    index = index+1
    print("now psId is ",psId)
    print('now index is' , index ,'of',len(psId_l1) )
    payload = {"callTime": callTime, "pageNum": 1, "pageSize": 10, "psId": psId}
    Reduce_costs = []   # 存储每日数据
    # 循环遍历每一天
    current_date = start_date
    while current_date <= end_date:
        payload["callTime"] = f"{current_date.strftime('%Y-%m-%d')} 08:00:00"
        dataTime = payload["callTime"]
        print("now dateTime is ", dataTime)
        try:
            res = api_web.post("/simulate/genSuggestion", json=payload)
            res.raise_for_status()
            data = res.json()["data"]
            print(data['connectType'])
            # 调用无馈网情况下功率计算
            if data['connectType'] == 3:
                data = recalculate_no_upgrid(data)
                print("此电站运行在无馈网模式")

            costReality = data["costReality"]   # 建议前日用电成本
            moveCostReality = data["moveCostReality"]   # 建议后日用电成本
            dayGenerate = data["dayGenerate"]   # 日发电量
            dayGrid = data["dayGrid"]   # 原始日上网电量
            moveDayGrid = data["moveDayGrid"]   # 建议后日上网电量
            daySelfUse = dayGenerate - dayGrid  # 原始日自发自用电量
            moveDaySelfUse = dayGenerate - moveDayGrid  # 建议后日自发自用电量
            daySelfUseRate = data["daySelfUseRate"]  # 原始日自发自用率
            moveDaySelfUseRate = data["moveDaySelfUseRate"]     # 建议后日自发自用率
            DayMove_SelfUseRate_Delta = (moveDaySelfUseRate - daySelfUseRate) * 100     # 日自发自用提升率
            formatted_DayMove_SelfUseRate_Delta = f"{DayMove_SelfUseRate_Delta:.2f}%"   # 日自发自用提升率格式化
            suggestion = data["detail"]
            costReduce = data["costReduce"]
            if costReduce > 0:
                costReduceRate = abs(costReduce / costReality * 100 if costReality != 0 else 0)
            elif costReduce < 0 and suggestion != []:
                costReduceRate = -abs(costReduce / costReality * 100 if costReality != 0 else 0)
                log.critical(f"callTime: {dataTime}    psId:{psId}    日降本为负值:{costReduce}")
            else:
                costReduce = 0
                costReduceRate = 0
                log.error(f"callTime: {dataTime}    psId:{psId}    日降本为零:{costReduce}")
            formatted_costReduceRate = f"{costReduceRate:.2f}%"
            Reduce_costs.append(
                {
                    "psId": payload["psId"],
                    "测试日期": dataTime,
                    "建议前日用电成本": costReality,
                    "建议后日用电成本": moveCostReality,
                    "日降本": costReduce,
                    "日发电量": dayGenerate,
                    "原始日上网电量": dayGrid,
                    "建议后日上网电量": moveDayGrid,
                    "原始日自发自用电量": daySelfUse,
                    "原始日自发自用率": daySelfUseRate,
                    "建议后日自发自用电量": moveDaySelfUse,
                    "建议后日自发自用率": moveDaySelfUseRate,
                    "日自发自用提升率": formatted_DayMove_SelfUseRate_Delta,
                    "日降本率": formatted_costReduceRate
                }
            )
        except Exception as e:
            log.error(f"callTime: {dataTime}    psId:{psId}    接口异常")
            pass
            # print(f"错误：{e}")
        finally:
            current_date += timedelta(days=1)

    # 过滤掉 costReduce 为负值或零的字典项
    # Reduce_costs = [item for item in Reduce_costs if item["日降本"] > 0]

    # 生成单个站点所有日数据excel
    df_site = pd.DataFrame(Reduce_costs)
    df_site.to_excel(f'./test_data/{psId}_testdata.xlsx', index=False)

    # 计算单个站点日均数据
    if Reduce_costs:
        avg_costReality = sum(item["建议前日用电成本"] for item in Reduce_costs) / len(Reduce_costs)
        avg_moveCostReality = sum(item["建议后日用电成本"] for item in Reduce_costs) / len(Reduce_costs)
        avg_costReduce = avg_costReality - avg_moveCostReality
        avg_dayGenerate = sum(item["日发电量"] for item in Reduce_costs) / len(Reduce_costs)
        avg_dayGrid = sum(item["原始日上网电量"] for item in Reduce_costs) / len(Reduce_costs)
        avg_moveDayGrid = sum(item["建议后日上网电量"] for item in Reduce_costs) / len(Reduce_costs)
        avg_daySelfUse = sum(item["原始日自发自用电量"] for item in Reduce_costs) / len(Reduce_costs)
        avg_daySelfUseRate = (avg_daySelfUse / avg_dayGenerate) * 100 if avg_dayGenerate != 0 else 0
        avg_moveDaySelfUse = sum(item["建议后日自发自用电量"] for item in Reduce_costs) / len(Reduce_costs)
        avg_moveDaySelfUseRate = (avg_moveDaySelfUse / avg_dayGenerate) * 100 if avg_dayGenerate != 0 else 0
        avg_formatted_SelfUseRate_Delta = ((avg_moveDaySelfUse - avg_daySelfUse) / avg_dayGenerate) * 100 if (
                avg_dayGenerate != 0) else 0
        avg_formatted_costReduceRate = (avg_costReduce / abs(avg_costReality)) * 100 if avg_costReality != 0 else 0

        avg_Reduce_costs.append(
            {
                "psId": payload["psId"],
                "测试日期": f"{str(start_date).split(' ')[0]}---{str(end_date).split(' ')[0]}",
                "建议前日均用电成本": avg_costReality,
                "建议后日均用电成本": avg_moveCostReality,
                "日均降本": avg_costReduce,
                "日均发电量": avg_dayGenerate,
                "原始日均上网电量": avg_dayGrid,
                "建议后日均上网电量": avg_moveDayGrid,
                "原始日均自发自用电量": avg_daySelfUse,
                "原始日均自发自用率": f"{avg_daySelfUseRate:.2f}%",
                "建议后日均自发自用电量": avg_moveDaySelfUse,
                "建议后日均自发自用率": f"{avg_moveDaySelfUseRate:.2f}%",
                "日均自发自用提升率": f"{avg_formatted_SelfUseRate_Delta:.2f}%",
                "日均降本率": f"{avg_formatted_costReduceRate:.2f}%"
            }
        )

# 对所有数据进行排序，确保数据点按沿右y轴自发自用率升序展示
avg_Reduce_costs.sort(key=lambda x: float(x["原始日均自发自用率"].strip('%')))

# 计算测试样本数
testdata_count = str(len(avg_Reduce_costs))

# 提取数据用于绘图
test_dates = [item["测试日期"] for item in avg_Reduce_costs]
avg_daySelfUseRate = [float(item["原始日均自发自用率"].strip('%')) for item in avg_Reduce_costs]
avg_formatted_SelfUseRate_Delta = [float(item["日均自发自用提升率"].strip('%')) for item in avg_Reduce_costs]
avg_formatted_costReduceRate = [float(item["日均降本率"].strip('%')) for item in avg_Reduce_costs]

# 绘制曲线
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体

# 第一个图表：日均自发自用提升率
fig, ax1 = plt.subplots(figsize=(12, 6))

# 自适应柱形图宽度
num_samples = len(test_dates)
min_bar_width = 0.2  # 设置最小柱形图宽度
max_bar_width = 0.5  # 设置最大柱形图宽度
bar_width = max(min_bar_width, min(max_bar_width, 0.8 / num_samples))  # 动态调整柱形图宽度

# 左y轴：日均自发自用提升率（柱形图）
x = range(len(test_dates))
ax1.set_xlabel(f'测试样本数：{testdata_count}        测试日期：{str(start_date).split(" ")[0]}---{str(end_date).split(" ")[0]}', fontsize=12, fontweight='bold')
ax1.set_ylabel('日均自发自用提升率 (%)')
ax1.bar(x, avg_formatted_SelfUseRate_Delta, width=bar_width, color='tab:orange', alpha=0.6)
ax1.tick_params(axis='y')

# 右y轴：原始日自发自用率（折线图）
ax2 = ax1.twinx()
ax2.set_ylabel('原始日均自发自用率 (%)')
ax2.plot(x, avg_daySelfUseRate, color='tab:green', marker='o', linestyle='-', linewidth=2)
ax2.tick_params(axis='y')

# 添加标题
fig.suptitle('日均自发自用提升率和原始日均自发自用率的负相关性', fontsize=16, fontweight='bold', y=0.95)

# 隐藏x轴标签以避免重叠
plt.xticks([])

plt.tight_layout(rect=[0, 0.05, 1, 0.95])  # 调整rect以适应提示信息

# 添加y轴提示
text1 = '柱形图：日均自发自用提升率'
text2 = '折线图：原始日均自发自用率'

# 计算文本的总长度
total_length = len(text1) + len(text2) + 10  # 10个字符的间隔

# 计算每个文本的起始位置
x1 = (0.5 - (total_length / 200.0))  # 假设每个字符宽度约为1/3000
x2 = (0.5 + (total_length / 200.0)) - (len(text2) / 3000)

fig.text(x1, 0.02, text1, color='tab:orange', fontsize=11, fontweight='bold', ha='left')
fig.text(x2, 0.02, text2, color='tab:green', fontsize=11, fontweight='bold', ha='right')

# 检查并创建目录
output_dir = f'./test_data/simulate/avg'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 保存图表
plt.savefig(f'{output_dir}/avg_result_1.png')
plt.close()

# 第二个图表：日均降本率
fig, ax1 = plt.subplots(figsize=(12, 6))

# 左y轴：日均降本率（柱形图）
ax1.set_xlabel(f'测试样本数：{testdata_count}        测试日期：2024/07/01-2024/09/30', fontsize=12, fontweight='bold')
ax1.set_ylabel('日均降本率 (%)')
ax1.bar(x, avg_formatted_costReduceRate, width=bar_width, color='tab:blue', alpha=0.6)
ax1.tick_params(axis='y')

# 右y轴：原始日自发自用率（折线图）
ax2 = ax1.twinx()
ax2.set_ylabel('原始日均自发自用率 (%)')
ax2.plot(x, avg_daySelfUseRate, color='tab:green', marker='o', linestyle='-', linewidth=2)
ax2.tick_params(axis='y')

# 添加标题
fig.suptitle('日均降本率和原始日均自发自用率的负相关性', fontsize=16, fontweight='bold', y=0.95)

# 隐藏x轴标签以避免重叠
plt.xticks([])

plt.tight_layout(rect=[0, 0.05, 1, 0.95])  # 调整rect以适应提示信息

# 添加y轴提示
text1 = '柱形图：日均降本率'
text2 = '折线图：原始日均自发自用率'

# 计算文本的总长度
total_length = len(text1) + len(text2) + 10  # 10个字符的间隔

# 计算每个文本的起始位置
x1 = (0.5 - (total_length / 200.0))  # 假设每个字符宽度约为1/3000
x2 = (0.5 + (total_length / 200.0)) - (len(text2) / 3000)

fig.text(x1, 0.02, text1, color='tab:orange', fontsize=11, fontweight='bold', ha='left')
fig.text(x2, 0.02, text2, color='tab:green', fontsize=11, fontweight='bold', ha='right')

# 保存图表
plt.savefig(f'{output_dir}/avg_result_2.png')
plt.close()

# 生成所有站点日均数据Excel文件
df = pd.DataFrame(avg_Reduce_costs)
df.to_excel(f'{output_dir}/avg_result.xlsx', index=False)

# 定义变量用于储存最终生成的excel文件内的数据行数（不包含表头）
excel_row_count = len(df)

print(f"生成的Excel文件数据行数: {excel_row_count}")

