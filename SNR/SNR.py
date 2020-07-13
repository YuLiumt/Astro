# -*- coding:utf-8 -*-
# @Author  : Yu Liu
# @Email   : yuliumutian@gmail.com
# @Software: PyCharm

import numpy as np


def radius(theta, d):
    r = 2 * np.pi * theta * d * 1000 / (360 * 60)
    return r

def h(b, d):
    h = 2 * np.pi * b * d * 1000 / 360
    return h

class SNR:
    def __init__(self, E, n, r):
        self.E = E
        self.n = n
        self.r = r

    def year(self):
        t = (0.61 * 1.6733 * 10 ** -24 * self.n) ** 0.5 \
            * (self.r * 3.08 * 10 ** 18) ** 2.5 \
            * (self.E) ** -0.5 \
            / 2.026
        y = t / (365 * 24 * 60 * 60)
        return y

if __name__ == '__main__':
     r = radius(9, 6)
     print(r)
     G = SNR(10 ** 50, 0.001, r)
     print(G.year())
#    h = h(6.2, 15)
#    print(h)
