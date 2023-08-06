# -*- coding:utf-8 -*-
"""
# Name:         dlgxa: utils
# Author:       MilkyDesk
# Date:         2022/3/10 16:17
# Description:
#   工具函数集合
# 1. 调潮流初始条件
# 2. 保证拓扑的情况下断线
"""

# ------------------------- params --------------------------


# ------------------------- params --------------------------
from typing import Union

from scipy.stats import norm
from ..base.bpa_uid import GEN_P, LOAD_P, LOAD_Q, VMAX, GEN_Q, ANGLE
from ..dat.bpa_dat import DAT
import numpy as np
from numpy import random
import networkx as nx


# LHS要用到的正态分布反函数
from ..dat.bpa_dat_data import DatBS, DatBV, DatBQ, DatL
from ..organize.file_organize import DefaultOrganizer


class _DATGenerator:

    name_pqpqvt = ['LOAD_P', 'LOAD_Q', 'GEN_P', 'GEN_Q', 'VOLTAGE', 'VMAX']
    idx_pl, idx_pg, idx_ql, idx_qg, idx_v, idx_t = [DatBV.field_index[LOAD_P], DatBV.field_index[GEN_P],
                                                    DatBV.field_index[LOAD_Q], DatBV.field_index[GEN_Q],
                                                    DatBV.field_index[VMAX], DatBS.field_index[ANGLE]]

    def _check_pqpqvt(self, pqpqvt):
        """
        根据dat的节点属性检查pqpqvt是否合法，不合法输出警告。
        :param pqpqvt:
        :return:
        """
        # 发电机、被允许的
        allowed = np.zeros([6, len(self.dat.bus)], dtype=np.bool_)
        # 发电机PV
        for i in self.dat.gen_bus_order:
            allowed[2, i] = True
            allowed[3, i] = True
        # 负荷PQ, 不新增负荷节点
        # 平衡机PQ
        for i, bus in enumerate(self.dat.bus):
            if bus.values[self.idx_pl] != 0 or bus.values[self.idx_ql] != 0:
                allowed[0, i] = True
                allowed[1, i] = True
            if isinstance(bus, DatBS):
                allowed[5, i] = True
                allowed[2, i] = False  # 平衡机P不可控

        conflict = []
        for i in range(6):
            for j in range(len(allowed[0])):
                if pqpqvt[i, j] and not allowed[i, j]:
                    conflict.append([self.name_pqpqvt[i], j])
                    pqpqvt[i, j] = False
        if len(conflict) > 0:
            # print(conflict)
            raise Warning(f'采样设置有误！{conflict}')
        return pqpqvt

    def set_sample_to_dat(self, sample, dat: DAT):
        for i in range(self.n_bus):
            for j in range(6):
                if self.pqpqvt[j, i]:
                    dat.bus[i].set_value(self.name_pqpqvt[j], sample[j, i], ignore_error=True)
        return dat

    def default_base(self, dat: DAT):
        base = np.zeros([6, len(dat.bus)])  # pl, ql, pg, qg, v, theta
        for i, bus in enumerate(dat.bus):
            base[0, i] = bus.values[self.idx_pl]
            base[1, i] = bus.values[self.idx_ql]
            base[2, i] = bus.values[self.idx_pg] if isinstance(bus, DatBQ) else 0
            base[3, i] = bus.values[self.idx_qg] if isinstance(bus, DatBQ) else 0
            base[4, i] = bus.values[self.idx_v] if isinstance(bus, (DatBQ, DatBS)) else 0
            base[5, i] = bus.values[self.idx_t] if isinstance(bus, DatBS) else 0
        return base


