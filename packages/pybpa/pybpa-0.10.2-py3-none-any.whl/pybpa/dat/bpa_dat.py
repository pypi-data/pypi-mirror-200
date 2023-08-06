# -*- coding:utf-8 -*-
"""
# Name:         transient_stability: bpa_dat
# Author:       MilkyDesk
# Date:         2021/6/29 9:59
# Description:
#   
"""
import os
from collections import defaultdict

from typing import List

import numpy as np
import pandas as pd

from ..base import bpa_annotation
from ..base.bpa_uid import _OneNameUid
from . import bpa_dat_before_data, bpa_dat_data
from ..base.bpa_base import _to_card
from ..base.bpa_uid import *
from ..base.bpa_str import bpa_card_line
import networkx as nx
"""
dat结构：
一级语句
网络数据前的控制语句
网络数据
控制语句
一级语句
"""


class DAT:
    """
    定位：
    提供DAT_Card的管理工具
    行为：
    1. 初始化: 读取文件
    2. __str__: 反向文本化功能。应该与_Card的组织类似。
    @todo 未来要加入许多其他元件的数据结构，所以会考虑重写这部分
    数据基础：
    lines: List of _Cards
    基础索引(行号)：
    can, cdt, cc1, cc2
    高级对象:
    bus, branch, gen: List of _Cards
    高级索引: list编号, uid_str
    *_name: List of uid_str
    *_order: {uid_str: #*}
    *_indexs: {uid_str: _Cards}
    branch_bus_order: List of [#bus, #bus]
    gen_bus_order: List of #bus
    """
    annotation_card = {'.', ' ', 'C'}
    symmeyty_line_card_set = {'L ', 'LD', 'LM', 'T ', 'TP', 'R ', 'RZ', 'RV', 'RQ', 'RP', 'RN', 'RM'}
    asymmeyty_line_card_set = {'L+', 'E '}
    dc_line_card_set = {'LD', 'LM', 'LY', 'LZ', 'BZG', 'LZG', 'DC'}
    dc_bus_card_set = {'BZ', 'BZ+', 'BA', 'BA1', 'BA2', 'BB', 'BD', 'BM'}
    line_card_set = {'L ', 'LD', 'LM', 'T ', 'TP', 'R ', 'RZ', 'RV', 'RQ', 'RP', 'RN', 'RM', 'L+', 'E ', 'LY', 'LZ', 'BZG', 'LZG'}
    bus_card_set = {'B ', 'BV', 'BM', 'BQ', 'BS', 'BT', 'BE', 'BF', 'BJ', 'BK', 'BL', 'BX', 'BD', '+', 'X ','BA',
                    'BZ', 'BZ+', 'BC', 'BB', 'BA1', 'BA2'}
    gen_card_set = {'B ', 'BQ', 'BM', 'BQ', 'BS', 'BT', 'BE', 'BF', 'BJ', 'BK', 'BL', 'BX', 'BD', '+', 'X ', 'BA', 'BZ',
                    'BC'}
    zone_card_set = {'I'}
    PZ_card_set = {'PZ'}
    cal_Y_card_type = ['L ', 'T ', 'TP', 'E ']  # 只会计算这些卡的导纳

    def __init__(self, *p):
        self.cards, self.can, self.cc1, self.cdt, self.cc2 = p
        self.cdt_branch = []
        self.cdt_bus = []
        self.cdt_zone = []
        self.cdt_PZ = []
        self.bus, self.bus_indexs, self.bus_order, self.bus_name, \
        self.branch, self.branch_indexs, self.branch_order, self.branch_name, self.branch_bus_order, \
        self.gen, self.gen_indexs, self.gen_order, self.gen_name, self.gen_bus_order, self.zone_exchange,\
        self.bus_zone, self.gen_zone, self.bus_zone_type, self.gen_zone_type, self.PZ = self.get_data_struct()
        self.gen_info = None
        self.branch_y, self.y_matrix,self.branch_X_order, self.branch_X,self.trans_bus_name = None, None, None, None, None
        self.bus_y = None
        # self.Converter, self.hydropower_station, self.photovoltaic, self.Wind_power = self.special_station()
        self.iso_delete_bus_order={}
        self.get_branch_y()
        self.get_Y_matrix()
        self.get_line_X()
        self.mva_base = 100
        self.load_level = 1.

        self.describe()

    def describe(self):
        """
        todo 汇报当前的dat长啥样
        节点电压等级及数量，
        各电压等级支路数量，变压器数量
        直流线路数量，直流线路是否造成孤岛
        新能源渗透率
        """
        print('\n\t***  DAT.describe() ***\t\n')
        import textwrap
        # 统计各电压等级节点数
        vol_level = [800, 500, 220, 110, 10, 0.48, 0.4]
        vol_count = {v: 0 for v in vol_level}
        from collections import Counter
        vol_bases = Counter([b[0].get_value('BASE') for b in self.bus_indexs.values()])
        vol_bases = [[k, v] for k, v in vol_bases.items()]
        vol_bases.sort(reverse=True)
        for v in vol_count.keys():
            for ll, n in vol_bases:
                if ll > v:
                    vol_count[v] += n
        ac_bus = [b for b in self.bus_indexs.values() if b[0].type not in self.dc_bus_card_set]
        dc_bus = [b for b in self.bus_indexs.values() if b[0].type in self.dc_bus_card_set]
        print(f"节点统计: {len(self.bus_indexs)}, \n\t" +
              textwrap.fill(f"{', '.join([str(k) + 'kV及以上节点数: ' + str(v) for k, v in vol_count.items() if v > 0])}",
                            width=120) +
              f"\n\t其中，交流节点卡: {Counter([b[0].type for b in ac_bus])}" +
              f"\n\t其中，直流节点卡: {Counter([b[0].type for b in dc_bus])}" +
              f'\n\t参与统计的卡类型: {self.bus_card_set}')

        # 统计线路数
        branch_type = Counter([b.get_value('TYPE') for b in self.branch])
        bt1 = {k: v for k, v in branch_type.items() if k in self.cal_Y_card_type}
        bt2 = {k: v for k, v in branch_type.items() if k not in self.cal_Y_card_type}
        ac_branch = [b for b in self.branch_indexs.values() if b[0].type not in self.dc_line_card_set]
        dc_branch = [b for b in self.branch_indexs.values() if b[0].type in self.dc_line_card_set]
        print(f"支路统计: {len(self.branch_indexs)}, 支路卡总计: {len(self.branch)}" +
              f"\n\t参与计算的支路卡统计  : {bt1}" +
              f'\n\t不参与计算的支路卡统计: {bt2}' +
              f"\n\t其中，交流支路卡: {Counter([b[0].type for b in ac_branch])}" +

              f"\n\t其中，直流支路卡: {Counter([b[0].type for b in dc_branch])}")

        # 同步网连通分量

        node_list = [bus[0].order for bus in ac_bus]
        edge_list = [self.branch_bus_order[b[0].order] for b in ac_branch]
        G=nx.Graph()
        G.add_nodes_from(node_list)
        G.add_edges_from(edge_list)
        sub_list = nx.connected_components(G)
        sub_list = list(sub_list)
        print(f'网络连通分量大小: {[len(sl) for sl in sub_list]}')

        # 卡类型连接情况
        print(f'\n节点-线路连接情况概览')
        bus_card = {}
        for branch_name, branch_list in self.branch_indexs.items():
            for branch in branch_list:
                bus_card[branch.name1] = bus_card.get(branch.name1, [])
                bus_card[branch.name1].append(branch.type)
                bus_card[branch.name2] = bus_card.get(branch.name2, [])
                bus_card[branch.name2].append(branch.type)
        bus_types = {}
        bus_count = {}
        for bus_name, bus_list in self.bus_indexs.items():
            t = [b.type for b in bus_list]
            t.sort()
            if (len(t) == 1 and t[0] == '+') \
                or (len(t) > 1 and ((len(t) == 1 or t[1][0] != 'B') or t not in [['BZ', 'BZ+'], ['BA', 'BA1', 'BA2']])):
                print(f'节点: {bus_name} 存在预期之外的卡组合: {t}')
            for tt in t:
                bus_count[tt] = bus_count.get(tt, 0) + 1
            t = t[0]
            bus_types[t] = bus_types.get(t, [])
            bus_types[t] += bus_card[bus_name]
        for bus_type in bus_types.keys():
            bus_types[bus_type] = Counter(bus_types[bus_type])

        for k, v in bus_types.items():
            print(f'{k}: {bus_count[k]} -- {", ".join([f"{kk}: {vv}" for kk, vv in v.items()])}')



        print('\n\t***  DAT.describe() end ***\t\n')

        return {'ac_bus': ac_bus, 'dc_bus': dc_bus, 'ac_branch': ac_branch, 'dc_branch': dc_branch, 'graph': G}

    def get_data_struct(self):
        """
        目标是建立起【不依赖文件结构的】电网对象的索引，包括：
        1. 全集: bus, branch
        2. 根据名称组织起来的卡片: bus_indexs, branch_indexs
        3. 根据出现次序给定的顺序：bus_order， branch_order
        4. 将所有bus，branch对象按照此顺序标上序号
        @note: 此后出现的数据结构里，只有order字段，没有name字段。
        @return:
        """
        bus_indexs, branch_indexs, bus_order, branch_order, gen_indexs, gen_order,bus_zone,gen_zone= {}, {}, {}, {}, {}, {},{},{}
        bus_name, branch_name, gen_name, gen_bus_order, branch_bus_order = [], [], [], [], []
        bus_zone_type, gen_zone_type = defaultdict(list), defaultdict(list)

        bus = [self.cards[f]
               for f in self.cdt
               if self.cards[f].type in DAT.bus_card_set]
        self.cdt_bus = [f
               for f in self.cdt
               if self.cards[f].type in DAT.bus_card_set]
        gen = []
        n_bus = 0
        n_gen = 0
        for i, b in enumerate(bus):
            if b.name in bus_indexs:
                bus_indexs[b.name] += [b]
            else:
                bus_indexs[b.name] = [b]
                bus_order[b.name] = n_bus
                bus_name += [b.name]
                n_bus += 1
            b.order = bus_order[b.name]
            b.index = i#能映射到实际文件行数
            if _bus_has_gen(b):
                g_name = b.name + ' '
                gen_indexs[g_name] = [b]  # 默认了每个节点只有一台发电机
                gen_order[g_name] = n_gen
                gen_name += [g_name]
                gen_bus_order += [bus_order[b.name]]
                gen += [b]
                n_gen += 1

        branch = [self.cards[f]
                  for f in self.cdt
                  if self.cards[f].type in DAT.line_card_set]
        self.cdt_branch = [f
                  for f in self.cdt
                  if self.cards[f].type in DAT.line_card_set]
        zone_exchange = [self.cards[f]
                         for f in self.cdt
                         if self.cards[f].type in DAT.zone_card_set]
        PZ_card = [self.cards[f]
                         for f in self.cc1
                         if self.cards[f].type in DAT.PZ_card_set]
        self.cdt_zone = [f
                         for f in self.cdt
                         if self.cards[f].type in DAT.zone_card_set]
        self.cdt_PZ = [f
                         for f in self.cc1
                         if self.cards[f].type in DAT.PZ_card_set]
        n_branch = 0
        for i, l in enumerate(branch):
            if l.name in branch_indexs:
                branch_indexs[l.name] += [l]
            else:
                branch_indexs[l.name] = [l]
                branch_order[l.name] = n_branch
                branch_bus_order.append([bus_order[l.name1], bus_order[l.name2]])
                branch_name += [l.name]
                n_branch += 1
            l.order = branch_order[l.name]
            l.index = i  # 能映射到实际文件行数
            l.order1 = bus_order[l.name1]
            l.order2 = bus_order[l.name2]

        branch_bus_order = np.array(branch_bus_order)
        return bus, bus_indexs, bus_order, bus_name, \
               branch, branch_indexs, branch_order, branch_name, branch_bus_order, \
               gen, gen_indexs, gen_order, gen_name, gen_bus_order,zone_exchange,bus_zone,gen_zone,bus_zone_type,\
               gen_zone_type,PZ_card

    def __str__(self):
        """将结构化的card还原回str行"""
        return '\n'.join([x if type(x) is str else str(x) for x in self.cards]) + '\n'

    def save_to_file(self, path, text_prefix=None):
        """
        想写入哪里，直接写完整路径即可。会直接递归地创建路径。
        todo 未来与swi的方法合并
        :param path: 有没有以.dat结尾都可以。
        :param text_prefix: 正文的开头，用来记录一些信息的。
        :return:
        """
        if path[-4:].lower() != '.dat':
            path += '.dat'
        os.makedirs(os.path.dirname(path), exist_ok=True)
        file = open(path, 'w')
        if text_prefix:
            file.write(text_prefix)
        file.write(str(self))
        file.close()

    def read_pfo(self, dat_path, pu=False, type ='BPA'):
        """
        #  1. 并不确定如何处理shuntQ:
         2022年11月5日 data.utils的处理，归入负荷。因为这些是静态的。Q1(使用的)+Q3(未投入), Q2(已有的)不包括在内
         参考：PSD-BPA潮流说明书4.5.3，P103最上
         "如果在潮流数据中设定了BE节点类型，为了保持该类型节点的电压值，程序计算时会在这些类型节点强制增加无功补偿，应查看潮流结果文件（PFO为后缀
         的文件）中“未安排无功的节点列表”，该列表中显示了所有BE节点强制增加的无功，如果为正值，表示增加了电容器，缺少无功，需要增加无功进行补偿；
         反之，表示增加了电抗器，无功较多，应减少无功补偿。"
        #  2. 并不确定如何处理恒功率负荷
        :param dat_path:
        :param pu: 是否对功率标幺化
        :return:
        """
        n_bus = len(self.bus_order)

        # 读pfo文件
        # pfo_lines = open(dat_path[:-4] + '.pfo', 'rb').readlines()
        if type=='BPA':
            pfo_lines = open(dat_path[:-4] + '.pfo', 'rb').readlines()
            # 检查是否收敛：
            key = '不收敛'.encode('gbk')
            for l in pfo_lines:
                if key in l:
                    return None

            # 只提取 bus_info_start_flag 那一段
            stl = [i for i, l in enumerate(pfo_lines) if '*  节点相关数据列表'.encode('gbk') in l]
            # 有些潮流结果有问题，但是又不想让程序中断
            if len(stl) == 0:
                return None
            stl = stl[0]
            edl = [i for i, l in enumerate(pfo_lines[stl:]) if '------'.encode('gbk') in l][1] + stl
            r = pfo_lines[stl:edl]
            sstl = []

            sstl = [i for i, l in enumerate(r) if b'\r\n' == l]
            if sstl:
                sstl = sstl[0] + 1
            else:
                sstl = 3
            r2 = r[sstl:]
            for i in range(len(r2)):
                s = r2[i]
                if s[45:46] == b' ':  # 'PF'
                    s = s[:45] + b'0' + s[46:]
                if s[97:98] == b' ':  # 'TYPE'
                    s = s[:97] + b'*' + s[98:]
                if s[102:103] == b' ':  # 'OWNER'  @todo 注意所有者代码是3个字节，因此这里应该用完全的三个字节进行比较。
                    s = s[:102] + b'*' + s[103:]
                if s[108:110] == b'  ':  # 'ZONE'
                    s = s[:108] + b'* ' + s[109:]
                r2[i] = s[:-2].decode('gbk', errors='ignore')
            df = pd.DataFrame(r2)[0].str.split(r'\s+|\s*/\s*|\n', expand=True).drop([0], axis=1)

            # 重命名、数据类型转换
            df.columns = [BUS_NAME_STR, BUS_BASE_STR, 'V',
                          GEN_P, GEN_Q, 'PF', LOAD_P, LOAD_Q,
                          'SHUNTQ1', 'SHUNTQ2', 'SHUNTQ3',
                          'TYPE', 'OWNER', 'ZONE', VOLTAGE, ANGLE]
            df[[BUS_NAME_STR, 'TYPE', 'OWNER', 'ZONE']] = df[[BUS_NAME_STR, 'TYPE', 'OWNER', 'ZONE']].astype('str',
                                                                                                             copy=False)
            df[[BUS_BASE_STR, 'V', GEN_P, GEN_Q, 'PF', LOAD_P, LOAD_Q, 'SHUNTQ1', 'SHUNTQ2', 'SHUNTQ3', VOLTAGE, ANGLE]] = \
                df[[BUS_BASE_STR, 'V', GEN_P, GEN_Q, 'PF', LOAD_P, LOAD_Q, 'SHUNTQ1', 'SHUNTQ2', 'SHUNTQ3', VOLTAGE,
                    ANGLE]].astype('float', copy=False)
            df.loc[df['TYPE'] == '*', 'TYPE'] = ' '
            df.loc[df['OWNER'] == '*', 'OWNER'] = ' '
            df.loc[df['ZONE'] == '*', 'ZONE'] = ' '

            # 标幺值转换
            if pu:
                df[[GEN_P, GEN_Q, LOAD_P, LOAD_Q, 'SHUNTQ1', 'SHUNTQ2', 'SHUNTQ3']] /= self.mva_base
                df['V'] /= df['BASE']
                # todo pfo中的pf是什么，为什么要标幺化？
                df['SHUNTB'] = df['SHUNTQ1'].copy().add(df['SHUNTQ3']).div(df[VOLTAGE]).div(df[VOLTAGE])
            else:
                print('dat.read_pfo: pu==False, 功率没有标幺化，另外没有计算SHUNTB，可能出错。')

            # 处理pfo中 节点电压等级被舍入为0.7的问题
            if not hasattr(self, 'pfo_name_dict'):
                self.pfo_name_dict = {(BNameFormatter.get_name(name[:-4], round(float(name[-4:]), 1))): name
                                      for name in self.bus_name}

            pfo_b_names = list(map(BNameFormatter.get_name, df[BUS_NAME_STR], df[BUS_BASE_STR]))
            pfo_bus_name = [self.pfo_name_dict.get(pfo_b_name) for pfo_b_name in pfo_b_names]

            df.index = [self.bus_order[name] for name in pfo_bus_name]
            df[BUS_NAME_STR] = pfo_bus_name

            # todo
            #  1. 并不确定如何处理shuntQ
            #  2. 并不确定如何处理恒功率负荷
        elif type == 'DSP':
            pfo_lines = open(dat_path, 'rb').readlines()
            # 检查是否收敛：
            key = '不收敛'.encode('gbk')
            for l in pfo_lines:
                if key in l:
                    return None

            # 针对粤西场景，需要提取场景相关线路的功率
            stl = [i for i, l in enumerate(pfo_lines) if '*  节点潮流数据列表'.encode('gbk') in l]
            # 有些潮流结果有问题，但是又不想让程序中断
            if len(stl) == 0:
                return None
            stl = stl[0]
            edl = [i for i, l in enumerate(pfo_lines[stl:]) if '------'.encode('gbk') in l][1] + stl
            r = pfo_lines[stl+1:edl]
            # sstl = []
            #
            # sstl = [i for i, l in enumerate(r) if b'\r\n' == l]
            # if sstl:
            #     sstl = sstl[0] + 1
            # else:
            #     sstl = 0
            tt = []
            for i in range(len(r)):
                s = r[i]#每一行
                if s[0:7] !=b'       ':#是首段节点
                    bus1_name = s[0:8].replace(b' ',b'').decode('gbk', errors='ignore')
                    bus1_base = s[9:14].replace(b' ',b'').decode('gbk', errors='ignore')
                    bus1_V = s[16:22].replace(b' ',b'').decode('gbk', errors='ignore')
                    bus1_theta = s[26:32].replace(b' ',b'').decode('gbk', errors='ignore')
                elif s[7:15] !=b'        ' and '直流'.encode('gbk') not in s:#是末端节点
                    bus2_name = s[7:15].replace(b' ',b'').decode('gbk', errors='ignore')
                    bus2_base = s[16:21].replace(b' ',b'').decode('gbk', errors='ignore')
                    line_flag = s[23:24].replace(b' ',b'').decode('gbk', errors='ignore')#支路并联号
                    P_line = s[37:44].replace(b' ',b'').decode('gbk', errors='ignore') #支路有功
                    Q_line = s[52:60].replace(b' ',b'').decode('gbk', errors='ignore') #支路无功
                    tt.append([bus1_name,bus1_base,bus1_V,bus1_theta,bus2_name,bus2_base,line_flag,P_line,Q_line])
                else:
                    pass
            df = pd.DataFrame(tt)
        return df.sort_index()

    def get_branch_y(self):
        if self.branch_y is not None:
            return self.branch_y
        n_line = len(self.branch_order)
        y = np.zeros([n_line, 4], dtype=np.complex_)

        cal_branch, cal_count, ignored_count = 0, {}, {}
        for bidx, blist in enumerate(self.branch_indexs.values()):
            ################################
            #            重  要            #
            ################################
            order_name1, order_name2 = blist[0].name1, blist[0].name2  # 所有的1和2，都是按照第一张卡的这个顺序

            # 收集需要计算的卡列表
            cal_list = []
            for b in blist:
                btype = b.type
                if btype in self.cal_Y_card_type:
                    cal_list.append(b)
                    cal_count[btype] = cal_count.get(btype, 0) + 1
                else:
                    ignored_count[btype] = ignored_count.get(btype, 0) + 1
            # 工业系统验证，所有的同起止点多线路卡情况，在self.cal_Y_card_type过滤后都是同种卡
            if len(cal_list) == 0:
                print(f'支路 {blist[0].name}没有可以计算的导纳类型，在导纳矩阵上可能因此拓扑断开')
                continue
            """
            from collections import Counter
            Counter([len(ll) for ll in dat.branch_indexs.values()])  # 查看所有的多重线路情况
            a = [[l for l in ll if l.type in dat.cal_Y_card_type] for ll in dat.branch_indexs.values() if len(ll) >1]
            Counter([len(aa) for aa in a])
            all([all([ll[0].type == i.type for i in ll]) for ll in a])  # 输出True表示所有的多重线路都是同种类型的卡
            """
            cal_branch += 1
            # 按并联线路分组
            cal_dict = {}
            for b in cal_list:
                key = b.get_value(CKT_ID)
                cal_dict[key] = cal_dict.get(key, [])
                cal_dict[key].append(b)
            # 每组并联线路，计算串联分段
            for key, value in cal_dict.items():
                if len(value) > 1:
                    print(f'支路 {value[0].name}存在串联支路情况，其串联等值模型的中间对地支路没有计入!(出现一次表示有一条支路存在串联情况)')
                yyyy = {}
                for l in value:
                    sec_y = l.get_y()
                    if l.name1 == order_name1:  # 卡同顺序，直接放置
                        yyyy[l.get_value(SEC_ID)] = sec_y
                    else:  # 卡不同顺序，反置
                        yyyy[l.get_value(SEC_ID)] = sec_y[::-1]
                # 合并串联分段
                sec_st, sec_ed = min(yyyy.keys()), max(yyyy.keys())
                y11, y22 = yyyy[sec_st][0] + yyyy[sec_st][1], yyyy[sec_ed][3] + yyyy[sec_ed][2]  # y11 + y12 == y10对地支路
                y12, y21 = -1 / sum([(1 / suby[1]) for suby in yyyy.values()]), -1 / sum([(1 / suby[2]) for suby in yyyy.values()])

                y[bidx] += [y11 + y12, -y12, -y21, y22 + y21]


        self.branch_y = y
        print(f'在计算导纳矩阵的过程中，对系统{len(self.branch)}张支路卡，一共计算了:{cal_branch}条支路（图意义上的）。其中：\n'
              f'\t计及的卡类型及数量: {cal_count} \n\t忽略的卡类型及数量: {ignored_count}')
        return self.branch_y

    def get_bus_y(self):
        """
        计算节点的并联导纳
        :return:
        """
        if self.bus_y is not None:
            return self.bus_y

        yb = np.zeros(len(self.bus_indexs), dtype=np.complex_)
        for b in self.bus_name:
            bus_list = self.bus_indexs[b]
            for bus in bus_list:
                if bus.type[0] == 'B' and bus.type not in self.dc_bus_card_set:
                    v = bus.get_value(BUS_BASE_STR)
                    pb = bus.get_value('SHUNTZP') + 1j * bus.get_value('SHUNTZQ')  # todo 确认功率方向 v4.6.2 p68
                    ib = np.conjugate(pb / v)
                    yb[self.bus_order[b]] += (ib / v)
        self.bus_y = yb
        return self.bus_y


    def get_Y_matrix(self):
        """
        2021年11月4日 已与matpower所用的Ybus核对过一致。
        matlab: y = makeYbus(case39())
        @return:
        """
        if self.y_matrix is not None:
            return self.y_matrix

        print(f'dat.get_Y_matrix(): 只计算下列支路{self.cal_Y_card_type}')

        n_bus = len(self.bus_order)
        n_line = len(self.branch_order)

        y = np.zeros([n_bus, n_bus], dtype=np.complex_)
        ys = self.get_branch_y()
        for i, b in enumerate(self.branch_bus_order):
            # y11, y12, y21, y22的格式. 1和2的顺序，以第一张卡的顺序为准
            y[b[0], b[0]] += ys[i, 0]
            y[b[0], b[1]] += ys[i, 1]
            y[b[1], b[0]] += ys[i, 2]
            y[b[1], b[1]] += ys[i, 3]
        yb = self.get_bus_y()
        y += np.diag(yb)

        '''
        from pypower.case39 import case39
        c = case39()
        from pypower.runpf import runpf
        # debug模式下断点在runpf的makeYbus处
        runpf(c)
        '''


        self.y_matrix = y

        coo_mask = [[i, i] for i in range(n_bus)]
        coo_mask.extend([[self.branch_indexs[l][0].order1, self.branch_indexs[l][0].order2]
                         for l in self.branch_name])
        coo_mask.extend([[self.branch_indexs[l][0].order2, self.branch_indexs[l][0].order1]
                         for l in self.branch_name])

        self.coo_mask = np.array(coo_mask, dtype=np.int_).transpose()
        self.line_loc_in_coo = np.array([[n_bus + i, n_bus + n_line + i] for i in range(n_line)], dtype=np.int_)

        return self.y_matrix

    def get_line_X(self):
        """
        todo 代码未审核
        """
        count=0
        # if self.line_X is not None:
        #     return self.line_X
        # 需要 bus_dict{name: index}, line_dict
        # n_bus = len(self.bus_order)
        n_line = len(self.branch)
        branch_X_order = [[]for i in range(30000)]
        branch_X = [[] for i in range(30000)]
        temp=[]
        trans_bus_name = []
        for i, b in enumerate(self.branch):
            if self.bus_indexs and b.name2 in self.bus_indexs:
                # line_card_set = {'L ', 'LD', 'LM', 'T ', 'TP', 'R ', 'RZ', 'RV', 'RQ', 'RP', 'RN', 'RM', 'L+', 'E '}
                if (b.type =='L '):
                    if b.values[b.field_index['CKT ID']]=='1' and self.branch[i+1].values[b.field_index['CKT ID']]=='2'  and self.branch[i+2].values[b.field_index['CKT ID']]!='3'\
                        and b.values[b.field_index['NAME1']]==self.branch[i + 1].values[b.field_index['NAME1']] and b.values[b.field_index['NAME2']]==self.branch[i + 1].values[b.field_index['NAME2']]:
                        branch_X_order[count]=([self.bus_order[b.name1], self.bus_order[b.name2]])
                        branch_X[count]=float(b.values[b.field_index['X']])/2
                        temp.append(self.bus_order[b.name1])
                        temp.append(self.bus_order[b.name2])
                        count=count+1
                        i = i+1
                    if b.values[b.field_index['CKT ID']]=='1' and self.branch[i+1].values[b.field_index['CKT ID']]=='2' and self.branch[i+2].values[b.field_index['CKT ID']]=='3'\
                        and b.values[b.field_index['NAME1']]==self.branch[i + 1].values[b.field_index['NAME1']] and b.values[b.field_index['NAME2']]==self.branch[i + 1].values[b.field_index['NAME2']]\
                       : #and b.values[b.field_index['NAME1']]==self.branch[i + 2].values[b.field_index['NAME1']] and b.values[b.field_index['NAME2']]==self.branch[i + 2].values[b.field_index['NAME2']]
                        branch_X_order[count]=([self.bus_order[b.name1], self.bus_order[b.name2]])
                        branch_X[count]=float(b.values[b.field_index['X']])/3
                        temp.append(self.bus_order[b.name1])
                        temp.append(self.bus_order[b.name2])
                        count=count+1
                        i = i+2
                    else:
                        branch_X_order[count]=([self.bus_order[b.name1], self.bus_order[b.name2]])
                        branch_X[count]=float(b.values[b.field_index['X']])
                        temp.append(self.bus_order[b.name1])
                        temp.append(self.bus_order[b.name2])
                        count=count+1
                if (b.type =='T '):
                    # X[count].append([b.name1,b.name2,self.bus_order[b.name1],self.bus_order[b.name2],float(b.values[b.field_index['X']])])
                    branch_X_order[count]=([self.bus_order[b.name1], self.bus_order[b.name2]])
                    branch_X[count]=float(b.values[b.field_index['X']])
                    temp.append(self.bus_order[b.name1])
                    temp.append(self.bus_order[b.name2])
                    trans_bus_name.append([b.name1,b.name2])
                    count=count+1
                if (b.type =='LM'):
                    branch_X_order[count]=([self.bus_order[b.name1], self.bus_order[b.name2]])
                    branch_X[count]=2*np.pi*50*10e-3*float(b.values[b.field_index['L']])
                    temp.append(self.bus_order[b.name1])
                    temp.append(self.bus_order[b.name2])
                    count=count+1
                if (b.type =='LD'):
                    branch_X_order[count]=([self.bus_order[b.name1], self.bus_order[b.name2]])
                    if b.values[b.field_index['L']]==0:
                        branch_X[count]=  0.1     # 直流连线：假定电抗很大，不受稳定影响
                    if b.values[b.field_index['L']]!=0:
                        branch_X[count] = 2 * np.pi * 50 * 10e-3 * float(b.values[b.field_index['L']])
                    temp.append(self.bus_order[b.name1])
                    temp.append(self.bus_order[b.name2])
                    count=count+1
                if (b.type =='R '):  # 变压器 视为强连接
                    branch_X_order[count]=([self.bus_order[b.name1], self.bus_order[b.name2]])
                    branch_X[count] = 0.00001
                    temp.append(self.bus_order[b.name1])
                    temp.append(self.bus_order[b.name2])
                    count=count+1



        del (branch_X_order[count:])
        del (branch_X[count:])

        self.branch_X_order = branch_X_order
        self.branch_X = branch_X
        self.trans_bus_name = trans_bus_name

        return self.branch_X_order, self.branch_X, self.trans_bus_name



    @staticmethod
    def build_from(path):
        """
        从文件夹或者文件中新建实例,如果是从文件夹，只会找文件夹中第一个出现的。
        :param path:
        :return:
        """
        if os.path.isfile(path):
            if '.dat' in path.lower():
                lines = open(path, 'rb').readlines()
                return DAT.build_from_lines(lines)
        elif os.path.isdir(path):
            for f in os.listdir(path):
                if '.dat' in f.lower():
                    lines = open(path + '/' + f, 'rb').readlines()
                    return DAT.build_from_lines(lines)
        raise ValueError('cannot find .dat file in path!')

    @staticmethod
    def std_dat(dat_path):
        # for f in os.listdir(folder_path):
        #     if '.dat' in f.lower():
            lines = open(dat_path, 'rb').readlines()
            lines = [bpa_card_line(line) for line in lines]
            dat_path = dat_path.replace('.DAT','_std.DAT')
            dat_path = dat_path.replace('.dat', '_std.dat')
            pathn = dat_path
            with open(pathn,'w') as filen:
                for linen in lines:
                    linen = str(linen, 'gbk')+'\n'
                    filen.write(linen)
            print('std=====>',pathn)
            filen.close()
            return pathn

    @staticmethod
    def build_from_lines(ll: List[str]):
        #ready_for_encoder:如果是解析后为修改DAT做准备，
        lines = []
        can = []
        cc1 = []
        cdt = []
        cc2 = []

        position = 1

        ll = [bpa_card_line(line) for line in ll]
        for i, l in enumerate(ll):
            if l == b'\n':
                lines.append('\n')
                continue

            c = _to_card(l, bpa_annotation.card_types)
            if c:
                lines.append(c)
                can.append(i)
                continue

            c = _to_card(l, bpa_dat_before_data.card_types)
            if c:
                lines.append(c)
                cc1.append(i)
                continue

            c = _to_card(l, bpa_dat_data.card_types)
            if c and position:
                lines.append(c)
                cdt.append(i)
                continue
            else:
                position = 0

            c = _to_card(l, bpa_dat_before_data.card_types)
            if c:
                lines.append(c)
                cc2.append(i)
                continue

            print('unknown bline! transform to Annotation Card: ', l)
            lines.append(_to_card(b'.' + l, bpa_annotation.card_types))
            position = 1

        return DAT(lines, can, cc1, cdt, cc2)


def _bus_has_gen(bus: _OneNameUid):
    """
    作用:判断这个bus是否有发电机.
    DAT文件里面，并没有明确指出发电机，所以只能我们自己根据节点卡判断.
    怎么判断呢？就是检查这个bus类是否具有GEN_P这个字段，如果有，并且GEN_P这个字段对应的值不为0，那么就认为这个bus存在发电机。
    之所以要重复判断，是考虑到我们以后可能会开机但不安排有功无功
    @param bus:
    @return:
    """
    if (GEN_P in bus.field_index and bus.get_value(GEN_P)) \
            or (GEN_P_MAX in bus.field_index and bus.get_value(GEN_P_MAX)) \
            or (GEN_Q_MIN in bus.field_index and bus.get_value(GEN_Q_MIN)) \
            or (GEN_Q_MAX in bus.field_index and bus.get_value(GEN_Q_MAX)):
        return True
    return False

