# -*- coding:utf-8 -*-
"""
# Name:         transient_stability: bpa_swi
# Author:       MilkyDesk
# Date:         2021/6/25 11:19
# Description:
#   定义swi类
"""

# ------------------------- fields --------------------------
import os

from typing import List

import pandas as pd

from .bpa_swi_control_and_model import SwiFF
from ..base.bpa_base import _to_card, _Field
from ..base.bpa_str import bpa_card_line
from ..dat.bpa_dat import DAT
from ..swi import bpa_swi_control_and_model as CM, bpa_swi_output as O
from ..base import bpa_annotation as A
from ..base.bpa_uid import *


# ------------------------- fields --------------------------

class SWI:
    """
    定位：
    提供Swi_Card的管理工具
    行为：
    1. 初始化: 读取文件
    2. __str__: 反向文本化功能。应该与_Card的组织类似。
    """
    annotation_card = {'.', ' ', 'C'}
    control_model_card = {'PARA_FILE', 'CASE', 'F0', 'F1', 'FF', 'LS', 'FLT', 'M', 'E', 'F', 'O', 'S', 'I', 'LN', 'G'}
    output_card = {'90', 'B', 'BH', 'GH', 'GHC', 'G', 'GP', 'LH', 'L', 'LC', 'DH', 'D', 'RH', 'R', 'PY', 'OBV', 'OGM',
                   'OLT', '99', 'OMW'}

    control_format = 'I1'
    """swi文件输出卡的默认控制格式"""

    base_reader = _Field(1, 5, BUS_BASE_STR, 'F5.0', 0).read
    base_writer = _Field(1, 4, BUS_BASE_STR, 'F4.0', 0).write


    def __init__(self, *p):
        self.lines, self.can, self.ccm, self.cop, self.cf0, self.cf1, self.cff, self.cpara_file, self.c90, self.c99, \
        self.linked_dat = p
        self.get_gen_info()
        self.swx_struct = self.get_output_struct()
        self.start_step = 0
        self.end_step = 400
        self.sim_step_mask = None
        self.steady_step, self.fault_step, self.clear_step = 9.5, 10.0, 15.0
        self.time_index = [self.steady_step, self.fault_step, self.clear_step]  # lsd文件中的信息
        self.coodinate = 'BS'

    def get_gen_info(self):
        """
        补充发电机信息到dat
        todo 2022年11月5日 对于PQ型新能源机组，应该被识别为发电机，但是Tj==0
        """
        df = pd.DataFrame(self.linked_dat.gen_name, columns=['NAME'])
        gen_name = self.linked_dat.gen_name
        for gen_card in [self.lines[i] for i in self.ccm if self.lines[i].name in gen_name]:
            if gen_card.name != 'NAME' and gen_card.name in gen_name:
                gen_i = self.linked_dat.gen_order[gen_card.name]
                for f_i in range(1, len(gen_card.fields)):
                    df.loc[gen_i, gen_card.fields[f_i].name] = gen_card.values[f_i]
        df['Tj'] = 2 * df['EMWS'] / df['MVA RATING']
        df['J'] = df['EMWS'] / ((50 * 2*np.pi)**2 / 2)
        self.linked_dat.gen_info = df

    def get_output_struct(self):
        """
        目标是得到输出文件的第几段，输出对象和输出字段
        似乎GH，BH卡的NDOT控制数据精度字段，对于读取程序来说并不会影响到？
        @return:
        """
        swx_struct = {'B': {}, 'L': {}, 'G': {}, 'D': {}, 'R': {}}
        for c in self.cop:
            card = self.lines[c]
            if 'H' in card.type or '9' in card.type:
                continue
            temp = [f.name
                    for f, v in zip(card.fields, card.values)
                    if f.format == SWI.control_format and v and v > 0]  # bpa_online竟然是1，bpa说明书是3
            if temp:
                if card.type in swx_struct:  # 此时是L卡
                    if card.name in swx_struct[card.type]:  # 如果LC卡信息已经在里面
                        swx_struct[card.type][card.name] = temp + swx_struct[card.type][card.name]
                    else:  # 如果LC卡信息还没在里面
                        swx_struct[card.type][card.name] = temp
                elif card.type == 'LC':  # 如果是LC卡
                    if card.name in swx_struct['L']:  # 如果L卡信息已经在里面
                        swx_struct['L'][card.name] = swx_struct['L'][card.name] + temp
                    else:  # 如果L卡信息还没在里面
                        swx_struct['L'][card.name] = temp
                elif card.type == 'OMW':
                    swx_struct['G'][card.name] = temp
                else:
                    print(f'输出卡 没有被统计到输出结构中！')

        return swx_struct

    def __str__(self):
        """将结构化的card还原回str行"""
        return '\n'.join([x if type(x) is str else str(x) for x in self.lines]) + '\n'

    def read_swx(self, swx_file, coordinate='self', get_label_method=None):
        if get_label_method is None:
            get_label_method = self.get_label
        # if not self.swx_struct:
        #     self.swx_struct = self.get_output_struct()
        # print(swx_file)  # debug
        f = open(swx_file, 'r')
        swx_lines = f.readlines()
        f.close()
        swx_lines = [l[:-1] for l in swx_lines if len(l) > 10]  # 作用：时间步的列宽为10，小于10的肯定放不下数据
        start_index = [i for i, l in enumerate(swx_lines) if '数据列表' in l and ' * ' in l]  # swx文件块起始行的特征
        start_index.append(len(swx_lines))
        blocks = [swx_lines[i:j] for i, j in zip(start_index[:-1], start_index[1:])]

        # assert len(self.swx_struct) == len(blocks)
        swx, pf = {k: {} for k in self.swx_struct.keys()}, {k: {} for k in self.swx_struct.keys()}
        err = False
        for b in blocks:
            if ' * 计算过程中的监视曲线数据列表' in b[0]:
                continue  # 不处理这个块。
            err = False
            try:
                t, name, idx, data1, data2 = self._parse_block(b)
                swx[t].update({idx: data1})
                pf[t].update({idx: data2})
            except:
                err = True
        if err:
            print(swx_file.split('/')[-2:], '\terr= ', err,
                  '\t已知问题，当swx仿真结果多于swi规定的版本（俩版本对不上时）的情况。')

        # 将功角转化为指定坐标系下
        label = None
        if swx['G']:
            g_gname_map = [i for i in range(len(self.linked_dat.gen_name)) if i in swx['G']]
            if coordinate == '滞后':
                swx = self.ref_to_lag_gen(swx, g_gname_map)
            elif coordinate == 'COI':
                swx = self.ref_to_coi(swx, g_gname_map)

        # 打标签，将字典转换为断面, 默认有发电机
        label = get_label_method(swx, g_gname_map)
        pfs = self.swx2pf_section(pf)

        # 截断和重新组织swx
        for k, v in swx.items():
            if v:
                for kk, vv in v.items():
                    v[kk] = vv.iloc[self.start_step: self.end_step, :]

        return swx, pfs, label

    def ref_to_coi(self, swx, g_gname_map):
        gs = swx['G']

        no_angle_report = [key for key, value in gs.items() if ANGLE not in value.columns]
        if no_angle_report:
            raise ValueError('SWX存在发电机没有ANGLE字段！' + str(no_angle_report))

        # 所以实际上，能够进行到这一步，所有发电机的名字都应该是全的，否则不能计算COI
        g = np.array([gs[i][ANGLE] for i in g_gname_map])
        """g: angle: time * gen"""

        Tj = np.array(self.linked_dat.gen_info['Tj'])
        Tj = Tj / sum(Tj)

        # 对于swi不关注的发电机，默认为没有惯量，因此不计算在COI内
        Tj = np.array([Tj[i] for i in g_gname_map])
        coi = np.matmul(g.T, Tj.reshape(-1, 1)).reshape(1, -1)

        g = g - coi

        for i in range(len(self.linked_dat.gen_name)):
            gs[i][ANGLE] = g[i]

        swx['COI'] = {'COI': pd.DataFrame(coi)}
        return swx

    def ref_to_lag_gen(self, swx, g_gname_map):
        gs = swx['G']

        no_angle_report = [key for key, value in gs.items() if ANGLE not in value.columns]
        if no_angle_report:
            raise ValueError('SWX存在发电机没有ANGLE字段！' + str(no_angle_report))

        # 所以实际上，能够进行到这一步，所有发电机的名字都应该是全的，否则不能计算COI
        # 反驳楼上，有时候新能源机组不用计算功角。而且这不是计算COI的场合
        g = np.array([gs[i][ANGLE] for i in g_gname_map])
        """g: angle: time * gen"""

        Tj = np.array(self.linked_dat.gen_info['Tj'])
        Tj = Tj / sum(Tj)

        # 对于swi不关注的发电机，默认为没有惯量，因此不计算在COI内
        Tj = np.array([Tj[i] for i in g_gname_map])
        coi = np.matmul(g.T, Tj.reshape(-1, 1)).reshape(1, -1)

        lag = np.amin(g, axis=0)
        g = g - lag

        for i, j in enumerate(g_gname_map):
            gs[j][ANGLE] = g[i]

        swx['LAG'] = {'LAG': pd.DataFrame(lag)}
        swx['COI'] = {'COI': pd.DataFrame(coi)}
        return swx

    def get_label(self, swx, g_gname_map):
        # 在这里处理所有时序信息
        # 功角稳定标签。默认所有发电机都有，毕竟发电机不完整的话，不叫功角稳定
        g = swx['G']
        max_delta_gen_angle, max_delta_sys_angle, tu, tu360, eu = None, None, None, None, None
        if g:
            '''
            max_g_i, min_g_i = delta_ij, for all j
            '''
            # temp_g = pd.concat([g[i][ANGLE] for i in range(len(self.temp_dat.gen_name))], axis=1, ignore_index=True)
            # temp_g.columns = [i for i in range(len(self.temp_dat.gen_name))]
            #
            # max_delta_gen_angle = temp_g.abs().max(axis=0)
            #
            # max_g = temp_g.max(axis=1)
            # min_g = temp_g.min(axis=1)
            # max_delta_sys_angle = max_g.sub(min_g, axis=0).abs().max(axis=0)

            '''
            g_i = delta_i - coi? 先用绝对值试一试
            '''
            # temp_g = pd.concat([g[i][ANGLE] for i in range(len(self.temp_dat.gen_name))], axis=1, ignore_index=True)
            # temp_g.columns = [i for i in range(len(self.temp_dat.gen_name))]
            #
            # # 假设已经是滞后机组坐标系下的了，则直接输出机组最大角度即可
            # max_delta_gen_angle = temp_g.max(axis=0)
            # assert any(max_delta_gen_angle >= 0), 'get_label有问题，滞后坐标系啊，发电机的角度有小于0的'
            #
            # max_g = temp_g.max(axis=1)
            # min_g = temp_g.min(axis=1)
            # max_delta_sys_angle = max_g.sub(min_g, axis=0).max(axis=0)
            '''
            g_i = delta_i_coodinated.max, tu = first > 180
            实际上只要用了两个相减，坐标系就是没影响的。有影响的是tu
            '''
            g_gname_map = [i for i in g_gname_map if ANGLE in g[i].columns]  # 只计算有ANGLE的对象，也就是传统发电机，风机是没有的。

            temp_g = pd.concat([g[i][ANGLE] for i in g_gname_map],
                               axis=1, ignore_index=True)
            temp_g.columns = [i for i in g_gname_map]

            max_delta_gen_angle = temp_g.max(axis=0)
            # jiyu的tu
            tu = temp_g[temp_g > 180]
            tu = np.array([tu[x].first_valid_index() for x in tu.columns])
            tu = np.array([x if x is not None else -1 for x in tu])
            tu360 = temp_g[temp_g > 360]
            tu360 = np.array([tu360[x].first_valid_index() for x in tu360.columns])
            tu360 = np.array([x if x is not None else -1 for x in tu360])

            dangles = [(g[g_gname_map[i]]['DANGLE'][t] if t > -1 else 0) for i, t in enumerate(tu)]
            eu = [dangle * np.pi / (self.get_sim_step() * 0.02 * 180) for dangle in dangles]
            dangles = [(g[g_gname_map[i]]['DANGLE'][t] if t > -1 else 0) for i, t in enumerate(tu360)]
            eu360 = [dangle * np.pi / (self.get_sim_step() * 0.02 * 180) for dangle in dangles]
            # assert any(max_delta_gen_angle >= 0), 'get_label有问题，滞后坐标系啊，发电机的角度有小于0的'

            max_g = temp_g.max(axis=1)
            min_g = temp_g.min(axis=1)
            max_delta_sys_angle = max_g.sub(min_g, axis=0).max(axis=0)


        # 电压稳定标签
        b = swx['B']
        min_bus_voltage, max_bus_voltage = None, None
        if b:
            temp_b = pd.concat([bb[VOLTAGE] for bb in b.values()], axis=1, ignore_index=True)
            temp_b.columns = b.keys()
            min_bus_voltage = temp_b.min(axis=0)
            max_bus_voltage = temp_b.max(axis=0)

        return {'G': [max_delta_gen_angle, max_delta_sys_angle, tu, tu360, eu, eu360],
                'B': [min_bus_voltage, max_bus_voltage]}

    def swx2pf_section(self, swx_struct):
        """
        最终妥协成跟pfo一样的格式。
        @param temp_dat:
        @param swx_struct:
        @return:
        """
        pfs = {t: {} for t in self.time_index}

        for t in self.time_index:
            df_b = pd.DataFrame([swx_struct['B'][key].loc[t]
                                 for key in swx_struct['B'].keys()], index=swx_struct['B'].keys())
            df_g = pd.DataFrame([swx_struct['G'][key].loc[t]
                                 for key in swx_struct['G'].keys()], index=swx_struct['G'].keys())
            df_g.index = [self.linked_dat.gen_bus_order[i] for i in df_g.index]
            if ANGLE in df_g.columns:  # todo 检查是否有更改这一行，应该要有的
                df_g.rename(columns={ANGLE: ANGLE + '_g'}, inplace=True)
            df = pd.merge(df_b, df_g, how='outer', left_index=True, right_index=True)
            df.fillna(0, inplace=True)  # todo 有什么必要？
            df.sort_index(inplace=True)
            pfs[t] = df

        return pfs

    def _parse_block(self, block):
        """

        @param block:
        @return: data1保留0-，data2为0+
        """
        info_line = block[0][(block[0].index(' * ') + 3):].split('\"')
        info_type = info_line[0]  # 发电机、母线、线路
        if '风电机组' == info_type:
            """
            风电机组块结构：
                            * 风电机组"bus32    100.0  "输出数据列表
                 =======	====================	====================	====================
                  时间   	机组有功功率    (MW)	机组无功功率  (Mvar)	发电机角速度    (pu)
                   0.0	         0.7222     	         0.2979     	         1.2000   
                   ...  
            """
            data = pd.DataFrame(block[3:])[0].str.split('\t', expand=True)
        else:
            """
            其他块结构：
                * 节点"bus1     100.0"输出数据列表
                 =======================================================
                  时间   	 正序电压 	 正序角度 	 有功负荷 	 无功负荷 
                               (PU)   	   (度)   	   (MW)   	  (Mvar)  
                   0.0	    1.0254	    1.5467	    0.0000	    0.0000
                   ...
            """
            data = pd.DataFrame(block[4:])[0].str.split('\t', expand=True)

        # 解析元信息
        if '发电机' == info_type or '风电机组' == info_type:  # 还差光伏的
            t = 'G'
            name, idx = self._parse_gen(info_line[1])
        elif '节点' == info_type:
            t = 'B'
            name, idx = self._parse_bus(info_line[1])
        elif '线路' == info_type:
            t = 'L'
            name, idx = self._parse_2bus(info_line[1])
        elif '串联补偿' == info_type:
            t = 'R'
            name, idx = self._parse_2bus(info_line[1])
        elif '直流' == info_type:
            t = 'D'
            name, idx = self._parse_2bus(info_line[1])
        else:
            raise ValueError('info_type not in  {发电机，节点，线路，串联补偿，直流} ！')

        data.columns = ['STEP'] + self.swx_struct[t][name]
        try:
            data = data.astype('float')
        except ValueError:
            print('gg. 已知问题：仿真中断导致数据不全')  # 已知问题：仿真中断导致数据不全
        # 功率处理为标幺值
        for col in data.columns:
            if col in [GEN_Q, GEN_P, LOAD_Q, LOAD_P]:  # 暂时的，还有问题。todo
                data[col] = data[col].div(self.linked_dat.mva_base)

        # 数据预处理,分割
        if self.sim_step_mask is None:
            # 目的是去除重复的时间步
            self.sim_step_mask = (data['STEP'] - data['STEP'].shift(1)).astype('bool')
            # 用于提取需要潮流的地方，与sim_step_mask不互补之处在于，第一个时间片是丢弃的，有可能没达到稳态，转而取t0-
            self.pf_step_mask = ~self.sim_step_mask
            repeat_step = [i for i in range(len(self.pf_step_mask)) if self.pf_step_mask[i]]
            self.pf_step_mask[repeat_step[0]] = False
            self.pf_step_mask[repeat_step[1] - 2] = True  # 为什么不取真正的t0-？ 这样后面的时间片不好取

        # 需要处理发电机角度
        if t == 'G' and 'ANGLE' in data.columns:
            data['DANGLE'] = (data['ANGLE'] - data['ANGLE'].shift(1))
            data['DANGLE'][0] = 0
            assert len(data['DANGLE'][data['DANGLE'] == 180]) == 0, '出现时间步加速度恰好为180，检查是否有加速度超过180的！'
            data['DANGLE'][data['DANGLE'] > 180] = data['DANGLE'][data['DANGLE'] > 180] - 360
            data['DANGLE'][data['DANGLE'] <-180] = data['DANGLE'][data['DANGLE'] <-180] + 360
            data['ANGLE'] = data['DANGLE'].cumsum(axis=0) + data['ANGLE'][0]

        # 分割出t0+-的时刻
        sim_data, pf_data = data[self.sim_step_mask].copy(), data[self.pf_step_mask].copy()
        sim_data.set_index('STEP', inplace=True)
        pf_data.set_index('STEP', inplace=True)
        # self.fault_step, self.clear_step = data2.index[1], data2.index[2]

        return t, name, idx, sim_data, pf_data  # 舍去0时刻

    def get_sim_step(self):
        return self.lines[self.cff].get_value('DT')

    def get_sim_len(self):
        return self.lines[self.cff].get_value('ENDT')

    def save_to_file(self, path, temp_fault: list=None):
        """
        想写入哪里，直接写完整路径即可。会直接递归地创建路径。
        todo 未来与dat的方法合并
        :param temp_fault: 字符串列表
        :param path: 有没有以.dat结尾都可以。
        :param text_prefix: 正文的开头，用来记录一些信息的。
        :return:
        """
        if path[-4:].lower() != '.swi':
            path += '.swi'
        os.makedirs(os.path.dirname(path), exist_ok=True)
        file = open(path, 'w')
        if temp_fault:
            for i, card in enumerate(self.lines):
                if isinstance(card, SwiFF):
                    break
            file.write('\n'.join([x if type(x) is str else str(x) for x in self.lines[:i]]) + '\n')
            file.write('\n'.join(temp_fault))
            file.write('\n'.join([x if type(x) is str else str(x) for x in self.lines[i:]]) + '\n')
        else:
            file.write(str(self))
        file.close()

    @staticmethod
    def build_from(path, dat=None):
        """
        从文件夹或者文件中新建实例,如果是从文件夹，只会找文件夹中第一个出现的。
        :param path:
        :return:
        """
        if os.path.isfile(path):
            if '.swi' in path.lower():
                if dat is None:
                    dat = DAT.build_from(path)
                lines = open(path, 'rb').readlines()
                return SWI.build_from_lines(lines, dat)
        elif os.path.isdir(path):
            for f in os.listdir(path):
                if '.swi' in f.lower():
                    if dat is None:
                        dat = DAT.build_from(path)
                    lines = open(path + '/' + f, 'rb').readlines()
                    return SWI.build_from_lines(lines, dat)
        raise ValueError('cannot find .swi file in path!')

    @staticmethod
    def std_swi(folder_path):
        for f in os.listdir(folder_path):
            if '.swi' in f.lower():
                lines = open(folder_path + '/' + f, 'rb').readlines()
                lines = [bpa_card_line(line) for line in lines]
                f = f.replace('.SWI','_std.SWI')
                f = f.replace('.swi', '_std.swi')
                pathn = folder_path + '\\' + f
                with open(pathn,'w') as filen:
                    for linen in lines:
                        linen = str(linen, 'gbk')+'\n'
                        filen.write(linen)
                print('std=====>',pathn)
                filen.close()
                return pathn

    @staticmethod
    def build_from_lines(ll: List[str], dat):
        ll = [bpa_card_line(line) for line in ll]

        lines = []
        can = []
        ccm = []
        cop = []

        position = 0
        # 唯一的卡
        cf0, cf1, cff, cpara_file, c90, c99 = [], [], [], [], [], []
        cm_only1 = {'F0': cf0, 'F1': cf1, 'FF': cff, 'PARA_FILE': cpara_file}
        op_only1 = {'90': c90, '99': c99}

        for i, l in enumerate(ll):
            if l == b'\n':
                lines.append('\n')
                continue

            c = _to_card(l, A.card_types)
            if c:
                lines.append(c)
                can.append(i)
                continue

            if l[:2] == b'90':
                position = 2

            if position < 2:
                c = _to_card(l, CM.card_types)
                if c:
                    position = 1
                    lines.append(c)
                    ccm.append(i)

                    if c.type in cm_only1:
                        cm_only1[c.type].append(i)

                    continue

            else:
                c = _to_card(l, O.card_types)
                if c:
                    position = 2
                    lines.append(c)
                    cop.append(i)

                    if c.type in op_only1:
                        op_only1[c.type].append(i)
                    continue

            print('unknown bline! transform to Annotation Card: ', l)
            lines.append(_to_card(b'.' + l, A.card_types))

        for c in [cf0, cf1, cff, cpara_file, c90, c99]:
            if len(c) > 1:
                raise ValueError('has more than 1 card!')
        cf0 = cf0[0] if cf0 else None
        cf1 = cf1[0] if cf1 else None
        cff = cff[0] if cff else None
        cpara_file = cpara_file[0] if cpara_file else None
        c90 = c90[0] if c90 else None
        c99 = c99[0] if c99 else None

        return SWI(lines, can, ccm, cop, cf0, cf1, cff, cpara_file, c90, c99, dat)

    def _parse_bus(self, line):
        """不用uid的原因是，这里的base是F5.0"""
        bline = bytes(line, encoding='gbk') if type(line) is not bytes else line
        assert len(bline) == 14
        name = bline[:8].decode('gbk', errors='ignore') + SWI.base_writer(SWI.base_reader(bline[9:].decode('gbk', errors='ignore')))
        return name, self.linked_dat.bus_order[name]

    def _parse_gen(self, line):
        """不用uid的原因是，这里的base是F5.0"""
        bline = bytes(line, encoding='gbk')
        # assert len(bline) == 15  # 也有可能是16个，如风电机组
        name = bline[:8].decode('gbk', errors='ignore') \
               + SWI.base_writer(SWI.base_reader(bline[9:15].decode('gbk', errors='ignore'))) \
               + bline[-1:].decode('gbk', errors='ignore')
        return name, self.linked_dat.gen_order[name]

    def _parse_2bus(self, line):
        """不用uid的原因是，这里的base是F5.0"""
        bline = bytes(line, encoding='gbk')
        assert len(bline) == 30
        name = self._parse_bus(bline[:14])[0] + self._parse_bus(bline[15:-1])[0] + line[-1]
        return name, self.linked_dat.branch_order[name]

