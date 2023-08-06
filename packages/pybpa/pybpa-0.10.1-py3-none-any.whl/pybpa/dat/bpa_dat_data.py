# -*- coding:utf-8 -*-
"""
# Name:         transient_stability: bpa_dat_data
# Author:       MilkyDesk
# Date:         2021/7/1 16:31
# Description:
#   
"""

# ------------------------- fields --------------------------


# ------------------------- fields --------------------------
import inspect
import sys

from ..base.bpa_base import _build, CARD_TYPE
from ..base.bpa_uid import _TypeNameUid, _OneNameUid, _LineCard, BUS_NAME_STR, BUS_BASE_STR, BUS_NAME1_STR, \
    BUS_NAME2_STR, BUS_BASE1_STR, BUS_BASE2_STR, CKT_ID, GEN_P, GEN_P_MAX, GEN_Q_MAX, GEN_Q_MIN, LOAD_P, LOAD_Q, \
    GEN_Q, VMAX, ANGLE, SEC_ID


# ======================================================================================================================
#
#                                             #########################
#
# ======================================================================================================================

class DatB(_OneNameUid):
    fields, line, field_index = _build([[1, 2, CARD_TYPE, 'A2', 'B '],
                                        [3, 3, 'CHANGE CODE', 'A1'],
                                        [4, 6, 'OWNER', 'A3'],
                                        [7, 14, BUS_NAME_STR, 'A8'],
                                        [15, 18, BUS_BASE_STR, 'F4.0', None, 'kV'],
                                        [19, 20, 'ZONE', 'A2'],
                                        [21, 25, LOAD_P, 'F5.0', 0, 'MW'],
                                        [26, 30, LOAD_Q, 'F5.0', 0, 'MVA'],
                                        [31, 34, 'SHUNTZP', 'F4.0', 0, 'MW'],
                                        [35, 38, 'SHUNTZQ', 'F4.0', 0, 'MVA'],
                                        [39, 42, GEN_P_MAX, 'F4.0', 0, 'MVA'],
                                        [43, 47, GEN_P, 'F5.0', 0, 'MW'],
                                        [48, 52, GEN_Q, 'F5.0'],
                                        [53, 57, GEN_Q_MIN, 'F5.0'],
                                        [58, 61, VMAX, 'F4.3'],
                                        [62, 65, 'VMIN', 'F4.3']])


class DatBT(_OneNameUid):
    fields, line, field_index = _build([[1, 2, CARD_TYPE, 'A2', 'BT'],
                                        [3, 3, 'CHANGE CODE', 'A1'],
                                        [4, 6, 'OWNER', 'A3'],
                                        [7, 14, BUS_NAME_STR, 'A8'],
                                        [15, 18, BUS_BASE_STR, 'F4.0', None, 'kV'],
                                        [19, 20, 'ZONE', 'A2'],
                                        [21, 25, LOAD_P, 'F5.0', 0, 'MW'],
                                        [26, 30, LOAD_Q, 'F5.0', 0, 'MVA'],
                                        [31, 34, 'SHUNTZP', 'F4.0', 0, 'MW'],
                                        [35, 38, 'SHUNTZQ', 'F4.0', 0, 'MVA'],
                                        [39, 42, GEN_P_MAX, 'F4.0', 0, 'MVA'],
                                        [43, 47, GEN_P, 'F5.0', 0, 'MW'],
                                        [48, 52, GEN_Q, 'F5.0'],
                                        [53, 57, GEN_Q_MIN, 'F5.0'],
                                        [58, 61, VMAX, 'F4.3'],
                                        [62, 65, 'VMIN', 'F4.3']])


class DatBC(_OneNameUid):
    fields, line, field_index = _build([[1, 2, CARD_TYPE, 'A2', 'BC'],
                                        [3, 3, 'CHANGE CODE', 'A1'],
                                        [4, 6, 'OWNER', 'A3'],
                                        [7, 14, BUS_NAME_STR, 'A8'],
                                        [15, 18, BUS_BASE_STR, 'F4.0', None, 'kV'],
                                        [19, 20, 'ZONE', 'A2'],
                                        [21, 25, LOAD_P, 'F5.0', 0, 'MW'],
                                        [26, 30, LOAD_Q, 'F5.0', 0, 'MVA'],
                                        [31, 34, 'SHUNTZP', 'F4.0', 0, 'MW'],
                                        [35, 38, 'SHUNTZQ', 'F4.0', 0, 'MVA'],
                                        [39, 42, GEN_P_MAX, 'F4.0', 0, 'MVA'],
                                        [43, 47, GEN_P, 'F5.0', 0, 'MW'],
                                        [48, 52, GEN_Q, 'F5.0'],
                                        [53, 57, GEN_Q_MIN, 'F5.0'],
                                        [58, 61, VMAX, 'F4.3'],
                                        [62, 65, 'VMIN', 'F4.3']])


class DatBV(_OneNameUid):
    fields, line, field_index = _build([[1, 2, CARD_TYPE, 'A2', 'BV'],
                                        [3, 3, 'CHANGE CODE', 'A1'],
                                        [4, 6, 'OWNER', 'A3'],
                                        [7, 14, BUS_NAME_STR, 'A8'],
                                        [15, 18, BUS_BASE_STR, 'F4.0', None, 'kV'],
                                        [19, 20, 'ZONE', 'A2'],
                                        [21, 25, LOAD_P, 'F5.0', 0, 'MW'],
                                        [26, 30, LOAD_Q, 'F5.0', 0, 'MVA'],
                                        [31, 34, 'SHUNTZP', 'F4.0', 0, 'MW'],
                                        [35, 38, 'SHUNTZQ', 'F4.0', 0, 'MVA'],
                                        [39, 42, GEN_P_MAX, 'F4.0', 0, 'MVA'],
                                        [43, 47, GEN_P, 'F5.0', 0, 'MW'],
                                        [48, 52, GEN_Q, 'F5.0'],
                                        [53, 57, GEN_Q_MIN, 'F5.0'],
                                        [58, 61, VMAX, 'F4.3'],
                                        [62, 65, 'VMIN', 'F4.3']])


