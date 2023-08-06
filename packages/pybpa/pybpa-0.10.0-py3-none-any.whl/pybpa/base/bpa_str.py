#!/usr/bin/python
# -*- coding: gbk -*-


BPA_LINE_LEN = 86  # �ȶ�5.3�汾��80��5.7�汾��86

def bpa_card_line(bline: str):
    """
    �淶��bpa�ļ��С�
    ���ڲ��Ǵ����е��У���������ļ��У�
    1. ȥ����ĩ�����������Ŀո�\r��\n, \t
    2. �ÿո��뵽BPA_LINE_LEN����
    """
    return bline.strip().ljust(BPA_LINE_LEN)


class FFFloat2Str:
    def __init__(self, w, d):
        self.w = w
        self.d = d
        self.max = 10 ** (w - (1 if d else 0))
        self.min = -1 * 10 ** (w - 1 - (1 if d else 0))
        self.pfull = 10 ** (w - d - 1)
        self.nfull = -1 * 10 ** (w - d - 2)

    def write(self, fl):
        f = fl[0]
        if not f:
            return ' ' * self.w
        assert self.min < f < self.max

        f += 0.0
        if self.pfull < f < self.pfull * 10 or 10 * self.nfull < f < self.nfull:
            f *= 10 ** (3 * self.d)
            return ('{:.' + str(self.w) + 'f}').format(f)[:self.w].ljust(self.w)

        s = ('{:.' + str(self.w) + 'f}').format(abs(f))
        if s[:2] == '0.':
            s = s[1:]
        if f < 0:
            s = '-' + s
        return s[:self.w].ljust(self.w)


if __name__ == '__main__':
    import fortranformat as ff
    class t:
        def __init__(self, w, b):
            self.a = ff.FortranRecordReader('F' + str(w) + '.' + str(b))
            self.b = FFFloat2Str(w, b)
        def w(self, f):
            h = self.b.write([f])
            g = self.a.read(h)[0]
            return g == f, '\t'.join([str(f), h, str(g)])

    a = FFFloat2Str(6, 5)  # todo F6.5  ��.00008,д����8.0000
    print(a.write([.00008]))
    print(a.write([-321.12345]))
    print(a.write([.12345]))
    print(a.write([-.12345]))
    #
    # b = t(5, 4)
    # for i in range(1000000):
    #     f, s = b.w(i / 10000)
    #     if not f:
    #         print(i, '\t' + s)
