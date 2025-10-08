"""
    @Time : 2025/4/27 10:15

    @Author : liuzhongkai

    @File : recalculate_no_upgrid
    
"""
import json, copy
import matplotlib.pyplot as plt


def recalculate_no_upgrid(data):
    batteryCapacity = data.get('batteryCapacity', 15000)
    maxBessOutput = data.get('maxBessOutput', batteryCapacity * 0.7)
    efOut = 0.95
    soc_limit_index = 0.7

    pvPrediction = data["pvPrediction"]
    pvReality = [copy.deepcopy(item) for item in data["pvReality"]]
    planPvReality = [copy.deepcopy(item) for item in pvReality]
    movePlanPvReality = [copy.deepcopy(item) for item in pvReality]

    loadReality = data["loadReality"]
    bessReality = data["bessReality"]
    gridReality = data["gridReality"]
    socReality = data["socReality"]

    moveLoadReality = data["moveLoadReality"]
    moveBessReality = data["moveBessReality"]
    moveGridReality = data["moveGridReality"]
    moveSocReality = data["moveSocReality"]

    # 处理预测分辨率 15min->5min
    pvPrediction_temp = [copy.deepcopy(item) for item in data["pvReality"]]
    for i in range(len(pvPrediction_temp)):
        pvPrediction_temp[i]['realityLoad'] = pvPrediction[int(i / 3)]['forecastPower']
    pvPrediction = [copy.deepcopy(item) for item in pvPrediction_temp]

    # 找到建议前光伏限发开始时间
    limit_pv_time_index = -1
    max_soc_index_before = -1
    max_soc_before = max(socReality, key=lambda x: x['realityLoad'])
    max_soc_value_before = max_soc_before['realityLoad']
    for index, item in enumerate(socReality):
        if item['realityLoad'] >= max_soc_value_before * 0.9:
            max_soc_index_before = index
            break

    if max_soc_value_before >= soc_limit_index:
        limit_pv_time_index = max_soc_index_before

    if limit_pv_time_index != -1:
        # 限发后处理,建议前
        # print("建议前光伏限发开始数据点序号：", limit_pv_time_index)
        # print("建议前光伏实际功率:")
        for i in range(limit_pv_time_index, len(pvPrediction) - 1):
            temp_pv = pvPrediction[i]['realityLoad']  # 读取值
            planPvReality[i]['realityLoad'] = temp_pv
            # print(planPvReality[i]['realityLoad'])

            # 光伏比负荷大
            if planPvReality[i]['realityLoad'] >= loadReality[i]['realityLoad']:
                # 没充满继续充
                if socReality[i]['realityLoad'] < 1.0:
                    bessReality[i]['realityLoad'] = -1 * (
                            planPvReality[i]['realityLoad'] - loadReality[i]['realityLoad'])
                # 充满了限发
                else:
                    socReality[i]['realityLoad'] = 1.0
                    planPvReality[i]['realityLoad'] = loadReality[i]['realityLoad']
                    bessReality[i]['realityLoad'] = 0
                gridReality[i]['realityLoad'] = 0
            # 光伏比负荷小
            else:
                # 能放电就放
                if socReality[i]['realityLoad'] > 0:
                    if loadReality[i]['realityLoad'] - planPvReality[i]['realityLoad'] > maxBessOutput:
                        bessReality[i]['realityLoad'] = maxBessOutput
                    else:
                        bessReality[i]['realityLoad'] = (
                                loadReality[i]['realityLoad'] - planPvReality[i]['realityLoad'])
                    gridReality[i]['realityLoad'] = loadReality[i]['realityLoad'] - planPvReality[i]['realityLoad'] - \
                                                    bessReality[i]['realityLoad']
                # 没电了
                else:
                    socReality[i]['realityLoad'] = 0
                    bessReality[i]['realityLoad'] = 0
                    gridReality[i]['realityLoad'] = loadReality[i]['realityLoad'] - planPvReality[i]['realityLoad'] - \
                                                    bessReality[i]['realityLoad']

            socReality[i + 1]['realityLoad'] = socReality[i]['realityLoad'] - bessReality[i]['realityLoad'] / efOut / (
                batteryCapacity) / 12

    # 找到建议后光伏限发开始时间
    limit_pv_time_index_after = -1
    max_soc_index_after = -1
    max_soc_after = max(moveSocReality, key=lambda x: x['realityLoad'])
    max_soc_value_after = max_soc_after['realityLoad']
    for index, item in enumerate(moveSocReality):
        if item['realityLoad'] >= max_soc_value_after * 0.9:
            max_soc_index_after = index
            break

    if max_soc_value_after >= soc_limit_index:
        limit_pv_time_index_after = max_soc_index_after

    if limit_pv_time_index != -1 and limit_pv_time_index_after == -1:
        limit_pv_time_index_after = limit_pv_time_index

    if limit_pv_time_index_after != -1:
        # 建议后
        # print("建议后光伏限发开始数据点序号：", limit_pv_time_index_after)
        # print("建议后光伏实际功率:")
        for i in range(limit_pv_time_index_after, len(pvPrediction) - 1):
            temp_pv = pvPrediction[i]['realityLoad']  # 读取值
            movePlanPvReality[i]['realityLoad'] = temp_pv
            # print(movePlanPvReality[i]['realityLoad'])

            if movePlanPvReality[i]['realityLoad'] >= moveLoadReality[i]['realityLoad']:
                if moveSocReality[i]['realityLoad'] < 1.0:
                    moveBessReality[i]['realityLoad'] = -1 * (
                            movePlanPvReality[i]['realityLoad'] - moveLoadReality[i]['realityLoad'])
                else:
                    moveSocReality[i]['realityLoad'] = 1.0
                    movePlanPvReality[i]['realityLoad'] = moveLoadReality[i]['realityLoad']
                    moveBessReality[i]['realityLoad'] = 0
                moveGridReality[i]['realityLoad'] = 0
            else:
                # 能放电就放
                if moveSocReality[i]['realityLoad'] > 0:
                    if moveLoadReality[i]['realityLoad'] - movePlanPvReality[i]['realityLoad'] > maxBessOutput:
                        moveBessReality[i]['realityLoad'] = maxBessOutput
                    else:
                        moveBessReality[i]['realityLoad'] = (
                                moveLoadReality[i]['realityLoad'] - movePlanPvReality[i]['realityLoad'])
                    moveGridReality[i]['realityLoad'] = moveLoadReality[i]['realityLoad'] - movePlanPvReality[i][
                        'realityLoad'] - moveBessReality[i]['realityLoad']
                else:
                    moveSocReality[i]['realityLoad'] = 0
                    moveBessReality[i]['realityLoad'] = 0
                    moveGridReality[i]['realityLoad'] = moveLoadReality[i]['realityLoad'] - movePlanPvReality[i][
                        'realityLoad'] - \
                                                        moveBessReality[i]['realityLoad']

            moveSocReality[i + 1]['realityLoad'] = moveSocReality[i]['realityLoad'] - moveBessReality[i][
                'realityLoad'] / efOut / (batteryCapacity) / 12

    # # 画图
    # pv_data = [item.get('realityLoad', 0.0) for item in planPvReality]
    # load_data = [item.get('realityLoad', 0.0) for item in loadReality]
    # bess_data = [item.get('realityLoad', 0.0) for item in bessReality]
    # grid_data = [item.get('realityLoad', 0.0) for item in gridReality]
    # soc_data = [item.get('realityLoad', 0.0) for item in socReality]
    #
    # move_pv_data = [item.get('realityLoad', 0.0) for item in movePlanPvReality]
    # move_load_data = [item.get('realityLoad', 0.0) for item in moveLoadReality]
    # move_bess_data = [item.get('realityLoad', 0.0) for item in moveBessReality]
    # move_grid_data = [item.get('realityLoad', 0.0) for item in moveGridReality]
    # move_soc_data = [item.get('realityLoad', 0.0) for item in moveSocReality]
    #
    # # 计划图
    # fig, ax1 = plt.subplots()
    # plt.title('计划')
    # line1, = ax1.plot(load_data, label='总负荷', color='red', linestyle='-.', marker='o')
    # line2, = ax1.plot(pv_data, label='光伏', color='orange', linestyle='--', marker='*')
    # line3, = ax1.plot(grid_data, label='电网', color='blue', linestyle=':', marker='^')
    # line4, = ax1.plot(bess_data, label='储能', color='green', linestyle='-', marker='x')
    #
    # ax2 = ax1.twinx()  # 关键步骤：创建双纵坐标轴
    # line5, = ax2.plot(soc_data, color='black', label='soc', marker='s')
    #
    # ax1.set_xlabel('时间')
    # ax1.set_ylabel('功率 (kW)')
    # ax2.set_ylabel('SOC (%)')
    #
    # ax1.grid(True, which='both', axis='both', linestyle='--', linewidth=0.5)
    #
    # lines = [line1, line2, line3, line4, line5]
    # labels = [line.get_label() for line in lines]  # 现在应该可以正确获取标签
    # ax1.legend(lines, labels, loc='upper right', ncol=1)  # ncol 控制图例的列数
    #
    # plt.rcParams['font.sans-serif'] = ['SimHei']  # Windows系统常用中文字体
    # plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #
    # # plt.show()
    #
    # # 建议后图
    # fig, ax1 = plt.subplots()
    # plt.title('建议')
    # line1, = ax1.plot(move_load_data, label='总负荷', color='red', linestyle='-.', marker='o')
    # line2, = ax1.plot(move_pv_data, label='光伏', color='orange', linestyle='--', marker='*')
    # line3, = ax1.plot(move_grid_data, label='电网', color='blue', linestyle=':', marker='^')
    # line4, = ax1.plot(move_bess_data, label='储能', color='green', linestyle='-', marker='x')
    #
    # ax2 = ax1.twinx()  # 关键步骤：创建双纵坐标轴
    # line5, = ax2.plot(move_soc_data, color='black', label='soc', marker='s')
    #
    # ax1.set_xlabel('时间')
    # ax1.set_ylabel('功率 (kW)')
    # ax2.set_ylabel('SOC (%)')
    #
    # ax1.grid(True, which='both', axis='both', linestyle='--', linewidth=0.5)
    #
    # lines = [line1, line2, line3, line4, line5]
    # labels = [line.get_label() for line in lines]  # 现在应该可以正确获取标签
    # ax1.legend(lines, labels, loc='upper right', ncol=1)  # ncol 控制图例的列数
    #
    # plt.rcParams['font.sans-serif'] = ['SimHei']  # Windows系统常用中文字体
    # plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #
    # plt.show()
    #
    # # 建议前后soc对比
    # plt.figure()
    # plt.plot(soc_data, label='计划总soc', color='red', linestyle='-.', marker='o')
    # plt.plot(move_soc_data, label='建议soc', color='green', linestyle='-.', marker='o')
    # plt.legend()
    # plt.grid(True)
    # # plt.show()

    # 修改验证后的值
    data["planPvReality"] = planPvReality
    data["loadReality"] = loadReality
    data["bessReality"] = bessReality
    data["gridReality"] = gridReality
    data["socReality"] = socReality

    data["movePlanPvReality"] = movePlanPvReality
    data["moveLoadReality"] = moveLoadReality
    data["moveBessReality"] = moveBessReality
    data["moveGridReality"] = moveGridReality
    data["moveSocReality"] = moveSocReality

    return data
