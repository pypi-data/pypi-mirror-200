# -*- coding:utf-8 -*-

# ===========================================================
# Name:         transient_stability: gen_dat
# Author:       MilkyDesk
# Date:         2021/3/11 10:21
# Description:
#   根据已有的bpa仿真目录和内容，生成纯净的方式文件夹，每个文件夹包含dat文件和swi
#   从目标文件夹中，完成【任务】到target_path
# ===========================================================
import os
import re
import shutil
from multiprocessing import Pool

from tqdm import tqdm


# ------------------------- fields --------------------------


# path_dats = 'C:/Users/MilkyDesk/Downloads/' + 'dats/'
case_system = 39

path_root = 'E:/Data/transient_stability/' + str(case_system) + 'rd_gen/'
target_path = r'E:\Data\transient_stability/' + str(case_system) + 'rd_gen/rd_gen2/'
"""唯一一个与节点数量有关的路径"""
processes = 6
# path_dats = path_root + 'dats/'
path_dats = 'E:/dats/'
"""方式文件夹的存放路径"""

path_bpa = path_root + 'bpa/39数据/N-2/'

# 目录及筛选条件
task_dir_list = os.listdir(path_bpa)
task_dir_list = [x for x in task_dir_list if '.' not in x]
# task_dir_list = [x for x in task_dir_list if '.' not in x and '0' in x.split('_')[1]]

# ------------------------- fields --------------------------
"""
遍历文件夹
"""

def task(operation_name):

    # 计数器
    n_operation = 1
    n_case = 0
    # 遍历方式文件夹
    operation_path = path_bpa + operation_name
    # if operation_name[0] == '0':  # 处理思婷的命名法 '0_100_0_id'
    #     op = operation_name.split('_')
    #     target_path2 = target_path + '_'.join([op[0], op[1], op[-1]])   # '0_100_id'
    # else:
    #     target_path2 = target_path + operation_name
    target_path2 = target_path + operation_name

    for file in os.listdir(operation_path):
        f = file.lower()
        if '.dat' in f:  # x((x)-(x)).swi
            if not os.path.exists(target_path2):
                os.makedirs(target_path2)

            shutil.copy(operation_path + '/' + f, target_path2 + '/' + f)

            file_too_small = ''
            n_case += 1

    task_output = [n_operation, n_case]

    return task_output

class TaskReporter:
    """以task的输出为输入,屏幕输出任务完成情况"""
    def __init__(self):
        self.value = [0, 0]

    def record(self, task_output):
        self.value[0] += task_output[0]
        self.value[1] += task_output[1]

    def report(self):
        print('folder: ', self.value[0], '\tcase: ', self.value[1])


def prepare_data():
    tr = TaskReporter()
    # 多进程
    with Pool(processes=processes) as p:
        with tqdm(total=len(task_dir_list)) as pbar:
            for i, task_output in enumerate(p.imap_unordered(task, task_dir_list)):
                pbar.update()
                tr.record(task_output)
    tr.report()


def commented(s):
    """[疑似已丢弃]将一行注释掉"""
    print('WARNING: _Card方法已带有commented，此方法不再使用。需要检查哪里使用这个代码')
    return '.' + s


def uncommented(s):
    """将一行反注释"""
    print('WARNING: _Card方法已带有commented，此方法不再使用。需要检查哪里使用这个代码')
    if s:
        i = 0
        while i < len(s) and s[i] == '.':
            i += 1
        return s[i:]
    return s


if __name__ == '__main__':
    # if not os.source_path.exists(path_dats):
    #     os.makedirs(path_dats)
    prepare_data()