class DatBE(_OneNameUid):
    fields, line, field_index = _build([[1, 2, CARD_TYPE, 'A2', 'BE'],
                                        [3, 3, 'CHANGE CODE', 'A1'],
                                        [4, 6, 'OWNER', 'A3'],
                                        [7, 14, BUS_NAME_STR, 'A8'],
                                        [15, 18, BUS_BASE_STR, 'F4.0', None, 'kV'],
                                        [19, 20, 'ZONE', 'A2'],
                                        [21, 25, LOAD_P, 'F5.0', 0, 'MW'],
                                        [26, 30, LOAD_Q, 'F5.0', 0, 'MVA'],
                                        [31, 34, 'SHUNTZP', 'F4.0', 0, 'MW'],
                                        [35, 38, 'SHUNTZQ', 'F4.0', 0, 'MVA'],
                                        [39, 42, GEN_P_MAX, 'F4.0', 0, 'MVA'],
                                        [43, 47, GEN_P, 'F5.0', 0, 'MW'],
                                        [48, 52, GEN_Q_MAX, 'F5.0'],
                                        [53, 57, GEN_Q_MIN, 'F5.0'],
                                        [58, 61, VMAX, 'F4.3'],
                                        [62, 65, 'VMIN', 'F4.3']])


class DatBQ(_OneNameUid):
    fields, line, field_index = _build([[1, 2, CARD_TYPE, 'A2', 'BQ'],
                                        [3, 3, 'CHANGE CODE', 'A1'],
                                        [4, 6, 'OWNER', 'A3'],
                                        [7, 14, BUS_NAME_STR, 'A8'],
                                        [15, 18, BUS_BASE_STR, 'F4.0', None, 'kV'],
                                        [19, 20, 'ZONE', 'A2'],
                                        [21, 25, LOAD_P, 'F5.0', 0, 'MW'],
                                        [26, 30, LOAD_Q, 'F5.0', 0, 'MVA'],
                                        [31, 34, 'SHUNTZP', 'F4.0', 0, 'MW'],
                                        [35, 38, 'SHUNTZQ', 'F4.0', 0, 'MVA'],
                                        [39, 42, GEN_P_MAX, 'F4.0', 0, 'MVA'],
                                        [43, 47, GEN_P, 'F5.0', 0, 'MW'],
                                        [48, 52, GEN_Q_MAX, 'F5.0'],
                                        [53, 57, GEN_Q_MIN, 'F5.0'],
                                        [58, 61, VMAX, 'F4.3'],
                                        [62, 65, 'VMIN', 'F4.3']])


class DatBG(_OneNameUid):
    fields, line, field_index = _build([[1, 2, CARD_TYPE, 'A2', 'BG'],
                                        [3, 3, 'CHANGE CODE', 'A1'],
                                        [4, 6, 'OWNER', 'A3'],
                                        [7, 14, BUS_NAME_STR, 'A8'],
                                        [15, 18, BUS_BASE_STR, 'F4.0', None, 'kV'],
                                        [19, 20, 'ZONE', 'A2'],
                                        [21, 25, LOAD_P, 'F5.0', 0, 'MW'],
                                        [26, 30, LOAD_Q, 'F5.0', 0, 'MVA'],
                                        [31, 34, 'SHUNTZP', 'F4.0', 0, 'MW'],
                                        [35, 38, 'SHUNTZQ', 'F4.0', 0, 'MVA'],
                                        [39, 42, GEN_P_MAX, 'F4.0', 0, 'MVA'],
                                        [43, 47, GEN_P, 'F5.0', 0, 'MW'],
                                        [48, 52, GEN_Q_MAX, 'F5.0'],
                                        [53, 57, GEN_Q_MIN, 'F5.0'],
                                        [58, 61, VMAX, 'F4.3'],
                                        [62, 65, 'VMIN', 'F4.3'],
                                        [66, 73, 'REMOTE BUS', 'A8'],
                                        [74, 77, 'REMOTE BASE', 'F4.3', None, 'kV'],
                                        [78, 80, 'SUPPLIED VAR', 'F3.0', None, '%']])


class DatBX(_OneNameUid):
    fields, line, field_index = _build([[1, 2, CARD_TYPE, 'A2', 'BX'],
                                        [3, 3, 'CHANGE CODE', 'A1'],
                                        [4, 6, 'OWNER', 'A3'],
                                        [7, 14, BUS_NAME_STR, 'A8'],
                                        [15, 18, BUS_BASE_STR, 'F4.0', None, 'kV'],
                                        [19, 20, 'ZONE', 'A2'],
                                        [21, 25, LOAD_P, 'F5.0', 0, 'MW'],
                                        [26, 30, LOAD_Q, 'F5.0', 0, 'MVA'],
                                        [31, 34, 'SHUNTZP', 'F4.0', 0, 'MW'],
                                        [35, 38, 'SHUNTZQ', 'F4.0', 0, 'MVA'],
                                        [39, 42, GEN_P_MAX, 'F4.0', 0, 'MVA'],
                                        [43, 47, GEN_P, 'F5.0', 0, 'MW'],
                                        [48, 52, GEN_Q_MAX, 'F5.0'],
                                        [53, 57, GEN_Q_MIN, 'F5.0'],
                                        [58, 61, VMAX, 'F4.3'],
                                        [62, 65, 'VMIN', 'F4.3'],
                                        [66, 73, 'REMOTE BUS', 'A8'],
                                        [74, 77, 'REMOTE BASE', 'F4.3', None, 'kV'],
                                        [78, 80, 'SUPPLIED VAR', 'F3.0', None, '%']])


class DatBF(_OneNameUid):
    fields, line, field_index = _build([[1, 2, CARD_TYPE, 'A2', 'BF'],
                                        [3, 3, 'CHANGE CODE', 'A1'],
                                        [4, 6, 'OWNER', 'A3'],
                                        [7, 14, BUS_NAME_STR, 'A8'],
                                        [15, 18, BUS_BASE_STR, 'F4.0', None, 'kV'],
                                        [19, 20, 'ZONE', 'A2'],
                                        [21, 25, LOAD_P, 'F5.0', 0, 'MW'],
                                        [26, 30, LOAD_Q, 'F5.0', 0, 'MVA'],
                                        [31, 34, 'SHUNTZP', 'F4.0', 0, 'MW'],
                                        [35, 38, 'SHUNTZQ', 'F4.0', 0, 'MVA'],
                                        [39, 42, GEN_P_MAX, 'F4.0', 0, 'MVA'],
                                        [43, 47, GEN_P, 'F5.0', 0, 'MW'],
                                        [48, 52, GEN_Q_MAX, 'F5.0'],
                                        [53, 57, GEN_Q_MIN, 'F5.0'],
                                        [58, 61, VMAX, 'F4.3'],
                                        [62, 65, 'VMIN', 'F4.3']])


