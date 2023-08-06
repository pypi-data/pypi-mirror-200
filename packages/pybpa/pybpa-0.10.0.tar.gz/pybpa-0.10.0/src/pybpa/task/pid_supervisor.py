# -*- coding:utf-8 -*-
"""
# Name:         transient_stability: pid_supervisor
# Author:       MilkyDesk
# Date:         2021/7/14 10:35
# Description:
#   监控swnt进程，如果进程存在超过10分钟，则kill掉
"""
from os import kill
import time

import psutil
# ------------------------- params --------------------------
every_n_min = 10

# ------------------------- params --------------------------
pid_set = set()
while True:
    pids = [p for p in psutil.pids() if psutil.Process(p).name() == 'swnt-4.29.3rz.exe']
    killed_count = 0
    for pid in pids:
        if pid in pid_set and psutil.Process.name() == 'swnt-4.29.3rz.exe':
            kill(pid)
            pid_set.remove(pid)
            killed_count += 1
        else:
            pid_set.add(pid)
    print(time.time(), 'killed: ', killed_count)
    time.sleep(every_n_min * 60)
