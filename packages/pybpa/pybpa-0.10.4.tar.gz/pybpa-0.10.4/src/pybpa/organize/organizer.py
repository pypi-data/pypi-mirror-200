# -*- coding:utf-8 -*-
"""
# Name:         pybpa: organizer
# Author:       MilkyDesk
# Date:         2023/3/12 16:29
# Description:
#   
"""

# ------------------------- params --------------------------


# ------------------------- params --------------------------

import re

from ..dat.bpa_dat import DAT
from ..swi.bpa_swi import SWI


class DefaultOrganizer:
    """
    DefaultOrganizer定义了pybpa系统默认的文件组织和命名方式。与pfnt/swnt语义相同：
    1. 当运行pfnt时，会在dat目录下生成同方式名称的.pfo，.bse等文件
    2. 当运行swnt时，会在bse目录下生成同swi名称的.swx等文件。对于nrscp，则生成 f'{swi名}({.lsd定义的故障名称}).swx
    因此pybpa的organizer遵循这一设定，在此基础上，提供：
    1. 方式命名规则，从而提供文件的名称和路径：dat，pfo, bse
    2. 根据项目swi和lsd确定swx文件名, 从而提供文件的名称和路径：swi, swx, out, cur
    不同的organizer，最常见的区别是在文件名的组织上。可以继承这个基类，从而自定义上述两项命名规则。
    项目结构如下：
    project_path
    --base_dat.dat, base_swi.swi, base_lsd.lsd, (project_name.pybpa)
    --op_name1
    ----op_name1.dat
    ----base_swi(fault_name).swi
    ----op_name1.lsd

    """
    def __init__(self, root_path, project_name=None, swi_prefix='0'):
        """
        project_path：项目所在的上级目录，项目位于root_path/project_name
        project_name：当没有输入project_name时，默认root_path的最后一级已经包含项目名称，会将root_path解析为self.project_path/self.project_name
        swi_prefix: 临时swi名称前缀，也就是最终仿真的swx文件的前缀。如果没有这个，nrscp默认的名称是base_swi的名称，可能很长。
        """
        root_path = self.standard_path(root_path)  # 保证root_path以'/'结尾
        if project_name is None:
            self.project_name = root_path.split('/')[-1]
            print(f'项目名称没有定义，默认为根目录名称：{self.project_name}')
            self.project_path = root_path
        else:
            self.project_name = project_name
            self.project_path = self.standard_path(root_path + project_name)
        self.swi_prefix = swi_prefix
        self.describe()

    def describe(self):
        pass

    def knowledge(self):
        """输出organizer定义的文件结构的知识"""
        print(
            """
            DefaultOrganizer定义了pybpa系统默认的文件组织和命名方式。与pfnt/swnt语义相同：
            1. 当运行pfnt时，会在dat目录下生成同方式名称的.pfo，.bse等文件
            2. 当运行swnt时，会在bse目录下生成同swi名称的.swx等文件。对于nrscp，则生成 f'{swi名}({.lsd定义的故障名称}).swx
            因此pybpa的organizer遵循这一设定，在此基础上，提供：
            1. 方式命名规则，从而提供文件的名称和路径：dat，pfo, bse
            2. 根据项目swi和lsd确定swx文件名, 从而提供文件的名称和路径：swi, swx, out, cur
            不同的organizer，最常见的区别是在文件名的组织上。可以继承这个基类，从而自定义上述两项命名规则。
            项目结构如下：
            project_path
            --base_dat.dat, base_swi.swi, base_lsd.lsd, (project_name.pybpa)
            --op_name1
            ----op_name1.dat
            ----base_swi(fault_name).swi
            ----op_name1.lsd
        
            """)


    @staticmethod
    def standard_path(path):
        """
        定义“路径”：以'/'结尾。
        """
        return path + ('/' if path[-1] == '/' else '')

    def _get_base_path(self, suffix):
        """核心知识，规定了如何获取项目基础文件"""
        return self.project_path + self.project_name + '.' + suffix

    def get_path(self, ftype: str, op_name=None):
        """
        核心知识，返回指定方式的ftype文件路径，当没有指定方式时，返回参考文件路径。
        """
        if op_name:
            return f'{self.project_path}{op_name}/{op_name}.{ftype}'
        else:
            return f'{self.project_path}base_{ftype}.{ftype}'

    @staticmethod
    def parse_op_name(s):
        """
        核心知识，规定了 方式名称的检查方法
        方式名称:=K_info_[K]
        其中K是N-k，[K]是k条断开的线路
        info是方式的其他信息，可能是str也可能可以是int
        :return 如果符合格式，返回一个字典，否则False
        """
        try:
            v = s.split('_')
            v[0] = int(v[0])
            assert len(v) == v[0] + 2, f"在k={v[0]}时，_划分的字段数应为{v[0]+2}, 实际为{len(v)}"  # todo 改为logging
            v = [int(i) for i in s.split('_')]
            return {'pre_cut_line_num': v[0], 'info': v[1], 'pre_cut_line_list': v[2:]}
        except:
            return False

    @staticmethod
    def parse_info(info):
        """钩子方法，重写这个方法可以自定义info"""
        info = str(info)
        load_level = int(info)
        return {'load_level': load_level}

    # 核心知识，规定了如何获取方式名称: N_info_[N]
    @staticmethod
    def get_op_name(info, pre_cut_line_list):
        pre_cut_line_list = [i for i in pre_cut_line_list if i != '-1']
        return '_'.join([str(len(pre_cut_line_list)), str(info)] + pre_cut_line_list)

    def parse_path(self, path: str):
        """
        解析任意路径，按照这个organizer的知识
        """
        if self.project_path == path[:len(self.project_path)]:
            paths = path[len(self.project_path):].split('/')
            self.parse_op_name(path)
            print('是本项目的路径，但不是什么什么')
        else:
            print('不是本项目的路径！')


    def parse_op_name(self, op_name: str):
        v = [int(i) for i in op_name.split('_')]
        return {'pre_cut_line_num': v[0], 'info': v[1], 'pre_cut_line_list': v[2:]}

    # 核心知识，规定了如何获取方式文件路径
    def _get_op_file_path(self, op_name, suffix):
        return self.project_path + op_name + '/' + op_name + '.' + suffix

    # 核心知识，规定了如何获取swx文件名(NRSCP命名格式)
    def gen_swx_name(self, swi_name, post_cut_line_index, fault_bus):
        return swi_name + '(' + str(post_cut_line_index) + '-' + str(fault_bus) + ')'

    def parse_swx_name(self, swx_name):
        swx_info = re.sub('[.SWX()-]', ' ', swx_name.upper()).split()
        return {'swi_name': swx_info[0], 'post_cut_line_index': swx_info[1], 'fault_bus': swx_info[2]}

    # 核心知识，规定获取项目文件名
    def get_project_file_path(self):
        if not self.project_name:
            raise ValueError('没有定义项目文件名！')
        return self.project_path + self.project_name + '.pybpa'

    def get_lsd_path(self, op_name):
        return self._get_op_file_path(op_name, 'lsd')

    def get_dat_path(self, op_name):
        return self._get_op_file_path(op_name, 'dat')

    def get_pfo_path(self, op_name):
        return self._get_op_file_path(op_name, 'pfo')

    # get_bse
    def get_bse_path(self, op_name):
        return self.project_path + op_name + '/L3.bse'

    def get_swx_path(self, op_name, fault_name):
        return self.project_path + op_name + '/' + self.get_sw_name(fault_name) + '.swx'

    # 核心，规定了sw?文件名
    def get_sw_name(self, fault_name):
        return self.swi_prefix + '(' + fault_name + ')'

    # 仿真swi
    def get_temp_swi_path(self, op_name, fault_name):
        return self.project_path + op_name + '/' + self.swi_prefix + '(' + fault_name + ').swi'

    # 仿真swi
    def get_temp_swi_path(self, op_name, fault_name):
        return self.project_path + op_name + '/' + self.get_sw_name(fault_name) + '.swi'