class DatBS(_OneNameUid):
    fields, line, field_index = _build([[1, 2, CARD_TYPE, 'A2', 'BS'],
                                        [3, 3, 'CHANGE CODE', 'A1'],
                                        [4, 6, 'OWNER', 'A3'],
                                        [7, 14, BUS_NAME_STR, 'A8'],
                                        [15, 18, BUS_BASE_STR, 'F4.0', None, 'kV'],
                                        [19, 20, 'ZONE', 'A2'],
                                        [21, 25, LOAD_P, 'F5.0', 0, 'MW'],
                                        [26, 30, LOAD_Q, 'F5.0', 0, 'MVA'],
                                        [31, 34, 'SHUNTZP', 'F4.0', 0, 'MW'],
                                        [35, 38, 'SHUNTZQ', 'F4.0', 0, 'MVA'],
                                        [39, 42, GEN_P_MAX, 'F4.0', 0, 'MVA'],
                                        [43, 47, GEN_P, 'F5.0', 0, 'MW'],
                                        [48, 52, GEN_Q_MAX, 'F5.0'],
                                        [53, 57, GEN_Q_MIN, 'F5.0'],
                                        [58, 61, 'VSCHED', 'F4.3'],
                                        [62, 65, ANGLE, 'F4.1']])


class DatBJ(_OneNameUid):
    fields, line, field_index = _build([[1, 2, CARD_TYPE, 'A2', 'BJ'],
                                        [3, 3, 'CHANGE CODE', 'A1'],
                                        [4, 6, 'OWNER', 'A3'],
                                        [7, 14, BUS_NAME_STR, 'A8'],
                                        [15, 18, BUS_BASE_STR, 'F4.0', None, 'kV'],
                                        [19, 20, 'ZONE', 'A2'],
                                        [21, 25, LOAD_P, 'F5.0', 0, 'MW'],
                                        [26, 30, LOAD_Q, 'F5.0', 0, 'MVA'],
                                        [31, 34, 'SHUNTZP', 'F4.0', 0, 'MW'],
                                        [35, 38, 'SHUNTZQ', 'F4.0', 0, 'MVA'],
                                        [39, 42, GEN_P_MAX, 'F4.0', 0, 'MVA'],
                                        [43, 47, GEN_P, 'F5.0', 0, 'MW'],
                                        [48, 52, GEN_Q_MAX, 'F5.0'],
                                        [53, 57, GEN_Q_MIN, 'F5.0'],
                                        [58, 61, VMAX, 'F4.3'],
                                        [62, 65, 'VMIN', 'F4.3']])


class DatBK(_OneNameUid):
    fields, line, field_index = _build([[1, 2, CARD_TYPE, 'A2', 'BK'],
                                        [3, 3, 'CHANGE CODE', 'A1'],
                                        [4, 6, 'OWNER', 'A3'],
                                        [7, 14, BUS_NAME_STR, 'A8'],
                                        [15, 18, BUS_BASE_STR, 'F4.0', None, 'kV'],
                                        [19, 20, 'ZONE', 'A2'],
                                        [21, 25, LOAD_P, 'F5.0', 0, 'MW'],
                                        [26, 30, LOAD_Q, 'F5.0', 0, 'MVA'],
                                        [31, 34, 'SHUNTZP', 'F4.0', 0, 'MW'],
                                        [35, 38, 'SHUNTZQ', 'F4.0', 0, 'MVA'],
                                        [39, 42, GEN_P_MAX, 'F4.0', 0, 'MVA'],
                                        [43, 47, GEN_P, 'F5.0', 0, 'MW'],
                                        [48, 52, GEN_Q_MAX, 'F5.0'],
                                        [53, 57, GEN_Q_MIN, 'F5.0'],
                                        [58, 61, 'VSCHED', 'F4.3'],
                                        [62, 65, 'ANGLE', 'F4.1']])


class DatBL(_OneNameUid):
    fields, line, field_index = _build([[1, 2, CARD_TYPE, 'A2', 'BL'],
                                        [3, 3, 'CHANGE CODE', 'A1'],
                                        [4, 6, 'OWNER', 'A3'],
                                        [7, 14, BUS_NAME_STR, 'A8'],
                                        [15, 18, BUS_BASE_STR, 'F4.0', None, 'kV'],
                                        [19, 20, 'ZONE', 'A2'],
                                        [21, 25, LOAD_P, 'F5.0', 0, 'MW'],
                                        [26, 30, LOAD_Q, 'F5.0', 0, 'MVA'],
                                        [31, 34, 'SHUNTZP', 'F4.0', 0, 'MW'],
                                        [35, 38, 'SHUNTZQ', 'F4.0', 0, 'MVA'],
                                        [39, 42, GEN_P_MAX, 'F4.0', 0, 'MVA'],
                                        [43, 47, GEN_P, 'F5.0', 0, 'MW'],
                                        [48, 52, GEN_Q_MAX, 'F5.0'],
                                        [53, 57, GEN_Q_MIN, 'F5.0'],
                                        [58, 61, 'VSCHED', 'F4.3'],
                                        [62, 65, 'ANGLE', 'F4.1']])


class DatBD(_OneNameUid):
    fields, line, field_index = _build([[1, 2, CARD_TYPE, 'A2', 'BD'],
                                        [3, 3, 'CHANGE CODE', 'A1'],
                                        [4, 6, 'OWNER', 'A3'],
                                        [7, 14, BUS_NAME_STR, 'A8'],
                                        [15, 18, BUS_BASE_STR, 'F4.0', None, 'kV'],
                                        [19, 20, 'ZONE', 'A2'],
                                        [24, 25, 'PBRCKT BRDGS', 'I2'],
                                        [26, 30, 'SMOOTHING REACTOR', 'F5.1', 0, 'Mh'],
                                        [31, 35, 'RECT OPER MIN', 'F5.1', 0, 'DEGREE'],
                                        [36, 40, 'INVERTER OPER STOP', 'F5.1', 0, 'DEGREE'],
                                        [41, 45, 'VOL DROP (VOLTS)', 'F5.1', 0, 'V'],
                                        [46, 50, 'BRDGE CRRNT RATING (AMPS)', 'F5.1', 0, 'A'],
                                        [51, 58, 'COMMUTATING BUS NAME', 'A8'],
                                        [59, 62, 'COMMUTATING BASE', 'F4.0', 0, 'kV']])


