# -*- coding:utf-8 -*-
"""
# Name:         transient_stability: nrtsc_lsd
# Author:       MilkyDesk
# Date:         2021/7/23 11:13
# Description:
#   
"""

# ------------------------- params --------------------------


# ------------------------- params --------------------------
import os

class LSD:
    """目前并不支持lsd元素的修改"""
    def __init__(self, full_lsd_path):
        f = open(full_lsd_path, 'r')
        self.lines = f.readlines()
        if self.lines[-1][-1] != '\n':
            self.lines[-1] += '\n'
        faults = []
        for i, l in enumerate(self.lines):
            if 'NR_FG' == l[:5]:
                faults.append([i, l[5:].strip()])  # Fault结构：NR_FG fault_line_order-fault_bus_order
        # print(f'num of faults: {len(faults)}, they are: {faults}')
        self.faults = faults
        self.fault_dict = {f[1]: self.lines[(f[0]+1):(f[0]+3)] for f in faults}

    def get_fault_lines(self, fault_id):
        if isinstance(fault_id, int):
            return self.lines[(self.faults[fault_id]+1):(self.faults[fault_id]+3)]  # i(NR_FG xxx，不要)。 i+1, i+2, 一共两行
        else:
            return self.fault_dict[fault_id]

    @staticmethod
    def get_fault_name(fault_line_order, fault_bus_order):
        return str(fault_line_order) + '-' + str(fault_bus_order)

    @staticmethod
    def parse_fault_name(fault_name):
        return fault_name.split('-')

    @staticmethod
    def build_from(path):
        """
        从文件夹或者文件中新建实例,如果是从文件夹，只会找文件夹中第一个出现的。
        :param path:
        :return:
        """
        if os.path.isfile(path):
            if '.lsd' in path.lower():
                return LSD(path)
        elif os.path.isdir(path):
            for f in os.listdir(path):
                if '.lsd' in f.lower():
                    return LSD(path + '/' + f)
        raise ValueError('cannot find .lsd file in path!')

    def save_to_file(self, path, ban_branch=[]):
        """todo 合并到save_to_file
        想写入哪里，直接写完整路径即可。会直接递归地创建路径。
        todo 未来与swi的方法合并
        :param path: 有没有以.lsd结尾都可以。
        :param ban_branch: 正文的开头，用来记录一些信息的。
        :return:
        """
        if path[-4:].lower() != '.lsd':
            path += '.lsd'
        os.makedirs(os.path.dirname(path), exist_ok=True)
        file = open(path, 'w')
        for fault in self.faults:
            if self.parse_fault_name(fault[1])[0] not in ban_branch:
                file.writelines(self.lines[fault[0]:fault[0]+3])
        file.close()
