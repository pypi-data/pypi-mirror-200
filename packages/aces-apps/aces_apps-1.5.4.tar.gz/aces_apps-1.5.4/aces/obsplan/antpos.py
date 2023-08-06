from __future__ import print_function

"""
Holds AKSAP antenna positions, and utility routines.

Only use these approximate values for rough calculations.  For exact antenna positions, issue the following command on
aktos11 for the main array antennas and on akscor01 for the commissioning array antennas:

    fcm get |grep itrf
"""
import numpy as np
import itertools

antrel01 = np.array([[0.000, 0.000],
                     [26.978, -13.011],
                     [35.950, 7.490],
                     [-8.979, 35.008],
                     [-73.992, 31.503],
                     [135.660, 112.000],
                     [242.860, -109.980],
                     [-37.810, -238.510],
                     [-244.210, 110.550],
                     [-96.316, 279.496],
                     [267.951, 340.539],
                     [395.925, 269.476],
                     [438.720, -364.005],
                     [-24.860, -460.009],
                     [-739.700, -157.993],
                     [-636.115, 365.440],
                     [-496.818, 522.519],
                     [-106.785, 375.509],
                     [217.814, 481.520],
                     [506.320, 315.027],
                     [686.168, 322.006],
                     [845.840, 335.982],
                     [-0.708, -657.007],
                     [78.472, -978.523],
                     [-613.617, 653.507],
                     [-393.336, 667.503],
                     [-1070.503, 940.975],
                     [249.765, 1198.511],
                     [565.930, 753.210],
                     [1229.056, 798.468],
                     [2220.949, 992.985],
                     [3024.925, -2507.046],
                     [25.026, -2810.965],
                     [-2975.009, -2006.978],
                     [-2170.998, 992.991],
                     [23.232, 3190.068]])

ASKAP_antennas = range(1, 37)
BETA_antennas = [6, 1, 3, 15, 8, 9]
ASKAP_6_antennas = [2, 4, 5, 12, 13, 14]
ASKAP_12_antennas = [2, 4, 5, 10, 12, 13, 14, 16, 24, 27, 28, 30]

# as at 13/6/2018
ASKAP_main_antennas = [1, 2, 3, 4, 5, 6, 10, 12, 14, 16, 17, 19, 24, 27, 28, 30]
ASKAP_commissioning_antennas = [7, 8, 9, 11, 13, 15, 18, 20, 21, 22, 23, 25, 26, 29, 31, 32, 33, 34, 35, 36]


class AskapArray(object):
    def __init__(self, name):
        self.name = name
        if name == "BETA":
            self.arrayAntennas = BETA_antennas
        elif name == "ASKAP6":
            self.arrayAntennas = ASKAP_6_antennas
        elif name == "ASKAP12":
            self.arrayAntennas = ASKAP_12_antennas
        elif name == "ASKAP":
            self.arrayAntennas = ASKAP_antennas
        else:
            print('ASKAP_array: Unknown name %s' % name)
            self.arrayAntennas = []
        self.antennas = [a for a in self.arrayAntennas]
        self.baselines = self.gen_baselines()

    def select_antennas(self, antennas):
        self.antennas = [a for a in self.arrayAntennas if a in antennas]
        self.gen_baselines()

    def gen_baselines(self):
        ants = self.antennas
        n_ants = len(self.antennas)
        temp = [['%dx%d' % (ants[j], ants[i]) for i in range(j + 1, n_ants)] for j in range(n_ants)]
        return list(itertools.chain.from_iterable(temp))

    def get_ant_codes(self):
        bc = {}
        for bas in self.baselines:
            ants = map(int, bas.split('x'))
            iants = [ants.index(i) for i in ants]
            bc[bas] = iants
        return bc

    def get_ant_names(self):
        ret = ["AK%02d" % a for a in self.antennas]
        return ret


def baseline_2vec(bas):
    a1, a2 = map(int, bas.split('x'))
    vec = antrel01[a1 - 1] - antrel01[a2 - 1]
    return vec


def baseline_2v(a1, a2):
    vec = antrel01[a1 - 1] - antrel01[a2 - 1]
    return vec


def baseline_len(a1, a2):
    vec = antrel01[a1 - 1] - antrel01[a2 - 1]
    return np.sqrt((vec * vec).sum())
