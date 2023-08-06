# -*- coding:utf-8 -*-
"""
# Name:         transient_stability: file_organize
# Author:       MilkyDesk
# Date:         2021/7/7 23:40
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
        swi_prefix: 临时swi名称前缀，也就是最终仿真的swx文件的前缀。如果没有这个，nrscp默认的名称是base_swi的名称，可能很长。
        """
        self.root_path = root_path + ('/' if root_path[-1] == '/' else '')  # 保证root_path以'/'结尾
        if project_name is None:
            self.project_name = root_path.split('/')[-1]
            print(f'项目名称没有定义，默认为根目录名称：{self.project_name}')
        else:
            self.project_name = project_name
        self.swi_prefix = swi_prefix
        raise Warning('在后续版本会废弃这个路径，转而使用pybpa.organize.organizer的同名类。')

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

    # 核心知识，规定了如何获取项目基础文件
    def _get_base_path(self, suffix):
        return self.root_path + self.project_name + '.' + suffix

    @staticmethod
    def _parse_path(path):
        raise NotImplementedError  # todo

    # 核心知识，规定了如何获取方式名称: N_info_[N]
    def get_op_name(self, info, pre_cut_line_list):
        pre_cut_line_list = [i for i in pre_cut_line_list if i != '-1']
        return '_'.join([str(len(pre_cut_line_list)), str(info)] + pre_cut_line_list)

    def parse_op_name(self, op_name: str):
        v = [int(i) for i in op_name.split('_')]
        return {'pre_cut_line_num': v[0], 'info': v[1], 'pre_cut_line_list': v[2:]}

    # 核心知识，规定了如何获取方式文件路径
    def _get_op_file_path(self, op_name, suffix):
        return self.root_path + op_name + '/' + op_name + '.' + suffix

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
        return self.root_path + self.project_name + '.pybpa'

    def get_lsd_path(self, op_name):
        return self._get_op_file_path(op_name, 'lsd')

    def get_dat_path(self, op_name):
        return self._get_op_file_path(op_name, 'dat')

    def get_pfo_path(self, op_name):
        return self._get_op_file_path(op_name, 'pfo')

    # 仿真swi
    def get_temp_swi_path(self, op_name, fault_name):
        return self.root_path + op_name + '/' + self.swi_prefix + '(' + fault_name + ').swi'

    # 仿真swi
    def get_temp_swi_path(self, op_name, fault_name):
        return self.root_path + op_name + '/' + self.get_sw_name(fault_name) + '.swi'

    # get_bse
    def get_bse_path(self, op_name):
        return self.root_path + op_name + '/L3.bse'

    def get_swx_path(self, op_name, fault_name):
        return self.root_path + op_name + '/' + self.get_sw_name(fault_name) + '.swx'

    # 核心，规定了sw?文件名
    def get_sw_name(self, fault_name):
        return self.swi_prefix + '(' + fault_name + ')'

    def base_dat_path(self):
        return self._get_base_path('dat')

    def base_swi_path(self):
        return self._get_base_path('swi')

    def base_lsd_path(self):
        return self._get_base_path('lsd')



class JyLkOrganizer:
    """
    jy的文件组织方式
    liukai的文件组织方式：
    _path全部以'/'结尾
    """
    def __init__(self, case_system, root_path, source_path, target_path, dat_in_root, swi_in_root):
        """

        @param case_system:
        @param root_path:
        @param source_path:
        @param target_path:
        @param dat_in_root:
        @param swi_in_root:
        """
        self.case_system = str(case_system)
        self.root_path = root_path + self.case_system + '/'
        self.source_path = source_path
        self.target_path = target_path
        self.dat_in_root = dat_in_root
        self.swi_in_root = swi_in_root
        self.dat = None
        self.swi = None

    def get_dat(self, operation_folder: str = None):
        if self.dat is None:
            if self.dat_in_root or not operation_folder:
                self.dat = DAT.build_from(self.source_path)
            else:
                self.dat = DAT.build_from(self.source_path + operation_folder + '/')
        return self.dat

    def get_swi(self, coodinate: str = 'BS', operation_folder: str = None):
        if self.swi is None:
            if self.swi_in_root or not operation_folder:
                self.swi = SWI.build_from(self.source_path)
            else:
                self.swi = SWI.build_from(self.source_path + operation_folder + '/')
            self.dat = self.swi.linked_dat
            self.swi.coodinate = coodinate
        return self.swi

    def parse_operation_name(self, operation_name: str):
        operation_info = re.sub('_', ' ', operation_name).split()

        assert len(operation_info) >= 2
        pre_cut_line_num = int(operation_info[0])
        load_level = int(operation_info[1])
        pre_cut_line_list = [int(v) for v in operation_info[2:(2 + pre_cut_line_num)]]
        return pre_cut_line_num, load_level, pre_cut_line_list

    def parse_swx_name(self, swx_name: str):
        """
        解析swx文件的名称，得到故障切除线路和故障节点
        默认结构：a(b-c).swx
        """
        if 'bus' in swx_name:
            return self._parse_swx_name_old(swx_name)
        post_cut_line_index, fault_bus_index = None, None
        try:  # 有些名称不规则所以要try
            swx_info = re.sub('[.SWX()-]', ' ', swx_name.upper()).split()
            post_cut_line_index = int(swx_info[1])  # 默认这里就是dat读取到的line的原始顺序
            fault_bus_index = int(swx_info[2])  # 默认这里就是dat读取到的bus的原始顺序
        except:
            pass
        return post_cut_line_index, fault_bus_index

    def _parse_swx_name_old(self, swx_name: str):
        """结构：a(busb-busc(b)).swx, 只会出现在case39的0_"""
        swx_info = re.sub('[()-]', ' ', swx_name[:-4]).split()

        post_cut_line_index = -1
        for i, l in enumerate(self.dat.branch_name):
            if swx_info[1].ljust(8) in l and swx_info[2].ljust(8) in l:
                if post_cut_line_index == -1:
                    post_cut_line_index = i
                else:
                    raise ValueError('解析方式有误,出现了多条线路包含swx_info[1+2]！')
        if swx_info[1] == 'bus' + swx_info[3]:
            fault_bus_index = self.dat.bus_order[swx_info[1].ljust(8) + '100 ']
        else:
            fault_bus_index = self.dat.bus_order[swx_info[2].ljust(8) + '100 ']

        assert self.dat.bus_name[fault_bus_index] in self.dat.branch_name[post_cut_line_index]
        return post_cut_line_index, fault_bus_index


