# -*- coding:utf-8 -*-

# ===========================================================
# Name:         transient_stability: gen_dat
# Author:       MilkyDesk
# Date:         2021/3/11 10:21
# Description:
#   根据已有的bpa仿真目录和内容，生成纯净的方式文件夹，每个文件夹包含dat文件和swi
# ===========================================================
import os
import re
import shutil
from multiprocessing import Pool

from tqdm import tqdm


# ------------------------- fields --------------------------


# path_dats = 'C:/Users/MilkyDesk/Downloads/' + 'dats/'
case_system = 39

path_root = 'E:/Data/transient_stability/' + str(case_system) + '/'
target_path = r'E:\Data\transient_stability/' + str(case_system) + '/bpa_备用/'
"""唯一一个与节点数量有关的路径"""

# path_dats = path_root + 'dats/'
path_dats = 'E:/dats/'
"""方式文件夹的存放路径"""

path_bpa = path_root + 'bpa/'
# ------------------------- fields --------------------------
"""
1. 遍历生成dat和文件夹
2. 提供一个接口，可以根据运行方式信息使用
"""




def build_case_multiprocess(operation_name):
    n_case = 0
    n_operation = 0

    # 计数器
    n_operation = 1
    # 遍历方式文件夹
    operation_path = path_bpa + operation_name
    target_path2 = target_path + operation_name

    for file in os.listdir(operation_path):
        f = file.lower()
        if ('.temp_dat' in f or '.lsd' in f or '.swi' in f) and ('ongo' not in f) and ('post' not in f):  # x((x)-(x)).swi

            if not os.path.exists(target_path2):
                os.makedirs(target_path2)

            shutil.copy(operation_path + '/' + f, target_path2 + '/' + f)

            file_too_small = ''
            n_case += 1

    return [n_operation, n_case]


def prepare_data():
    listdir = os.listdir(path_bpa)
    listdir = [x for x in listdir if '.' not in x]
    count = [0, 0]

    # 多进程2
    with Pool(processes=6) as p:
        with tqdm(total=len(listdir)) as pbar:
            for i, result in enumerate(p.imap_unordered(build_case_multiprocess, listdir)):
                pbar.update()
                count[0] += result[0]
                count[1] += result[1]

    print('operation: ', count[0], '\tcase: ', count[1])


def commented(s):
    """将一行注释掉"""
    return '.' + s


def uncommented(s):
    """将一行反注释"""
    if s:
        i = 0
        while i < len(s) and s[i] == '.':
            i += 1
        return s[i:]
    return s


if __name__ == '__main__':
    # if not os.path.exists(path_dats):
    #     os.makedirs(path_dats)
    prepare_data()
