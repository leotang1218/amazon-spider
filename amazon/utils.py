# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : utils.py
# Time       ：2024/6/6 16:11
# Author     ：feo
# Description：
"""
import time


def now_ts():
    # 获取当前时间戳
    current_timestamp = time.time()
    return int(current_timestamp)


def first_or_def(l: list, default):
    if len(l) > 0:
        return l[0]
    if default is None:
        return ""
    return default


if __name__ == '__main__':
    print(now_ts())