class GridGenerator(_DATGenerator):
    """
    功能：网格抽样。(与拓扑无关)
    初始化，采样，生成。
    注意：这里的GridGenerator.sample(n_sample)方法，是会对每个随机维度生成n_sample个采样值，实际上就是n_sample**d个样本
    """
    def __init__(self, dat: DAT, pqpqvt: np.ndarray,
                 maxx: Union[float, np.ndarray] = 3, minx: np.ndarray = None):
        self.dat = dat

        self.n_bus = len(dat.bus)
        self.n_gen = len(dat.gen)

        if minx is None:
            self.minx = 0

        if isinstance(maxx, float):
            self.maxx = self.default_base(dat) * maxx
        else:  # maxx: ndarray 表示是绝对值
            self.maxx = maxx

        # 检查和输出
        self.pqpqvt = self._check_pqpqvt(pqpqvt)

        self.mean[self.pqpqvt == False] = 0
        self.std[self.pqpqvt == False] = 0

    def sample(self, n_sample):
        """采样得到pqpqvt格式的样本。(划掉。出于效率考虑目前并不是，因此需要采用自己的set方法
        由于网格采样结果与总采样数量有关，所以需要一次性输出所有采样结果"""
        x = []
        for i in range(len(self.pqpqvt)):
            for j in range(6):
                if self.pqpqvt[i][j]:
                    x.append(np.linspace(self.minx[i][j], self.maxx[i][j], n_sample))
        xs = np.meshgrid(*x)
        xs = [x.reshape(-1) for x in xs]
        xs = np.array(xs)
        return xs.T

    def set_sample_to_dat(self, sample, dat: DAT):
        count = 0
        for i in range(self.n_bus):
            for j in range(6):
                if self.pqpqvt[j, i]:
                    dat.bus[i].set_value(self.name_pqpqvt[j], sample[count], ignore_error=True)
                    count += 1
        assert count == len(sample)
        return dat


class LHSGenerator(_DATGenerator):
    """
    功能：拉丁超立方抽样。(与拓扑无关)
    初始化，采样，生成。
    """

    def __init__(self, dat: DAT, pqpqvt: np.ndarray, std: Union[float, np.ndarray]=0.1, mean=None,
                 truncate=1.0, distr='uniform'):
        self.dat = dat
        self.distr = distr
        self.truncate = truncate

        self.n_bus = len(dat.bus)
        self.n_gen = len(dat.gen)

        if mean is None:
            self.mean = self.default_base(dat)

        if isinstance(std, float) and std <= 1:
            self.std = self.mean * std
        else:  # std > 1 or std: ndarray 表示是绝对值
            self.std = std

        # 检查和输出
        self.pqpqvt = self._check_pqpqvt(pqpqvt)

        self.mean[self.pqpqvt == False] = 0
        self.std[self.pqpqvt == False] = 0

    def sample(self, n_sample):
        """采样得到pqpqvt格式的样本"""
        samples = self._sample(n_sample, self.mean, self.std, self.truncate)
        return [[str(i).zfill(3), sample] for i, sample in enumerate(samples)]

    def _sample(self, n_sample, mean, std, truncate=1.0):
        """
        带有截断正态分布的拉丁超立方采样
        :param n_sample:
        :param mean:
        :param std:
        :param truncate:
        :param distr: ['uniform', 'normal', any_func] 提供分布
        :return: shape: (n_sample, mean&std.shape)
        """
        # 1. 随机数生成，都是按照uniform来生成的
        samples = random.uniform(0, truncate / n_sample, size=mean.shape+(n_sample,))\
                  + np.linspace((1-truncate)/2, (1+truncate)/2, n_sample, False)
        shape = samples.shape
        samples = samples.reshape(-1, n_sample)
        for i in range(len(samples)):
            np.random.shuffle(samples[i])
        axis = np.arange(len(shape)) - 1

        # 2. 分布反变换。
        if self.distr == 'uniform':
            samples = 2 * (samples - 0.5)
        elif self.distr == 'normal':
            samples = norm(0, 1).ppf(samples)
        else:
            samples = self.distr(samples)

        samples = samples.reshape(shape).transpose(*axis)
        return mean[np.newaxis] + std[np.newaxis] * samples