class RdGenOrganizer:
    """
    jy的文件组织方式
    lk的文件组织方式：
    _path全部以'/'结尾
    """
    def __init__(self, case_system, root_path, source_path, target_path, dat_in_root, swi_in_root):
        """

        @param case_system:
        @param root_path:
        @param source_path:
        @param target_path:
        @param dat_in_root:
        @param swi_in_root:
        """
        self.case_system = str(case_system)
        self.root_path = root_path + self.case_system + '/'
        self.source_path = source_path
        self.target_path = target_path
        self.dat_in_root = dat_in_root
        self.swi_in_root = swi_in_root
        self.dat = None
        self.swi = None

    def get_dat(self, operation_folder: str = None):
        if self.dat_in_root or not operation_folder:
            if self.dat is None:
                self.dat = DAT.build_from_folder(self.source_path)
        else:
            self.dat = DAT.build_from_folder(self.source_path + operation_folder + '/')
        return self.dat

    def get_swi(self, coodinate: str = 'BS', operation_folder: str = None):
        if self.swi_in_root or not operation_folder:
            if self.swi is None:
                self.swi = SWI.build_from_folder(self.source_path)
        else:
            self.swi = SWI.build_from_folder(self.source_path + operation_folder + '/')
            self.dat = self.swi.temp_dat
        self.swi.coodinate = coodinate
        return self.swi

    def parse_swx_name(self, swx_name: str):
        """
        解析swx文件的名称，得到故障切除线路和故障节点
        默认结构：a(b-c).swx
        """
        if 'bus' in swx_name:
            return self._parse_swx_name_old(swx_name)
        post_cut_line_index, fault_bus_index = None, None
        try:  # 有些名称不规则所以要try
            swx_info = re.sub('[.SWX()-]', ' ', swx_name.upper()).split()
            post_cut_line_index = int(swx_info[1])  # 默认这里就是dat读取到的line的原始顺序
            fault_bus_index = int(swx_info[2])  # 默认这里就是dat读取到的bus的原始顺序
        except:
            pass
        return post_cut_line_index, fault_bus_index

    """st的组织习惯，位于/39rd_gen/"""
    def parse_operation_name(self, operation_name: str):
        operation_info = re.sub('_', ' ', operation_name).split()

        assert len(operation_info) >= 3
        pre_cut_line_num = int(operation_info[0])
        load_level = int(operation_info[1]) + int(operation_info[-1]) / 1000
        pre_cut_line_list = [int(v) for v in operation_info[2:(2 + pre_cut_line_num)]]
        return pre_cut_line_num, load_level, pre_cut_line_list

    def _parse_swx_name_old(self, swx_name: str):
        """结构：a(busb-busc(b)).swx, 只会出现在case39的0_"""
        swx_info = re.sub('[()-]', ' ', swx_name[:-4]).split()

        post_cut_line_index = -1
        for i, l in enumerate(self.dat.branch_name):
            if swx_info[1].ljust(8) in l and swx_info[2].ljust(8) in l:
                if post_cut_line_index == -1:
                    post_cut_line_index = i
                else:
                    raise ValueError('解析方式有误,出现了多条线路包含swx_info[1+2]！')
        if swx_info[1] == 'bus' + swx_info[3]:
            fault_bus_index = self.dat.bus_order[swx_info[1].ljust(8) + '100 ']
        else:
            fault_bus_index = self.dat.bus_order[swx_info[2].ljust(8) + '100 ']

        assert self.dat.bus_name[fault_bus_index] in self.dat.branch_name[post_cut_line_index]
        return post_cut_line_index, fault_bus_index