class DatX(_OneNameUid):
    fields, line, field_index = _build([[1, 2, CARD_TYPE, 'A2', 'X '],
                                        [3, 3, 'CHANGE CODE', 'A1'],
                                        [4, 6, 'OWNER', 'A3'],
                                        [7, 14, BUS_NAME_STR, 'A8'],
                                        [15, 18, BUS_BASE_STR, 'F4.0', None, 'kV'],
                                        [21, 28, 'RMT BUS NAME', 'A8'],
                                        [29, 32, 'RMT BUS BASE', 'F4.0', None, 'kV'],
                                        [33, 33, 'STEP1', 'I1'],
                                        [34, 38, 'DELTA MVAR1', 'F5.0', 0, 'MVAR'],
                                        [39, 39, 'STEP2', 'I1'],
                                        [40, 44, 'DELTA MVAR2', 'F5.0', 0, 'MVAR'],
                                        [45, 45, 'STEP3', 'I1'],
                                        [46, 50, 'DELTA MVAR3', 'F5.0', 0, 'MVAR'],
                                        [51, 51, 'STEP4', 'I1'],
                                        [52, 56, 'DELTA MVAR4', 'F5.0', 0, 'MVAR'],
                                        [57, 57, 'STEP5', 'I1'],
                                        [58, 62, 'DELTA MVAR5', 'F5.0', 0, 'MVAR'],
                                        [63, 63, 'STEP6', 'I1'],
                                        [64, 68, 'DELTA MVAR6', 'F5.0', 0, 'MVAR'],
                                        [69, 69, 'STEP7', 'I1'],
                                        [70, 74, 'DELTA MVAR7', 'F5.0', 0, 'MVAR'],
                                        [75, 75, 'STEP8', 'I1'],
                                        [76, 80, 'DELTA MVAR8', 'F5.0', 0, 'MVAR']])


class DatBB(_OneNameUid):
    """NOTE:组网点"""
    fields, line, field_index = _build([[1, 2, CARD_TYPE, 'A2', 'BB'],
                                        [3, 3, 'CHANGE CODE', 'A1'],
                                        [4, 6, 'OWNER', 'A3'],
                                        [7, 14, BUS_NAME_STR, 'A8'],
                                        [15, 18, BUS_BASE_STR, 'F4.0', None, 'kV'],
                                        [19, 20, 'ZONE', 'A2'],
                                        [22, 22, 'CTYPE', 'A1'],
                                        [24, 24, 'LEVEL', 'A1'],
                                        [39, 42, 'POWER PER', 'F4.2'],
                                        ])


class DatBM(_OneNameUid):
    """NOTE"""
    fields, line, field_index = _build([[1, 2, CARD_TYPE, 'A2', 'BM'],
                                        [3, 3, 'CHANGE CODE', 'A1'],
                                        [4, 6, 'OWNER', 'A3'],
                                        [7, 14, BUS_NAME_STR, 'A8'],
                                        [15, 18, BUS_BASE_STR, 'F4.0', None, 'kV'],
                                        [19, 20, 'ZONE', 'A2'],
                                        [21, 50, '待定', 'A30'],
                                        [51, 58, BUS_NAME2_STR, 'A8'],
                                        [59, 62, BUS_BASE2_STR, 'F4.0', None, 'kV']
                                        ])


    def get_y(self):
        raise ValueError('我有问题。')


class DatBZ(_OneNameUid):
    """NOTE：柔直"""
    fields, line, field_index = _build([[1, 2, CARD_TYPE, 'A2', 'BZ'],
                                        [3, 3, 'CHANGE CODE', 'A1'],
                                        [4, 6, 'OWNER', 'A3'],
                                        [7, 14, BUS_NAME_STR, 'A8'],
                                        [15, 18, BUS_BASE_STR, 'F4.0', None, 'kV'],
                                        [19, 20, 'ZONE', 'A2'],
                                        [22, 25, 'TOTAL MVA', 'F4.0'],
                                        [27, 32, 'R', 'F6.4'],
                                        [34, 39, 'L', 'F6.4'],
                                        [41, 43, 'LEVEL L NUM', 'I3'],
                                        [45, 49, 'C', 'F5.0', 0, 'uF'],
                                        [51, 55, 'LOSS', 'F5.4'],
                                        [57, 57, 'DC MOD', 'I1'],
                                        [59, 62, 'V HOLD', 'F4.3'],
                                        [64, 65, 'N POLE', 'I2'],
                                        [67, 71, 'DC BASE', 'F5.0'],
                                        [73, 77, 'POLE FDCR', 'F5.0', 0, 'mH'],
                                        [79, 83, 'GROUND FDCR', 'F5.0', 0, 'mH']])


class DatBZP(_OneNameUid):
    """NOTE：柔直"""
    fields, line, field_index = _build([[1, 3, CARD_TYPE, 'A3', 'BZ+'],
                                        [7, 14, BUS_NAME_STR, 'A8'],
                                        [15, 18, BUS_BASE_STR, 'F4.0', None, 'kV'],
                                        [20, 24, 'P', 'F5.0', 0, 'MW'],
                                        [26, 30, 'Q', 'F5.0', 0, 'MVar'],
                                        [34, 34, 'DC MOD', 'I1'],
                                        [36, 39, 'DC BASE', 'F4.0'],
                                        [41, 44, 'DC V HOLD', 'F4.0'],
                                        [46, 51, 'TRAN R', 'F6.5', 0, 'pu'],
                                        [53, 58, 'TRAN X', 'F6.5', 0, 'pu'],
                                        [60, 64, 'TAP1', 'F5.2'],
                                        [66, 70, 'TAP2', 'F5.2'],
                                        [72, 76, 'Q-COMP', 'F5.1']])


class DatBA(_OneNameUid):
    fields, line, field_index = _build([[1, 2, CARD_TYPE, 'A2', 'BA'],
                                        [3, 3, 'CHANGE CODE', 'A1'],
                                        [4, 6, 'OWNER', 'A3'],
                                        [7, 14, BUS_NAME_STR, 'A8'],
                                        [15, 18, BUS_BASE_STR, 'F4.0', None, 'kV'],
                                        [19, 20, 'ZONE', 'A2'],
                                        [22, 22, 'LTYPE', 'A1', None, 'R or I'],
                                        [24, 24, 'LBVBL', 'A1', None, 'H or L'],
                                        [26, 26, 'BRGNUM', 'I1'],
                                        [41, 45, 'SHUNT REACTOR', 'F5.1', None, 'mH'],
                                        [47, 50, 'POWER PER', 'F4.2', None, '%'],
                                        [52, 56, 'QSHUNT', 'F5.0']
                                        ])
