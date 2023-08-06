# -*- coding: utf-8 -*-#
import datetime
import os
import random
import shutil
import sys
from argparse import ArgumentParser
from multiprocessing import Pool, RLock, Manager
import win32gui, win32con, win32api

import tempfile
import numpy as np
import subprocess
import io
# from environment.environment import *

# -----------------------------------------------------------
# Name:         utils
# Author:       Jerem
# Date:         2021/2/11
# Description:
# ----------------------------------------------------------
import pandas as pd
import psutil
from pybpa.lsd.nrscp_lsd import LSD
from pywinauto.application import Application
import win32gui
import win32process

from tqdm.auto import trange
from tqdm import tqdm

from pybpa.dat.bpa_dat import DAT
from pybpa.organize.file_organize import DefaultOrganizer
from pybpa.lsd.nrscp_lsd import LSD
from pybpa.swi.bpa_swi import SWI
from pybpa.utils.utils import LHSGenerator, TopoDataGenerator, IslandFilter
import psutil

from functools import wraps
import time


IS_WIN32 = 'win32' in str(sys.platform).lower()
pfnt_path = r'D:\OneDrive\桌面\PsdEdit\BIN/'
pfnt_name = 'PFNT-20171220'
swnt_path = r'D:\OneDrive\桌面\PsdEdit\BIN/'
swnt_name = 'swnt3'
pfnt, swnt = pfnt_path + pfnt_name + '.exe', swnt_path + swnt_name + '.exe'
pf_time_tolerance = 5
ts_time_tolerance = 10
default_time_tolerance = 5
num_workers = 1
time_resolution = 0.001  # 轮询时间间隔
lock = RLock()


# ------------------------- fields --------------------------


# time装饰器
def timer(func):
    @wraps(func)  # 用来消除装饰器引起的func文档覆盖问题
    def wrap(*args, **kwargs):
        begin_time = time.perf_counter()
        result = func(*args, **kwargs)
        start_time = time.perf_counter()
        print(f'func:{func.__name__} took: {start_time - begin_time} sec')
        return result

    return wrap


def exe_key(mode: str, i: int):
    # """定义了这个脚本所有使用了exe副本的索引方式：exe后缀"""
    # return '_copy_' + str(i) + '.exe'
    return (swnt_name if mode == 'TS' else pfnt_name) + '_copy_' + str(i)