class LHSGradGenerator(LHSGenerator):
    """用于对采样得到的样本，按随机变量数量附加微增量，以获取"""
    def __init__(self, *p, **q):
        super().__init__(*p, **q)
        xs, ys = self.pqpqvt.nonzero()
        self.random_variance = np.array([[x, y] for x, y in zip(xs, ys)])


    def sample(self, n_sample):
        """采样得到pqpqvt格式的样本"""
        samples = self.sampler(n_sample, self.mean, self.std, self.truncate)
        samples_plus = [[str(i).zfill(3) + '00', sample] for i, sample in enumerate(samples)]
        for j, var in enumerate(self.random_variance):
            sample = samples.copy()
            sample[:, var[0], var[1]] += 1  # 增量步长
            samples_plus += [[str(i).zfill(3) + str(j+1).zfill(2), sample] for i, sample in enumerate(sample)]

        return samples_plus



class TopoDataGenerator:

    def __init__(self, dat: Union[DAT, str], target_root_path: str, file_organizer=None, lsd=None,
                 generator=None, data_filter=lambda x: True,
                 topo_filter=None):
        """
        示例：
        # 样本生成步骤
        # 指定路径
        dat_path = input('参考dat文件绝对路径')
        lsd_path = input('参考lsd文件绝对路径')
        target_root_path = input('数据的输出根路径（不需要事先新建）')
        dat = DAT.build_from(dat_path)

        # 指定随机数生成器
        pqpqvt = np.zeros([6, 39], dtype=np.bool_)
        pqpqvt[2, 31:33] = True
        generator = LHSGenerator(dat, pqpqvt, std=0.3, truncate=0.9973)  # 3sigma

        # 指定数据过滤器（可选）

        # 指定拓扑过滤器（可选）

        # 指定拓扑生成器
        tg = TopoDataGenerator(dat=dat, target_root_path=target_root_path,
                               generator=generator, data_filter=lambda x: True,
                               file_organizer=None,
                               lsd=LSD(lsd_path),  # 需要随方式生成lsd
                               topo_filter=IslandFilter(dat))
        tg.gen(depth=0, target_depth=2, n_samples=20, dat_text_title='info的信息为同个拓扑下不同bus32、bus33节点处理的采样序号')


        :param dat:
        :param target_root_path: 新项目的根目录
        :param file_organizer: 组织整个项目的文件结构，各个方式的命名规则
        :param gen_lsd: 是否生成方式匹配的lsd，默认是
        :param generator: 潮流定解条件采样器
        :param data_filter: 判断指定方式是否生成
        :param topo_filter: 拓扑过滤器，默认用孤岛的那个
        """
        # 文件设置
        # 生成器和过滤器
        #其他？
        self.dat = dat if isinstance(dat, DAT) else DAT.build_from(dat)
        self.file_organizer = file_organizer if file_organizer else DefaultOrganizer(target_root_path)
        self.generator = generator
        self.data_filter = data_filter if data_filter else (lambda x: True)
        self.topo_filter = topo_filter if topo_filter else IslandFilter(dat=dat)
        self.lsd = lsd
        print('【注意】：TopoDataGenerator 目前断线只会从L卡定义的线路中选。')

    def gen(self, depth, target_depth, n_samples, prefix=[], dat_text_title=None, candidates=None):
        """
        dfs采样。todo 还有一种是 生成所有的候选拓扑，然后逐个生成样本。
        设初始化的dat的深度为depth，按断线采样拓扑，最大断线量为target_depth - depth（包含）,比如输入（0，2）则采集N-0, N-1, N-2的拓扑。
        每个拓扑采样n_sample个。

        D_sample
        for filter(D_sample)
        for top:
            if top_filter:
                next_top()

        dat第一行：详细信息

        :param depth: 开始拓扑深度
        :param target_depth: 结束拓扑深度（包含）
        :param n_samples:
        :param prefix:
        :param dat_text_title: 写在所有生成的dat最前面一行的说明性文本，比如“基准文件来自...命名规则为” 对info的解释、
        :param candidates: 候选断线列表
        :return:
        """
        # 1. 采样（默认了调用==至少需要采这个）
        samples = self.generator.sample(n_samples)
        for info, sample in iter(samples):
            # 2. 过滤并输出文件
            if self.data_filter(sample):
                operation_name = self.file_organizer.get_op_name(info=info, pre_cut_line_list=prefix)
                self.generator.set_sample_to_dat(sample, self.dat)
                self.dat.save_to_file(path=self.file_organizer.get_dat_path(op_name=operation_name),
                                      text_prefix=f'. operation_name: {operation_name}, info: {info}\n' +
                                                  (f'.{dat_text_title}\n' if dat_text_title else ''))
                if self.lsd:
                    self.lsd.write(path=self.file_organizer.root_path + operation_name, op_name=operation_name,
                                   ban_branch=prefix)

            print(depth, '\t', operation_name)

        # 3. 下一层拓扑搜索
        if depth >= target_depth:
            return
        if candidates is None:
            candidates = [order for bname, order in self.dat.branch_order.items()
                          if isinstance(self.dat.branch_indexs[bname][0], DatL)
                          and not self.dat.branch_indexs[bname][0].is_commented]


        for i, b in enumerate(candidates):
            # 4. 去掉线路,检查去掉线路后的拓扑是否符合要求（是否是孤岛），是的搜索下一层
            if self.topo_filter.check(branch_order=b):  # nx.number_connected_components(graph) == 1
                self.gen(depth=depth+1, target_depth=target_depth, n_samples=n_samples,
                         candidates=candidates[(i+1):], prefix=prefix + [str(b)], dat_text_title=dat_text_title)
            # 6. 接回线路
            self.topo_filter.restore_line(branch_order=b)