class DatBA1(_OneNameUid):
    fields, line, field_index = _build([[1, 3, CARD_TYPE, 'A3', 'BA1'],
                                        [7, 14, BUS_NAME_STR, 'A8'],
                                        [15, 18, BUS_BASE_STR, 'F4.0', None, 'kV'],
                                        [20, 23, 'TRAN DCSIDE BASE', 'F4.0', None, 'kV'],
                                        [25, 28, 'TRAN RATE', 'F4.0', None, 'MVA'],
                                        [30, 35, 'TRAN R', 'F6.5', None, 'p.u.'],
                                        [37, 42, 'TRAN X', 'F6.5', None, 'p.u.'],
                                        [44, 49, 'TAP MAX', 'F6.2', None, 'kV'],
                                        [51, 56, 'TAP MIN', 'F6.2', None, 'kV'],
                                        [58, 59, 'TA NUM', 'A2']
                                        ])
class DatBA2(_OneNameUid):
    fields, line, field_index = _build([[1, 3, CARD_TYPE, 'A3', 'BA2'],
                                        [7, 14, BUS_NAME_STR, 'A8'],
                                        [15, 18, BUS_BASE_STR, 'F4.0', None, 'kV'],
                                        [20, 24, 'VAVLE DROP', 'F5.1', None, 'V'],
                                        [26, 30, 'BRDGE CUR RATING', 'F5.0', None, 'A'],
                                        [32, 36, 'ALPHA MIN', 'F5.1', None, 'degree'],
                                        [38, 42, 'ALPHA MAX', 'F5.1', None, 'degree'],
                                        [44, 48, 'ALPHA NORMAL', 'F5.1', None, 'degree'],
                                        [50, 54, 'GAMMA MIN', 'F5.1', None, 'degree'],
                                        [62, 66, 'TA NUM', 'F5.1', None, 'degree'],
                                        [68, 72, 'TA NUM', 'F5.0', None, 'kV']
                                        ])


class DatP(_OneNameUid):
    fields, line, field_index = _build([[1, 1, CARD_TYPE, 'A1', '+'],
                                        [2, 2, 'CODE', 'A1'],
                                        [3, 3, 'CHANGE CODE', 'A1'],
                                        [4, 6, 'OWNER', 'A3'],
                                        [7, 14, BUS_NAME_STR, 'A8'],
                                        [15, 18, BUS_BASE_STR, 'F4.0', None, 'kV'],
                                        [19, 20, 'CODE YEAR', 'A2'],
                                        [21, 25, LOAD_P, 'F5.0', 0, 'MW'],
                                        [26, 30, LOAD_Q, 'F5.0', 0, 'MVAR'],
                                        [31, 34, 'SHUNTZP', 'F4.0', 0, 'MW'],
                                        [35, 38, 'SHUNTZQ', 'F4.0', 0, 'MVAR'],
                                        [43, 47, GEN_P, 'F5.0', 0, 'MW'],
                                        [48, 52, GEN_Q, 'F5.0', 0, 'MVAR']])


class DatL(_LineCard):
    fields, line, field_index = _build([[1, 2, CARD_TYPE, 'A2', 'L '],
                                        [3, 3, 'CHANGE CODE', 'A1'],
                                        [4, 6, 'OWNER', 'A3'],
                                        [7, 14, BUS_NAME1_STR, 'A8'],
                                        [15, 18, BUS_BASE1_STR, 'F4.0', None, 'kV'],
                                        [19, 19, 'METER', 'I1'],
                                        [20, 27, BUS_NAME2_STR, 'A8'],
                                        [28, 31, BUS_BASE2_STR, 'F4.0', None, 'kV'],
                                        [32, 32, CKT_ID, 'A1'],
                                        [33, 33, SEC_ID, 'A1'],
                                        [34, 37, 'TOTAL CURRENT RATE AMP', 'F4.0'],
                                        [38, 38, 'OF CKT', 'I1', None, 'MW'],
                                        [39, 44, 'R', 'F6.5'],
                                        [45, 50, 'X', 'F6.5'],
                                        [51, 56, 'G', 'F6.5'],
                                        [57, 62, 'B', 'F6.5'],
                                        [63, 66, 'MILES', 'F4.1'],
                                        [67, 74, 'DESCDATA', 'A8'],
                                        [75, 75, 'DATA IN M', 'A1'],
                                        [76, 77, 'DATA IN Y', 'A2'],
                                        [78, 78, 'DATA OUT M', 'A1'],
                                        [79, 80, 'DATA OUT Y', 'A2']])


class DatLP(_LineCard):
    fields, line, field_index = _build([[1, 2, CARD_TYPE, 'A2', 'L+'],
                                        [3, 3, 'CHANGE CODE', 'A1'],
                                        [4, 6, 'OWNER', 'A3'],
                                        [7, 14, BUS_NAME1_STR, 'A8'],
                                        [15, 18, BUS_BASE1_STR, 'F4.0', None, 'kV'],
                                        [19, 19, 'METER', 'I1'],
                                        [20, 27, BUS_NAME2_STR, 'A8'],
                                        [28, 31, BUS_BASE2_STR, 'F4.0', None, 'kV'],
                                        [32, 32, CKT_ID, 'A1'],
                                        [33, 33, SEC_ID, 'A1'],
                                        [34, 38, 'MVAR1', 'F5.0'],
                                        [44, 48, 'MVAR2', 'F5.0']])
    def get_y(self):
        raise ValueError('我有问题。')


class DatE(_LineCard):
    fields, line, field_index = _build([[1, 2, CARD_TYPE, 'A2', 'E '],
                                        [3, 3, 'CHANGE CODE', 'A1'],
                                        [4, 6, 'OWNER', 'A3'],
                                        [7, 14, BUS_NAME1_STR, 'A8'],
                                        [15, 18, BUS_BASE1_STR, 'F4.0', None, 'kV'],
                                        [19, 19, 'METER', 'I1'],
                                        [20, 27, BUS_NAME2_STR, 'A8'],
                                        [28, 31, BUS_BASE2_STR, 'F4.0', None, 'kV'],
                                        [32, 32, CKT_ID, 'A1'],
                                        [33, 33, SEC_ID, 'A1'],
                                        [34, 37, 'TOTAL CURRENT RATE AMP', 'F4.0'],
                                        [38, 38, 'OF CKT', 'I1', 1, 'MW'],
                                        [39, 44, 'R', 'F6.5'],
                                        [45, 50, 'X', 'F6.5'],
                                        [51, 56, 'G1', 'F6.5'],
                                        [57, 62, 'B1', 'F6.5'],
                                        [63, 68, 'G2', 'F6.5'],
                                        [69, 74, 'B2', 'F6.5'],
                                        [75, 75, 'DATA IN M', 'A1'],
                                        [76, 77, 'DATA IN Y', 'I2'],
                                        [78, 78, 'DATA OUT M', 'A1'],
                                        [79, 80, 'DATA OUT Y', 'I2']])
    def get_y(self):
        raise ValueError('我有问题。')


