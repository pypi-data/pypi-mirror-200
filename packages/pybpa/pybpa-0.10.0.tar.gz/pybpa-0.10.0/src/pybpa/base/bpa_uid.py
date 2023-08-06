# -*- coding:utf-8 -*-
"""
# Name:         transient_stability: bpa_uid
# Author:       MilkyDesk
# Date:         2021/7/6 11:37
# Description:
#   bpa中card类对象的唯一标识符
#   每个card类都需要继承
"""
import numpy as np

from .bpa_base import _Card, _Field, CARD_TYPE

# ------------------------- params --------------------------
BUS_NAME_STR = 'NAME'
BUS_BASE_STR = 'BASE'
BUS_NAME1_STR = 'NAME1'
BUS_BASE1_STR = 'BASE1'
BUS_NAME2_STR = 'NAME2'
BUS_BASE2_STR = 'BASE2'
GEN_ID = 'ID'
CKT_ID = 'CKT ID'  # 并联线路
SEC_ID = 'SECTION'  # 串联线路
ANGLE = 'ANGLE'  # 节点或发电机角度
VMAX = 'VMAX'  # 节点电压上限，或发电机节点的安排电压
VOLTAGE = 'VOLTAGE'  # 电压幅值
ORDER = 'ORDER'  # 特指dat中的bus_order, line_order
GEN_P_MAX = 'GEN_P_MAX'
GEN_P = 'GEN_P'
GEN_Q = 'QSCHED'  # 也有可能是GEN_Q_MAX
GEN_Q_MAX = 'GEN_Q_MAX'
GEN_Q_MIN = 'GEN_Q_MIN'
LOAD_P = 'LOAD_P'
LOAD_Q = 'LOAD_Q'

# ------------------------- params --------------------------
class BNameFormatter:
    name_f = _Field(1, 8, '', 'A8')
    base_f = _Field(1, 4, '', 'F4.0')

    @staticmethod
    def get_name(name: str, base: float):
        return BNameFormatter.name_f.write(name.strip().ljust(8)) + BNameFormatter.base_f.write(base)

    @staticmethod
    def parse_name(name: str):
        assert len(name) == 14
        return BNameFormatter.name_f.read(name[:-4]), BNameFormatter.base_f.read(name[-4:])

class LNameFormatter:

    @staticmethod
    def get_name(name1: str, base1: float, name2: str, base2: float):
        return BNameFormatter.get_name(name1, base1) + BNameFormatter.get_name(name2, base2)

    @staticmethod
    def parse_name(name: str):
        s = bytes(name, encoding='gbk')
        assert len(s) == 29
        n1, b1 = BNameFormatter.parse_name(s[:14].decode('gbk', errors='ignore'))
        n2, b2 = BNameFormatter.parse_name(s[14:28].decode('gbk', errors='ignore'))
        ckt = s[28:]
        return n1, b1, n2, b2, ckt

    @staticmethod
    def parse_B(name: str, ckt=False):
        if ckt:
            return name[:14], name[14:28], name[28:]
        else:
            return name[:14], name[14:28]

class GNameFormatter:

    @staticmethod
    def get_name(name: str, base: float, id: str):
        return BNameFormatter.get_name(name, base) + id

    @staticmethod
    def parse_name(name: str):
        assert len(name) == 15
        n, b = BNameFormatter.parse_name(name[:-1])
        id = name[-1:]
        return n, b, id

    @staticmethod
    def parse_B(name, id=False):
        if id:
            return name[:-1], name[-1:]
        else:
            return name[:-1]


class _TypeNameUid(_Card):
    """
    没有节点名称的卡，一般适用于每个文件特有一张的卡，比如FF，90，或者控制卡等。
    """
    def __init__(self, bline):
        super(_TypeNameUid, self).__init__(bline)
        self.name = self.fields[0].default


class _OneNameUid(_Card):
    """
    只有一个节点名称的卡，一般适用于节点、发电机及相应的模型
    """
    def __init__(self, bline):
        super(_OneNameUid, self).__init__(bline)
        self.order = None
        # try 是对当前各种父类fields编写不完整的补丁
        try:
            n, b = self.field_index[BUS_NAME_STR], self.field_index[BUS_BASE_STR]
            self.name = BNameFormatter.get_name(self.values[n], self.values[b])
        except:
            self.name = self.fields[0].default
            print('_OneNameUid cannot parse name: ', bline.decode('gbk', errors='ignore'))