def subprocess_call(key: str, mode: str, *args, **kwargs):
    """
    针对swnt的运行失败弹窗占用内存的优化（NRSCP显然没有）
    当程序没有在time_tolerance内被正确执行时：
    1. 要么还没执行完成，强制结束进程
    2. 出错弹窗。这时候捕获窗口然后关闭
    :param key: str
    :param args:
    :param kwargs:
    :return:
    """
    # also works for Popen. It creates a new *hidden* window, so it will work in frozen apps (.exe).
    if IS_WIN32:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags = subprocess.CREATE_NEW_CONSOLE | subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        kwargs['startupinfo'] = startupinfo
    time_tolerance = kwargs.pop('timeout', default_time_tolerance)
    kwargs['stdin'] = subprocess.PIPE
    kwargs['stdout'] = subprocess.PIPE
    kwargs['stderr'] = subprocess.PIPE

    # 运行命令
    start_time = time.time()
    # time.sleep(random.random())  # 为什么要延迟来着？
    # outs, errs = 0, 0
    # debug注释
    proc = subprocess.Popen(*args, **kwargs)
    # 第3版，
    outs, errs = None, None
    try:
        for step in range(int(time_tolerance // time_resolution)):
            time.sleep(time_resolution)
            # 方法1，通过窗口
            hwnd = win32gui.FindWindow("#32770", key)  # 参数：类型，全名
            if hwnd != 0:
                while hwnd != 0:  # 可能没有正确关闭，所以需要多关几次
                    btnhdl = win32gui.FindWindowEx(hwnd, None, 'Button', '是(&Y)')  # 参数：窗口句柄, 不知道, 类型名, 控件文本全文
                    win32api.PostMessage(btnhdl, win32con.BM_CLICK, 0, 0)
                    hwnd = win32gui.FindWindow("#32770", key)
                break
                # childList = []
                # win32gui.EnumChildWindows(hwnd, lambda hwnd, param: param.append(hwnd), childList)
                # for child in childList:
                #     if '&Y' in win32gui.GetWindowText(child):
                #         win32api.PostMessage(child, win32con.BM_CLICK, 0, 0)



        # outs, errs = proc.communicate(timeout=time_tolerance)  # timeout 到期后子进程不会被清理

    except:  # 若要保证子进程被清理，需要手动捕获 timeout 异常. 潮流程序不会自己结束并退出
        pass
        # if mode == 'ts':
        #     os.kill(proc.pid)
            # try:  # 不用了，太慢了，要2-3秒
            #     # 捕获窗口，按下结束窗口的按键。
            #     app = Application(backend='uia').connect(title_re=key[:-4])
            #     app.window().print_control_identifiers()  # 展示窗口的所有控制编码
            #     app.window().type_keys('y')
            # except:
            #     pass
            # try:
            #     # 捕获 exe的pid
            #     pids = [p.pid for p in psutil.process_iter() if key in p.name()]
            #     if len(pids) > 0:
            #         os.kill(pids[0])
            # except:
            #     pass
    # 结束进程，如果还存在的话。
    finally:
        time.sleep(time_tolerance * 0.1)
        try:
            # 杀死报错的copy
            parent = psutil.Process(proc.pid)
            children = parent.children(recursive=True)
            for child in children:
                if child.name() == key:
                    child.kill()
            # 杀死进程组
            os.killpg(proc.pid)
            # psutil.Process(proc.pid).terminate()  # 终止指定pid的进程及其所有子进程。这种方法可以正常终止所有相关进程
        except:
            pass
            # print(f'进程及其子进程 {proc.pid} 没有正常中止！')
        # if proc.poll():
        #     proc.terminate()
        #     proc.kill()  # 同时手动清理子进程
        time_use = time.time() - start_time
    # 清理进程
    # # 清理ts的窗口
    # if mode == 'ts':
    #     try:
    #         window_title = ''
    #         # 捕获窗口，按下结束窗口的按键。
    #         app = Application(backend='uia').connect(title_re=window_title)
    #         # app.window().print_control_identifiers()  # 展示窗口的所有控制编码
    #         app.window().type_keys('y')
    #     except:
    #         pass

    # # 第二版，存在重定向到pipe之后，进程不会自动关闭的问题
    # while proc.poll() is None and time.time() < start_time + time_tolerance:  # 如果进程未结束且时间未到，则等待
    #     time.sleep(time_resolution)
    # time_duration = time.time() - start_time
    # # 清理进程
    # # 清理ts的窗口
    # if mode == 'ts':
    #     try:
    #         window_title = ''
    #         # 捕获窗口，按下结束窗口的按键。
    #         app = Application(backend='uia').connect(title_re=window_title)
    #         # app.window().print_control_identifiers()  # 展示窗口的所有控制编码
    #         app.window().type_keys('y')
    #     except:
    #         pass
    # # 结束进程，如果还存在的话。
    # if proc.poll() is None:
    #     proc.terminate()
    #     proc.kill()  # 同时手动清理子进程
    # outs, errs = proc.communicate()

    # # 监控进程，获取输出
    # try:
    #     outs, errs = proc.communicate(timeout=time_tolerance)  # timeout 到期后子进程不会被清理
    # except subprocess.TimeoutExpired:  # 若要保证子进程被清理，需要手动捕获 timeout 异常. 潮流程序不会自己结束并退出
    #     if mode == 'ts':
    #         try:
    #             # 捕获窗口，按下结束窗口的按键。
    #             app = Application(backend='uia').connect(title_re=key)
    #             # app.window().print_control_identifiers()  # 展示窗口的所有控制编码
    #             app.window().type_keys('y')
    #         except:
    #             pass
    #     # 结束进程，如果还存在的话。
    #     if proc.poll() is None:
    #         proc.terminate()
    #         proc.kill()			# 同时手动清理子进程
    #     outs, errs = proc.communicate()

    return outs, errs, time_use


def find_procs_by_file(file):
    """使用文件名查询占用该文件的线程，用来debug"""
    ls = []
    for p in psutil.process_iter(['name', 'exe', 'cmdline']):
        try:
            flist = p.open_files()
        except Exception:
            continue
        for nt in flist:
            if file.lower() in nt.path.lower():
                ls.append(p)
                break
    return ls

"""
南瑞步骤：
新建一个文件夹作为根目录
指定一个基础dat和一个基础swi和一个lsd
1. 生成方式文件夹
！按照文件名排序！这是记录进度的关键
2. 计算潮流
3. 根据lsd生成swi，调用swnt
由于调bpa的bug很多，所以最好能断点续传
"""


class NRSCPProject:
    TS_MODE, PF_MODE = 'TS', 'PF'
    OP_COL, PF_COL, PF_TIME_COL, PF_CODE_COL = 'operation', 'PF_state', 'PF_time', 'PF_code'
    TS_COL, CUR_COL = 'TS_state', 'current'

    def __init__(self, dir, base_dat=None, base_swi=None, base_lsd=None, project_name='default_project',
                 organizer=DefaultOrganizer):
        print(f'0.  创建项目，名称为 {project_name}')
        self.project_name = project_name
        self.dir = dir
        print(f'  0.0 文件结构定义,使用{organizer.__class__.__name__}, 查询结构定义，可以调用self.organizer.knowledge()')
        self.organizer = organizer(root_path=dir, project_name=project_name)
        if not os.path.exists(dir):
            os.makedirs(dir)
            print(f'  0.1 项目目录{dir}不存在，已创建。')
        else:
            if os.path.exists(self.organizer.get_project_file_path()):
                print(f'  0.1 项目目录{dir}已存在，从已有的项目文件 {project_name}.pybpa 加载')
                self.project = pd.read_csv(self.organizer.get_project_file_path())
                self.project.set_index(self.OP_COL, inplace=True)  # 从csv加载的话需要重新index，否则默认RangeIndex
            else:
                print(f'  0.1 项目目录{dir}已存在，项目文件{project_name}.pybpa 不存在，将被创建')
                self.project = pd.DataFrame(data=None, columns=[self.OP_COL, self.PF_COL, self.TS_COL,
                                                                self.PF_TIME_COL, self.PF_CODE_COL])
                self.project.set_index(self.OP_COL, inplace=True)  # project.loc[op_name]
                self.save()

        if os.path.exists(self.organizer.base_dat_path()):
            print(f'  0.2 项目目录已存在 {project_name}.dat, 优先级最高，以其为准。')
            self.dat = DAT.build_from(self.organizer.base_dat_path())
        elif isinstance(base_dat, DAT):
            print(f'  0.2 项目目录不存在 {project_name}.dat, 将输入的DAT实例存储到目录下。')
            self.dat = base_dat
            self.dat.save_to_file(self.organizer.base_dat_path())
        elif isinstance(base_dat, str):
            print(f'  0.2 项目目录不存在 {project_name}.dat, 将输入的dat文件复制到目录下。')
            self.dat = DAT.build_from(base_dat)
            self.dat.save_to_file(self.organizer.base_dat_path())
        else:
            raise ValueError('base_dat must be a str or a DAT object')

        self.mode = self.TS_MODE
        if os.path.exists(self.organizer.base_swi_path()):
            print(f'  0.2 项目目录已存在 {project_name}.swi, 优先级最高，以其为准。')
            self.swi = SWI.build_from(self.organizer.base_swi_path(), self.dat)
        elif isinstance(base_swi, SWI):
            print(f'  0.2 项目目录不存在 {project_name}.swi, 将输入的SWI实例存储到目录下。')
            self.swi = base_swi
            self.swi.save_to_file(self.organizer.base_swi_path())
        elif isinstance(base_swi, str):
            print(f'  0.2 项目目录不存在 {project_name}.swi, 将输入的dat文件复制到目录下。')
            self.swi = SWI.build_from(base_dat)
            self.swi.save_to_file(self.organizer.base_swi_path())
        elif base_swi is None:
            print(
                f'  0.2 项目目录不存在 {project_name}.swi, 也没有输入swi文件或实例，项目将只能在{self.PF_MODE}模式运行，后续需要{self.TS_MODE}模式则...')
            self.swi = None
            self.mode = self.PF_MODE
        else:
            raise ValueError('base_swi must be a str or a SWI object')

        if self.mode == self.PF_MODE:
            print(f'  0.3 项目运行在{self.PF_MODE}模式下，lsd设置为None')
            self.lsd = None
        elif os.path.exists(self.organizer.base_lsd_path()):
            print(f'  0.3 项目目录已存在 {project_name}.lsd, 优先级最高，以其为准。')
            self.lsd = LSD.build_from(dir + '/' + project_name + '.lsd')
        elif isinstance(base_lsd, LSD):
            print(f'  0.3 项目目录不存在 {project_name}.lsd, 将输入的LSD实例存储到目录下。')
            self.lsd = base_lsd
            self.lsd.save_to_file(self.organizer.base_lsd_path())
        elif isinstance(base_lsd, str):
            print(f'  0.3 项目目录不存在 {project_name}.lsd, 将输入的lsd文件复制到目录下。')
            self.lsd = LSD.build_from(base_lsd)
            self.lsd.save_to_file(self.organizer.base_lsd_path())
        elif base_lsd is None:
            print(
                f'  0.3 项目目录不存在 {project_name}.lsd, 也没有输入lsd文件或实例，项目将只能在{self.PF_MODE}模式运行，后续需要{self.TS_MODE}模式则...')
            self.lsd = None
            self.mode = self.PF_MODE
        else:
            raise ValueError('base_lsd must be a str or a LSD object')

        if self.mode == self.TS_MODE:
            self.project[[f[1] for f in self.lsd.faults]] = None

        print(f'  0.4.1 todo 检查dat，swi， lsd是否描述的是同一个系统。先默认是吧')
        self.check()
        self.refresh_project()

    def check(self):
        print('# todo 似乎不应该由项目来检查。因为单跑swnt时也需要这个。所以检查应该是swi发起对dat的检查，lsd发起对swi的检查')

    def refresh_project(self):
        """刷新project文件的信息"""
        op_list = [f for f in os.listdir(self.dir) if '.' not in f]
        for op in op_list:
            if op not in self.project.index:
                self.project.loc[op] = pd.Series(None, dtype=pd.Float32Dtype)
        self.save()
        print('refresh_report, saved to file.')

    def save(self):
        self.project.to_csv(self.organizer.get_project_file_path(), index=True, index_label=self.OP_COL)

    @timer
    def build_operations(self):
        print(f'  x. 开始创建方式。')

        # 检查lsd
        pqpqvt = np.zeros([6, 39], dtype=np.bool_)
        pqpqvt[2, 30:38] = True
        # generator = LHSGenerator(dat, pqpqvt, 0.4, truncate=0.9973)  # 3sigma
        generator = LHSGenerator(self.dat, pqpqvt, 0.01, truncate=1)
        # op_selector = lambda _: random.random() < 0.03
        op_selector = lambda *args, **kwargs: True
        topo_generator(0, 1, self.dat, self.organizer.root_path, 1, generator, make0=False,
                       lsd_writer=self.lsd, op_selector=op_selector, organizer=self.organizer)
        # 指定随机数生成器
        pqpqvt = np.zeros([6, 39], dtype=np.bool_)
        pqpqvt[2, 31:33] = True
        generator = LHSGenerator(self.dat, pqpqvt, std=0.3, truncate=0.9973)  # 3sigma

        # 指定数据过滤器（可选）

        # 指定拓扑过滤器（可选）

        # 指定拓扑生成器
        tg = TopoDataGenerator(dat=self.dat, target_root_path=self.organizer.root_path,
                               generator=generator, data_filter=lambda x: True,
                               file_organizer=None,
                               lsd=self.lsd,  # 需要随方式生成lsd
                               topo_filter=IslandFilter(self.dat))
        tg.gen(depth=0, target_depth=2, n_samples=20, dat_text_title='info的信息为同个拓扑下不同bus32、bus33节点处理的采样序号')

        # 加载到project文件
        self.refresh_project()

        print(f'  x. 方式创建结束，共生成了{len([f for f in os.listdir(self.dir) if "." not in f])}个方式。')

    @timer
    def sim_pf(self, num_workers):
        print(f'  x. 开始跑潮流。')

        op_list = list(self.project.index)
        for op in tqdm(op_list, desc='PF-simulation'):
            out, err, time_use = subprocess_call(exe_key(self.mode, 0),
                                                 'pf',
                                                 ' '.join([pfnt, self.organizer.get_dat_path(op)]),
                                                 timeout=pf_time_tolerance)
            # # 输出文件
            # with open(self.organizer.get_pfo_path(op), 'w') as f:
            #     f.write(out)

            self.project.loc[op] = {self.PF_TIME_COL: time_use, self.PF_CODE_COL: err}

        print(f'  x. 潮流结束，共计算了{len(op_list)}个方式。')

    @timer
    def sim_ts(self, num_workers):
        print(f'时间: {datetime.datetime.now()}, 项目: {self.project_name}, 地址: {self.dir}')
        tqdm.write(f'  x. 开始跑暂态。')

        op_list = self.project.index
        print(f'  需要仿真 {len(op_list)} 个方式')
        print(f'目前是通过手动打开目标目录，按修改时间排序查看。')

        # 检查exe副本是否足够，从1开始
        self.check_exe(self.TS_MODE, num_workers)

        # 方式1 https://www.codenong.com/9e2c75013d44050851ed/
        # print(f'父进程 {os.getpid()}')
        # freeze_support()
        if num_workers == 1:
            result = []
            for op in tqdm(op_list, leave=False, desc='任务总长度', ncols=100):
                result.append(self._sim_op_ts((op, {})))
        else:
            with Manager() as manager:
                d = manager.dict()
                with Pool(num_workers, initializer=tqdm.set_lock, initargs=(RLock(),)) as p:
                    result = p.map(self._sim_op_ts, zip(op_list, [d]*len(op_list)))
        for op_name, fault_dict in result:
            self.project.loc[op_name] = fault_dict

        # # 方式2
        # with Pool(processes=num_workers, initializer=tqdm.set_lock,
        #           initargs=(RLock(),)) as p:  # 试图设置tqdm显示多进程 https://www.freesion.com/article/3397514156/
        #     # todo 能在进程池开始接收工作前就知道所有进程pid吗？似乎不能，没有实例化。
        #     with tqdm(total=len(op_list), desc='TS-simulation', leave=True) as pbar:
        #         # 用imap_unordered好处：非阻塞，哪个完成哪个先输出。
        #         for i, result in enumerate(p.imap_unordered(self._sim_op_ts, op_list)):
        #             pbar.update()
        #             # deal with result
        #             op_name, fault_dict = result
        #             self.project.loc[op_name] = fault_dict

        print(f'  x. 暂态结束，共计算了{len(op_list)}个方式。')

        self.save()
        print(f' 项目文件已经保存。')
        return True

    def _sim_op_ts(self, inputs):
        """
        处理一个方式下的暂态仿真
        1. 根据 方式lsd 和 项目swi 生成执行swi
        2. 运行swnt
        3. 记录
        """
        time.sleep(random.random())
        op_name, d = inputs
        pid = os.getpid()
        if pid not in d:
            d[pid] = len(d) + 1
        proc_id = d[pid]
        exe = self.exe_path(proc_id)

        # 数据准备
        lsd = LSD(self.organizer.get_lsd_path(op_name=op_name))  # 结构 [line_id, fault_name]
        fault_dict = {}
        for i in trange(len(lsd.faults), desc=f'TS-proc_id={proc_id:>2}, {op_name:<20}', leave=False,
                        position=proc_id, ncols=100):
            fault = lsd.faults[i]
        # for fault in tqdm(lsd.faults, desc=f'TS-proc_id={proc_id:>2}, {op_name:<20}', leave=False, position=proc_id):
            # 1. 根据 方式lsd 和 项目swi 生成临时swi
            temp_swi_path = self.organizer.get_temp_swi_path(op_name=op_name, fault_name=fault[1])
            bse_path = self.organizer.get_bse_path(op_name)
            self.swi.save_to_file(path=temp_swi_path, temp_fault=lsd.get_fault_lines(fault_id=fault[1]))
            # 2. 仿真
            time.sleep(0.4)  # 出现file_not_found, 猜测是硬盘没有响应，所以需要时间且硬盘不能跑满
            out, err, time_use = subprocess_call(exe_key(self.mode, proc_id),
                                                 'ts',
                                                 ' '.join([exe, bse_path, temp_swi_path]),
                                                 timeout=pf_time_tolerance)

            time.sleep(0.1)
            # 3. 删除
            try:
                os.remove(temp_swi_path)
            except:
                # print(f'PermissionError: [Errno 13] 另一个程序正在使用此文件，进程无法访问。 以后再删。')
                for p in find_procs_by_file(temp_swi_path):
                    print(f'正在使用{temp_swi_path}的进程：{p}')
            # 4. L3.swx, L3.out, L3.err, L3.cur 改名
            for suffix in ('.OUT', '.ERR', '.CUR', '.SWX'):  # !大小写敏感!
                if os.path.exists(bse_path[:-4] + suffix):
                    try:
                        os.rename(bse_path[:-4] + suffix, temp_swi_path[:-4] + suffix)
                    except:
                        pass

            fault_dict[fault[1]] = time_use

        # # 同步锁
        # with lock:
        #     self.project.loc[op_name] = fault_dict
        return op_name, fault_dict

    @staticmethod
    def exe_path(i: int):
        return swnt[:-4] + '_copy_' + str(i) + '.exe'

    @staticmethod
    def check_exe(mode, num_workers):
        """为了后续查找窗口的唯一性，要为每个exe复制名字唯一的多个副本"""
        print(f'check_exe: num_workers={num_workers}, 应该拥有{num_workers}个swnt副本')
        exe = pfnt if mode == NRSCPProject.PF_MODE else swnt
        for i in range(1, num_workers+1):
            worker = NRSCPProject.exe_path(i)
            if not os.path.exists(worker):
                shutil.copy(exe, worker)
        print(f'check_exe: completed.')

    @timer
    def simulate(self, num_workers):
        # 单线程pf
        self.sim_pf(num_workers)

        if self.mode == self.PF_MODE:
            print(f'1.-1 项目模式为{self.PF_MODE}, 程序运行结束。')
            return

        # 多线程sw
        self.sim_ts(num_workers)

        # 记录文件
        self.refresh_project()

# 测试
if __name__ == '__main__':
    # prj_dir = f'E:\Data/transient_stability/39/bpa/34_n90/7/pt0/'
    # prj_dir = f'E:\Data/transient_stability/39/bpa/test/'
    # prj = NRSCPProject(prj_dir,
    #                    base_dat=DAT.build_from(prj_dir), base_swi=SWI.build_from(prj_dir), base_lsd=LSD.build_from(prj_dir),  # 在项目里面预先放入
    #                    project_name='milktest',
    #                    organizer=DefaultOrganizer)
    # prj.sim_ts(1)
    # 需要在cmd使用python nrscp.py 运行，才能不会出现进度条对不齐的情况

    # for id1 in ['7', '11', '20']:
    print('main仅用于示例，需要在cmd使用python nrscp.py 运行，才能不会出现进度条对不齐的情况')
    # parser = ArgumentParser()
    #
    # parser.add_argument('-l', type=int, default=7)
    # parser.add_argument('-p', type=int, default=1)
    # args = parser.parse_args()

    for p in [5]:
        # prj_dir = f'E:\Data/transient_stability/39/bpa/34_n90/{args.l}/pt{args.p}/'
        # prj_dir = f'E:\Data/transient_stability/39/bpa/34_n90/20/pt{p}/'
        prj_dir = r'E:\Data\transient_stability\39\bpa\test/'
        prj = NRSCPProject(prj_dir,
                           base_dat=DAT.build_from(prj_dir), base_swi=SWI.build_from(prj_dir), base_lsd=LSD.build_from(prj_dir),  # 在项目里面预先放入
                           project_name='milktest',
                           organizer=DefaultOrganizer)
        prj.sim_pf(9)

