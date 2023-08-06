# -*- coding:utf-8 -*-
"""
# Name:         dlgxa: n_sample-012randomPQ
# Author:       MilkyDesk
# Date:         2022/3/10 16:28
# Description:
#   生成N-0/1/2不同拓扑下的随机出力
1. 超参数配置方法
2. for 拓扑:
       for 出力: 生成新的dat并保存到指定文件夹
"""

# ------------------------- params --------------------------

# ------------------------- params --------------------------
from ..utils.utils import GridGenerator, LSDWriter, topo_generator
from ..lsd.nrscp_lsd import LSD
import numpy as np
from ..dat.bpa_dat import DAT
import networkx as nx
import os

pqpqvt = np.zeros([6, 39], dtype=np.bool_)
pqpqvt[2, 30:38] = True
dat_path = input('dat文件绝对路径')
lsd_path = input('lsd文件绝对路径')
output_path = input('数据的输出路径（不需要事先新建）')
dat = DAT.build_from(dat_path)
# generator = LHSGenerator(dat, pqpqvt, 0.4, truncate=0.9973)  # 3sigma
# generator = LHSGenerator(dat, pqpqvt, 0.1, truncate=1)
maxx = 3  # 风电场装机容量取基准发电的3倍
generator = GridGenerator(dat, pqpqvt, maxx, minx=0)
lsd_writer = LSDWriter(lsd_path)
# topo_generator(0, 3, dat, output_path, 1, generator, make0=False, lsd_writer=lsd_writer)  # 生成N，N-1，N-2拓扑的样本
topo_generator(0, -1, dat, output_path, 1, generator, make0=True, lsd_writer=lsd_writer)  # 生成原拓扑的样本
# topo_generator(2, -1, dat, output_path, 20, generator, prefix=['1', '26'])  # 生成指定拓扑树下的案例
# todo 要生成单个拓扑下的很多很多个样本，至少1000.

