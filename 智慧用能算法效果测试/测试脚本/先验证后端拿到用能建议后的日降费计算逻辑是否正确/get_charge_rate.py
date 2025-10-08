# -*- coding: utf-8 -*-
"""
储能型号充电倍率区间
"""


def rate_range(battery_model):
    if battery_model == "SBH":
        data = [
            (-float('inf'), 0, 0),
            (0, 5, 0.1),
            (5, 10, 0.2),
            (10, 15, 0.3),
            (15, 20, 0.5),
            (20, 25, 0.8),
            (25, 45, 1),
            (45, 50, 0.8),
            (50, 55, 0.5),
            (55, float('inf'), 0)
        ]
    else:
        data = [
            (-float('inf'), 0, 0),
            (0, 5, 0.1),
            (5, 10, 0.3),
            (10, 25, 0.6),
            (25, 48, 0.6),
            (48, 50, 0.4),
            (50, 55, 0.3),
            (55, float('inf'), 0)
        ]
    return data


def get_rate(T, data):
    for low, high, value in data:
        if T is not None:
            if low <= T < high:
                return value
        else:
            return 0