class IslandFilter:
    """
    产生新拓扑的对象。
    过滤规则是断线后不产生孤岛
    """
    def __init__(self, dat: DAT):
        self.dat = dat
        self.graph = nx.Graph([dat.branch_bus_order[b] for b in dat.branch_order.values()])
        print('注意：使用这个的前提是系统没有直流线路。目前只把L和E线路认为是可能断开的')

    def check(self, branch_order: int):
        """
        这里check操作和实际改变拓扑的操作是高度耦合的：检查拓扑是否符合要求的同时，已经改变了拓扑了，没必要再变回去。
        但是改变之后无论是否符合结果，都需要手动复原。
        这个逻辑其实很像with这种上下文管理器，随着操作的生存期，有__enter__和__exit__方法。但是目前似乎只有对象的上下文管理，没有方法的上下文管理。
        :param branch_order:
        :return:
        """
        self.cut_line(branch_order)
        return nx.is_connected(self.graph)

    def cut_line(self, branch_order):
        self.graph.remove_edge(*(self.dat.branch_bus_order[branch_order]))
        for card in self.dat.branch_indexs[self.dat.branch_name[branch_order]]:
            card.commented()

    def restore_line(self, branch_order):
        """复原被断开的线路卡（们）。操作的是单回线路（uid），不是连接两个节点的所有线路"""
        self.graph.add_edge(*(self.dat.branch_bus_order[branch_order]))
        for card in self.dat.branch_indexs[self.dat.branch_name[branch_order]]:
            card.uncommented()


class SpecificBranchFilter(IslandFilter):
    def __init__(self, dat, specific_branch, ban_branch=[]):
        super().__init__(dat)
        self.specific_branch = specific_branch if isinstance(specific_branch, list) else [specific_branch]
        self.ban_branch = ban_branch if isinstance(ban_branch, list) else [ban_branch]

    def check(self, branch_order: int):
        not_island = super().check(branch_order)
        return (branch_order in self.specific_branch) and (branch_order not in self.ban_branch) and not_island

