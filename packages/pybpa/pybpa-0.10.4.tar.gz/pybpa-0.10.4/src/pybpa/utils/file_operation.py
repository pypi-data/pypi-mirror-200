# -*- coding:utf-8 -*-
"""
# Name:         uncertain: file_operation
# Author:       MilkyDesk
# Date:         2022/9/13 10:53
# Description:
#   提供一些：
        创建新工作目录的方法
        带过滤器的文件深度复制方法
"""

# ------------------------- params --------------------------
import fnmatch

base_allow_patterns = ['.linked_dat', '.swi', '.lsd']
result_allow_patterns = ['.linked_dat', '.swi', '.lsd', '.swx', '.pfo']

# ------------------------- params --------------------------
import os
import shutil

def _allow_patterns(patterns):
    """
    仿照shutil.ignore_patterns写的
    输入的是允许的后缀。
    """
    def _ignore_patterns(path, names):
        ignored_names = [name for name in names if '.' in name and name[-4:].lower() not in patterns]
        return list(ignored_names)
    return _ignore_patterns

def new_working_dir(source_path, target_path=None, allow_patterns=base_allow_patterns) -> bool:
    """
    以source为初始内容，在target创建目录
    :param source_path:
    :param target_path:
    :return:
    """
    try:
        shutil.copytree(source_path, target_path, ignore=_allow_patterns(allow_patterns))
        return True
    except Exception as e:
        print(e)
    return False

if __name__ == '__main__':
    # r'E:\Data\transient_stability\39\bpa\0_100_0'
    # r'E:\Data\transient_stability\39\rd_1'
    new_working_dir(source_path=r'E:\Data\transient_stability\39\bpa',
                    target_path=r'E:\Data\transient_stability\39\rd_1')
    # new_working_dir(input('source_path='), input('target_path='), allow_patterns=base_allow_patterns)