class _TwoNameUid(_Card):
    """
    有两个节点名称的卡，一般适用于线路、发电机及相应的模型
    """
    def __init__(self, bline):
        super(_TwoNameUid, self).__init__(bline)
        self.order = None
        self.order1, self.order2 = None, None
        # try 是对当前各种父类fields编写不完整的补丁
        try:
            n1, b1 = self.field_index[BUS_NAME1_STR], self.field_index[BUS_BASE1_STR]
            n2, b2 = self.field_index[BUS_NAME2_STR], self.field_index[BUS_BASE2_STR]

            # 对所有双名卡规定顺序, 规则：要小的在前面. 处理：直接value换位，避免后续影响.这里是无论填卡顺序，只改uid，不改卡内容
            if self.values[n1] > self.values[n2] or (self.values[n1] == self.values[n2] and self.values[b1] > self.values[b2]):
                n1, b1, n2, b2 = n2, b2, n1, b1

            self.name1 = BNameFormatter.get_name(self.values[n1], self.values[b1])
            self.name2 = BNameFormatter.get_name(self.values[n2], self.values[b2])
            self.name = LNameFormatter.get_name(self.values[n1], self.values[b1], self.values[n2], self.values[b2])
        except:
            print('line cannot parse name: ', bline.decode('gbk', errors='ignore'))
            raise ValueError('有人需要有两个名字，但是他没有名字。')


class _GenUid(_Card):
    def __init__(self, bline):
        super(_GenUid, self).__init__(bline)
        self.order = None
        self.order1 = None
        # try 是对当前各种父类fields编写不完整的补丁
        try:
            n, b, id = self.field_index[BUS_NAME_STR], self.field_index[BUS_BASE_STR], self.field_index[GEN_ID]
            self.name = GNameFormatter.get_name(self.values[n], self.values[b], self.values[id])
            self.name1 = GNameFormatter.parse_B(self.name)
        except:
            self.name = self.fields[0].default


class _LineCard(_TwoNameUid):
    def get_y(self):
        """
        返回自身对导纳矩阵的影响(L,E,T,TP),顺序y11, y12, y21, y22
        特别的卡（L+，LD，LM，R，RZ）需要自己实现，否则会报错
        线路标幺值是折算到dat首端节点电压下的；变压器是折算到铭牌电压下的，容量基值也是系统基值（dat中的T卡容量仅做过负荷校验用）；
        Ref: 李汉香,刘丽平. 具有非标准变比变压器的参数计算[J]. 电网技术, 1999, (12): 39-42.
        BPA采用的不是常见的单理想变压器的Pi型等值电路，而是双理想变压器的Pi型等值电路
        """
        # 计算自导纳。兼容不对称卡E，所以才不用L作为条件
        # todo 分开卡计算吧
        if self.get_value(CARD_TYPE) in ['L ', 'E ']:
            y = 1 / (self.get_value('R') + 1j * self.get_value('X'))
            if self.get_value(CARD_TYPE) == 'E ':  # 不对称线路。对于不对称线路，Gi,Bi是各侧对地导纳G/2,B/2 (潮流手册4.4.1末)
                y11 = (self.get_value('G1') + 1j * self.get_value('B1'))
                y22 = (self.get_value('G2') + 1j * self.get_value('B2'))
            elif self.get_value(CARD_TYPE) == 'L ':  # 对称线路，以及变压器。
                y11 = (self.get_value('G') + 1j * self.get_value('B'))
                y22 = y11
            return y11 + y, -y, -y, y22 + y

        # 计算互导纳（和变压器自导纳）兼容变压器T,TP
        if self.get_value(CARD_TYPE) == 'T ':
            # BPA的变压器模型: ---k1:1---(R+jX)---1:k2---
            k1 = self.get_value('TP1') / self.get_value(BUS_BASE1_STR)
            k2 = self.get_value('TP2') / self.get_value(BUS_BASE2_STR)
            y = 1 / (self.get_value('R') + 1j * self.get_value('X'))
            y12 = y / (k1 * k2)
            y21 = y12
            y11 = (k2 - k1) / k1 * y12
            y22 = (k1 - k2) / k2 * y12
            # todo 励磁支路 G+jB 归算到y11还是y22？
            # 2023年3月14日根据BPA仿真，发现励磁支路不是简单接在任一端节点成为对地支路的，很有可能同变压器模型，接在标准边的中性电压点中间。
        elif self.get_value(CARD_TYPE) == 'TP':
            # 移相器公式：现代电力系统分析，王锡凡P14(1-36~1-39) 图1-4(a)模型
            k = 1 / np.exp(-1j * np.pi / 180 * self.get_value('PHASE SHIFT DEG'))
            y = 1 / (self.get_value('R') + 1j * self.get_value('X'))
            y12 = y / k
            y21 = y / k.conjugate()
            y11 = y
            y22 = y / (abs(1) ** 2)

        # 励磁支路存疑，不知道加在哪边。BPA是有计入这个项目的，但是实际参数相对很小很小。
        # todo 2023年3月14日根据BPA仿真，发现励磁支路不是简单接在任一端节点成为对地支路的，很有可能同变压器模型，接在标准边的中性电压点中间。
        # 于是做了这个Pi型假设，分两半接在变压器两侧，大概有1%的误差。
        y10 = (self.get_value('G') + 1j * self.get_value('B')) / 2
        y20 = y10

        return y10 + y11 + y12, -y12, -y21, y20 + y22 + y21