class DatLD(_LineCard):
    fields, line, field_index = _build([[1, 2, CARD_TYPE, 'A2', 'LD'],
                                        [3, 3, 'CHANGE CODE', 'A1'],
                                        [4, 6, 'OWNER', 'A3'],
                                        [7, 14, BUS_NAME1_STR, 'A8'],
                                        [15, 18, BUS_BASE1_STR, 'F4.0', None, 'kV'],
                                        [20, 27, BUS_NAME2_STR, 'A8'],
                                        [28, 31, BUS_BASE2_STR, 'F4.0', None, 'kV'],
                                        [32, 32, CKT_ID, 'A1', ' ', '纯粹用作Uid占位符'],
                                        [34, 37, 'TOTAL CURRENT RATE AMP', 'F4.0'],
                                        [38, 43, 'R', 'F6.2'],
                                        [44, 49, 'L', 'F6.2'],
                                        [50, 55, 'C', 'F6.2'],
                                        [56, 56, 'CONTROL', 'A1'],
                                        [57, 61, 'DC LINE POWER', 'F5.1'],
                                        [62, 66, 'RECT VOLT', 'F5.1'],
                                        [67, 70, 'RECT TIFIER', 'F4.1', 0, 'DEGREE'],
                                        [71, 74, 'INVERTER', 'F4.1'],
                                        [75, 78, 'MILES', 'F4.0']])
    def get_y(self):
        raise ValueError('我有问题。')


class DatLM(_LineCard):
    fields, line, field_index = _build([[1, 2, CARD_TYPE, 'A2', 'LM'],
                                        [3, 3, 'CHANGE CODE', 'A1'],
                                        [4, 6, 'OWNER', 'A3'],
                                        [7, 14, BUS_NAME1_STR, 'A8'],
                                        [15, 18, BUS_BASE1_STR, 'F4.0', None, 'kV'],
                                        [20, 27, BUS_NAME2_STR, 'A8'],
                                        [28, 31, BUS_BASE2_STR, 'F4.0', None, 'kV'],
                                        [32, 32, CKT_ID, 'A1', ' ', '纯粹用作Uid占位符'],
                                        [34, 37, 'TOTAL CURRENT RATE AMP', 'F4.0'],
                                        [38, 43, 'R', 'F6.2'],
                                        [44, 49, 'L', 'F6.2'],
                                        [50, 55, 'C', 'F6.2'],
                                        [71, 74, 'MILES', 'F4.0'],
                                        [75, 75, 'DATA IN M', 'A1'],
                                        [76, 77, 'DATA IN Y', 'I2'],
                                        [78, 78, 'DATA OUT M', 'A1'],
                                        [79, 80, 'DATA OUT Y', 'I2']])
    def get_y(self):
        raise ValueError('我有问题。')


class DatT(_LineCard):
    fields, line, field_index = _build([[1, 2, CARD_TYPE, 'A2', 'T '],
                                        [3, 3, 'CHANGE CODE', 'A1'],
                                        [4, 6, 'OWNER', 'A3'],
                                        [7, 14, BUS_NAME1_STR, 'A8'],
                                        [15, 18, BUS_BASE1_STR, 'F4.0', None, 'kV'],
                                        [19, 19, 'METER', 'I1'],
                                        [20, 27, BUS_NAME2_STR, 'A8'],
                                        [28, 31, BUS_BASE2_STR, 'F4.0', None, 'kV'],
                                        [32, 32, CKT_ID, 'A1'],
                                        [33, 33, SEC_ID, 'A1'],
                                        [34, 37, 'CAPACITY MVA', 'F4.0'],
                                        [38, 38, 'OF CKT', 'A1'],
                                        [39, 44, 'R', 'F6.5'],
                                        [45, 50, 'X', 'F6.5'],
                                        [51, 56, 'G', 'F6.5'],
                                        [57, 62, 'B', 'F6.5'],
                                        [63, 67, 'TP1', 'F5.2'],
                                        [68, 72, 'TP2', 'F5.2'],
                                        [75, 75, 'DATA IN M', 'A1'],
                                        [76, 77, 'DATA IN Y', 'I2'],
                                        [78, 78, 'DATA OUT M', 'A1'],
                                        [79, 80, 'DATA OUT Y', 'I2']])


class DatTP(_LineCard):
    fields, line, field_index = _build([[1, 2, CARD_TYPE, 'A2', 'TP'],
                                        [3, 3, 'CHANGE CODE', 'A1'],
                                        [4, 6, 'OWNER', 'A3'],
                                        [7, 14, BUS_NAME1_STR, 'A8'],
                                        [15, 18, BUS_BASE1_STR, 'F4.0', None, 'kV'],
                                        [19, 19, 'METER', 'I1'],
                                        [20, 27, BUS_NAME2_STR, 'A8'],
                                        [28, 31, BUS_BASE2_STR, 'F4.0', None, 'kV'],
                                        [32, 32, CKT_ID, 'A1'],
                                        [33, 33, SEC_ID, 'A1'],
                                        [34, 37, 'CAPACITY MVA', 'F4.0'],
                                        [38, 38, 'OF CKT', 'I1', 1, 'MW'],
                                        [39, 44, 'R', 'F6.5'],
                                        [45, 50, 'X', 'F6.5'],
                                        [51, 56, 'G', 'F6.5'],
                                        [57, 62, 'B', 'F6.5'],
                                        [63, 67, 'PHASE SHIFT DEG', 'F5.2'],
                                        [75, 75, 'DATA IN M', 'A1'],
                                        [76, 77, 'DATA IN Y', 'I2'],
                                        [78, 78, 'DATA OUT M', 'A1'],
                                        [79, 80, 'DATA OUT Y', 'I2']])


class DatR(_LineCard):
    # todo 32,32 占位符来源成迷，不止一个地方
    fields, line, field_index = _build([[1, 2, CARD_TYPE, 'A2', 'R '],
                                        [3, 3, 'CHANGE CODE', 'A1'],
                                        [4, 6, 'OWNER', 'A3'],
                                        [7, 14, BUS_NAME1_STR, 'A8'],
                                        [15, 18, BUS_BASE1_STR, 'F4.0', None, 'kV'],
                                        [19, 19, 'METER', 'I1'],
                                        [20, 27, BUS_NAME2_STR, 'A8'],
                                        [28, 31, BUS_BASE2_STR, 'F4.0', None, 'kV'],
                                        [32, 32, CKT_ID, 'A1', ' ', '纯粹用作Uid占位符'],
                                        [34, 41, 'REMOTE BUS', 'A8'],
                                        [42, 45, 'REMOTE BASE', 'F4.0'],
                                        [46, 50, 'MAX TAP', 'F5.2'],
                                        [51, 55, 'MIN TAP', 'F5.2'],
                                        [56, 57, '#TAPS', 'I2']])
    def get_y(self):
        raise ValueError('我有问题:没有实现get_y()')


class DatRV(_LineCard):
    fields, line, field_index = _build([[1, 2, CARD_TYPE, 'A2', 'RV'],
                                        [3, 3, 'CHANGE CODE', 'A1'],
                                        [4, 6, 'OWNER', 'A3'],
                                        [7, 14, BUS_NAME1_STR, 'A8'],
                                        [15, 18, BUS_BASE1_STR, 'F4.0', None, 'kV'],
                                        [19, 19, 'METER', 'I1'],
                                        [20, 27, BUS_NAME2_STR, 'A8'],
                                        [28, 31, BUS_BASE2_STR, 'F4.0', None, 'kV'],
                                        [32, 32, CKT_ID, 'A1', ' ', '纯粹用作Uid占位符'],
                                        [34, 41, 'REMOTE BUS', 'A8'],
                                        [42, 45, 'REMOTE BASE', 'F4.0'],
                                        [46, 50, 'MAX TAP', 'F5.2'],
                                        [51, 55, 'MIN TAP', 'F5.2'],
                                        [56, 57, '#TAPS', 'I2']])
    def get_y(self):
        raise ValueError('我有问题。')


class DatRQ(_LineCard):
    fields, line, field_index = _build([[1, 2, CARD_TYPE, 'A2', 'RQ'],
                                        [3, 3, 'CHANGE CODE', 'A1'],
                                        [4, 6, 'OWNER', 'A3'],
                                        [7, 14, BUS_NAME1_STR, 'A8'],
                                        [15, 18, BUS_BASE1_STR, 'F4.0', None, 'kV'],
                                        [19, 19, 'METER', 'I1'],
                                        [20, 27, BUS_NAME2_STR, 'A8'],
                                        [28, 31, BUS_BASE2_STR, 'F4.0', None, 'kV'],
                                        [32, 32, CKT_ID, 'A1', ' ', '纯粹用作Uid占位符'],
                                        [34, 41, 'REMOTE BUS', 'A8'],
                                        [42, 45, 'REMOTE BASE', 'F4.0'],
                                        [46, 50, 'MAX TAP', 'F5.2'],
                                        [51, 55, 'MIN TAP', 'F5.2'],
                                        [56, 57, '#TAPS', 'I2'],
                                        [58, 62, 'SCHED Q', 'F5.0']])
    def get_y(self):
        raise ValueError('我有问题。')


class DatRN(_LineCard):
    fields, line, field_index = _build([[1, 2, CARD_TYPE, 'A2', 'RN'],
                                        [3, 3, 'CHANGE CODE', 'A1'],
                                        [4, 6, 'OWNER', 'A3'],
                                        [7, 14, BUS_NAME1_STR, 'A8'],
                                        [15, 18, BUS_BASE1_STR, 'F4.0', None, 'kV'],
                                        [19, 19, 'METER', 'I1'],
                                        [20, 27, BUS_NAME2_STR, 'A8'],
                                        [28, 31, BUS_BASE2_STR, 'F4.0', None, 'kV'],
                                        [32, 32, CKT_ID, 'A1', ' ', '纯粹用作Uid占位符'],
                                        [34, 41, 'REMOTE BUS', 'A8'],
                                        [42, 45, 'REMOTE BASE', 'F4.0'],
                                        [46, 50, 'MAX TAP', 'F5.2'],
                                        [51, 55, 'MIN TAP', 'F5.2'],
                                        [56, 57, '#TAPS', 'I2'],
                                        [58, 62, GEN_Q_MAX, 'F5.0'],
                                        [63, 67, GEN_Q_MIN, 'F5.0']])
    def get_y(self):
        raise ValueError('我有问题。')


class DatRP(_LineCard):
    fields, line, field_index = _build([[1, 2, CARD_TYPE, 'A2', 'RP'],
                                        [3, 3, 'CHANGE CODE', 'A1'],
                                        [4, 6, 'OWNER', 'A3'],
                                        [7, 14, BUS_NAME1_STR, 'A8'],
                                        [15, 18, BUS_BASE1_STR, 'F4.0', None, 'kV'],
                                        [19, 19, 'METER', 'I1'],
                                        [20, 27, BUS_NAME2_STR, 'A8'],
                                        [28, 31, BUS_BASE2_STR, 'F4.0', None, 'kV'],
                                        [32, 32, CKT_ID, 'A1', ' ', '纯粹用作Uid占位符'],
                                        [34, 41, 'REMOTE BUS', 'A8'],
                                        [42, 45, 'REMOTE BASE', 'F4.0'],
                                        [46, 50, 'MAX ANGLE', 'F5.2'],
                                        [51, 55, 'MIN ANGLE', 'F5.2'],
                                        [56, 57, '#TAPS', 'I2'],
                                        [58, 62, 'SCHED P', 'F5.0']])
    def get_y(self):
        raise ValueError('我有问题。')


class DatRM(_LineCard):
    fields, line, field_index = _build([[1, 2, CARD_TYPE, 'A2', 'RM'],
                                        [3, 3, 'CHANGE CODE', 'A1'],
                                        [4, 6, 'OWNER', 'A3'],
                                        [7, 14, BUS_NAME1_STR, 'A8'],
                                        [15, 18, BUS_BASE1_STR, 'F4.0', None, 'kV'],
                                        [19, 19, 'METER', 'I1'],
                                        [20, 27, BUS_NAME2_STR, 'A8'],
                                        [28, 31, BUS_BASE2_STR, 'F4.0', None, 'kV'],
                                        [32, 32, CKT_ID, 'A1', ' ', '纯粹用作Uid占位符'],
                                        [34, 41, 'REMOTE BUS', 'A8'],
                                        [42, 45, 'REMOTE BASE', 'F4.0'],
                                        [46, 50, 'MAX TAP', 'F5.2'],
                                        [51, 55, 'MIN TAP', 'F5.2'],
                                        [56, 57, '#TAPS', 'I2'],
                                        [58, 62, 'MAXP', 'F5.0'],
                                        [63, 67, 'MINP', 'F5.0']])
    def get_y(self):
        raise ValueError('我有问题。')


class DatRZ(_LineCard):
    fields, line, field_index = _build([[1, 2, CARD_TYPE, 'A2', 'RZ'],
                                        [3, 3, 'CHANGE CODE', 'A1'],
                                        [4, 6, 'OWNER', 'A3'],
                                        [7, 14, BUS_NAME1_STR, 'A8'],
                                        [15, 18, BUS_BASE1_STR, 'F4.0', None, 'kV'],
                                        [20, 27, BUS_NAME2_STR, 'A8'],
                                        [28, 31, BUS_BASE2_STR, 'F4.0', None, 'kV'],
                                        [32, 32, CKT_ID, 'A1'],
                                        [33, 33, 'SETION', 'A1'],
                                        [34, 34, 'MODE', 'A1'],
                                        [35, 39, 'PCMAX', 'F5.0'],
                                        [40, 44, 'PCMIN', 'F5.0'],
                                        [45, 48, 'INAMP', 'F4.0'],
                                        [49, 54, 'XIJMAX', 'F6.5'],
                                        [55, 60, 'XIJMIN', 'F6.5']])
    def get_y(self):
        raise ValueError('我有问题。')


class DatLZ(_LineCard):
    fields, line, field_index = _build([[1, 2, CARD_TYPE, 'A2', 'LZ'],
                                        [3, 3, 'CHANGE CODE', 'A1'],
                                        [4, 6, 'OWNER', 'A3'],
                                        [7, 14, BUS_NAME1_STR, 'A8'],
                                        [15, 18, BUS_BASE1_STR, 'F4.0', None, 'kV'],
                                        [20, 27, BUS_NAME2_STR, 'A8'],
                                        [28, 31, BUS_BASE2_STR, 'F4.0', None, 'kV'],
                                        [32, 32, CKT_ID, 'A1', ' ', '纯粹用作Uid占位符'],
                                        [33, 33, SEC_ID, 'A1', ' '],
                                        [34, 37, 'LINE RAT', 'F4.0'],
                                        [38, 43, 'R', 'F6.2'],
                                        [44, 49, 'L', 'F6.2'],
                                        [50, 55, 'C', 'F6.2'],
                                        [57, 61, 'SIDE1 SHUNTR', 'F5.0'],
                                        [62, 66, 'SIDE2 SHUNTR', 'F5.0'],
                                        [75, 78, 'LENTH', 'F4.0']])
class DatBZG(_OneNameUid):
    fields, line, field_index = _build([[1, 3, CARD_TYPE, 'A3', 'BZG'],
                                        [7, 14, BUS_NAME_STR, 'A8'],
                                        [15, 18, BUS_BASE_STR, 'F4.0', None, 'kV'],
                                        [20, 27, 'POS DCBUS NAME', 'A8'],
                                        [28, 31, 'POS DCBUS BASE', 'F4.0', None, 'kV'],
                                        [33, 40, 'NEG DCBUS NAME', 'A8'],
                                        [41, 44, 'NEG DCBUS BASE', 'F4.0', None, 'kV'],
                                        [46, 51, 'GND R', 'F6.2'],
                                        [53, 58, 'GND H', 'F6.2'],
                                        [60, 60, 'MODE', 'I1']])

class DatLZG(_LineCard):
    fields, line, field_index = _build([[1, 3, CARD_TYPE, 'A3', 'LZG'],
                                        [7, 14, BUS_NAME1_STR, 'A8'],
                                        [15, 18, BUS_BASE1_STR, 'F4.0', None, 'kV'],
                                        [20, 27, BUS_NAME2_STR, 'A8'],
                                        [28, 31, BUS_BASE2_STR, 'F4.0', None, 'kV'],
                                        [32, 32, CKT_ID, 'A1', ' ', '纯粹用作Uid占位符'],
                                        [33, 33, SEC_ID, 'A1', ' '],
                                        [34, 37, 'LINE RAT', 'F4.0'],
                                        [38, 43, 'R', 'F6.2'],
                                        [44, 49, 'L', 'F6.2'],
                                        [50, 55, 'C', 'F6.2'],
                                        [57, 61, 'SIDE1 SHUNTR', 'F5.0'],
                                        [62, 66, 'SIDE2 SHUNTR', 'F5.0'],
                                        [68, 68, 'MODE', 'I1']])


class DatTS(_TypeNameUid):
    fields, line, field_index = _build([[1, 2, CARD_TYPE, 'A2', 'TS'],
                                        [3, 80, '待定', 'A78']])


class DatTU(_TypeNameUid):
    fields, line, field_index = _build([[1, 2, CARD_TYPE, 'A2', 'TU'],
                                        [3, 80, '待定', 'A78']])

class DatLY(_LineCard):
    fields, line, field_index = _build([[1, 2, CARD_TYPE, 'A2', 'LY'],
                                        [3, 3, 'CHANGE CODE', 'A1'],
                                        [4, 6, 'OWNER', 'A3'],
                                        [7, 14, BUS_NAME1_STR, 'A8'],
                                        [15, 18, BUS_BASE1_STR, 'F4.0', None, 'kV'],
                                        [20, 27, BUS_NAME2_STR, 'A8'],
                                        [28, 31, BUS_BASE2_STR, 'F4.0', None, 'kV'],
                                        [34, 37, 'LINE RAT', 'F4.0', None, 'A'],
                                        [38, 43, 'DC R', 'F6.2', None, 'ohm'],
                                        [44, 49, 'DC L', 'F6.2', None, 'mH'],
                                        [50, 55, 'DC C', 'F6.2', None, 'uF'],
                                        [75, 78, 'LENTH', 'F4.0', None, 'km']])


class DatDC(_TypeNameUid):
    fields, line, field_index = _build([[1, 2, CARD_TYPE, 'A2', 'DC'],
                                        [3, 80, '待定', 'A78']])


class DatA(_TypeNameUid):
    fields, line, field_index = _build([[1, 1, CARD_TYPE, 'A1', 'A'],
                                        [2, 80, '待细化', 'A79']])


class DatI(_TypeNameUid):
    fields, line, field_index = _build([[1, 1, CARD_TYPE, 'A1', 'I'],
                                        [3, 3, 'CHANGE CODE', 'A1'],
                                        [4, 13, 'INTERCHANGE AREA NAME1', 'A10'],
                                        [15, 24, 'INTERCHANGE AREA NAME2', 'A10'],
                                        [27, 34, 'SCHED EXPORT FROM 1 TO 2', 'F8.0']])




# ======================================================================================================================
#
#                                             #########################
#
# ======================================================================================================================

# ======================================================================================================================

card_types = {cls[1].fields[cls[1].field_index[CARD_TYPE]].default: cls[1]
              for cls in inspect.getmembers(sys.modules[__name__], inspect.isclass)
              if '_' not in cls[0]}

# ======================================================================================================================