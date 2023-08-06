#!/usr/bin/env python


from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
import argparse as ap
import sys

import time
import matplotlib.pylab as plt
import numpy as np

from numpy import pi

import pickle
import scipy.special as ssp
from scipy.interpolate import interp1d, interp2d, griddata

import glob
import itertools
from aces.obsplan.config import ACESConfig

aces_cfg = ACESConfig()
fp_factory = aces_cfg.footprint_factory

HELP_START = """This estimates the ASKAP survey speed for an optimum setting of the beam separation.
It does this for any available footprint, and gives results as a function of frequency.
The results are saved into python pickle files and used to construct some summary plots.
The -p option will do the plotting without re-doing the time-consuming optimising calculations.

The Fov_method options (chosen with '-m') are:
  sefd  USe recent SEFD measures across footprint
  image Use recent estimates from image noise across mosaic
  old   Use the original measurement made with BETA (Mark I PAF)

V 2April2019
"""
explanation = "\n" + HELP_START + "\n\n"

announce = "\ns_optimise.py\n"
fp_choices = [a for a in fp_factory.get_footprint_names() if a.startswith("ak:") or a.startswith("xx:")]

def arg_init():
    """Define the interpretation of command line arguments.
    """
    parser = ap.ArgumentParser(prog='s_optimise',
                               formatter_class=ap.RawDescriptionHelpFormatter,
                               description=HELP_START,
                               epilog='See -x for more explanation .')
    parser.add_argument('-o', '--output_suffix', default='', help='Optional suffix for output plot files')
    parser.add_argument('-f', '--fpnames', nargs='*', choices=fp_choices, default='ak:square_6x6',
                        help='Footprint name')
    parser.add_argument('-m', '--fov_method', choices=('old', 'sefd', 'image'), default='sefd',
                        help='FoV method to use')
    parser.add_argument('-q', '--frequencies', nargs='*', type=float, default=1000., help='Frequencies')
    parser.add_argument('-p', '--plot_only', action='store_true', help="Only plot previous results")
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-x', '--explain', action='store_true', help="Give an expanded explanation")
    return parser


class intList(ap.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        # print 'ACTION : %r %r %r' % (namespace, values, option_string)
        safe_dict = {'range': range}
        rp = eval(values, safe_dict)
        if isinstance(rp, int):
            rp = [rp]
        setattr(namespace, self.dest, rp)


def bsect(x, z):
    n = len(x)
    j1 = 0
    j2 = n
    j = j1
    while (j2 - j1) > 1:
        j = (j1 + j2) / 2
        if x[j] == z:
            break
        if x[j] > z:
            j2 = j
        else:
            j1 = j
    if x[j] > z:
        j = j - 1
    return j


class Timer:
    def __init__(self):
        self.t0 = 0.
        self.cpu0 = 0.
        self.t1 = 0.
        self.cpu1 = 0.
        self.reset()

    def reset(self):
        self.t0 = time.time()
        self.cpu0 = time.clock()
        self.t1 = self.t0
        self.cpu1 = self.cpu0

    def getTotal(self):
        return time.time() - self.t0

    def getDelta(self):
        t1 = time.time()
        delta = t1 - self.t1
        self.t1 = t1
        return delta


root2 = np.sqrt(2.0)


def fit_parabola(x, y):
    """
    Fit a parabola to three points
    :param x: the three abscissae
    :param y: the three ordinates
    :return: the coefficients of x**0, x**1, x**2
    """
    a = np.zeros([3, 3])
    a[:, 0] = 1.0
    a[:, 1] = x
    a[:, 2] = x**2
    ai = np.linalg.inv(a)
    b = np.dot(ai, y)
    return b


def fit_parabola(x, y):
    """
    Fit a parabola to the given points. If len(x) == 3, find the unique coefficients; otherwise
    perform a least-squares fit.
    :param x: the three abscissae
    :param y: the three ordinates
    :return: the coefficients of x**0, x**1, x**2
    """
    N = len(x)
    a = np.zeros([N,3])
    a[:,0] = 1.0
    a[:,1] = x
    a[:,2] = x**2
    if N == 3:
        ai = np.linalg.inv(a)
        coeff = np.dot(ai,y)
    else:
        coeff, r, rank, s = np.linalg.lstsq(a, y)
    return coeff


def airy(x):
    # Return airy function value at x
    # x in units of lambda/D
    return 2 * ssp.jn(1, x * pi) / x / pi


def airy1d(xgrid, xc, wid=1.0):
    wf = 0.7095 * wid
    aix = airy((xgrid - xc) / wf)
    aix[np.isnan(aix)] = 1.0
    return aix


def airy2d(xgrid, xc, yc, wid=1.0):
    wf = 0.7095 * wid
    x, y = np.meshgrid(xgrid, xgrid)
    r = np.sqrt((x - xc) * (x - xc) + (y - yc) * (y - yc))
    aix = airy(r / wf)
    aix[np.isnan(aix)] = 1.0
    return aix


def gauss1d(M, dxy, xc, wid=1.0):
    x0 = - M / 2 * dxy
    x1 = M / 2 * dxy
    x = np.arange(x0, x1, dxy)
    ag2 = wid ** 2 / (4 * np.log(2))
    r2 = (x - xc) ** 2 / ag2
    z = np.exp(-r2)
    return x, z


def gauss2d(xgrid, xc, yc, wid=1.0):
    x, y = np.meshgrid(xgrid, xgrid)
    ag2 = wid ** 2 / (4 * np.log(2))
    r2 = ((x - xc) ** 2 + (y - yc) ** 2) / ag2
    z = np.exp(-r2)
    return x, z


def empiricalFWHM(freq):
    # return the empirically deermined FWHM as a function of frequency in MHz.
    factor = 1.09
    D = 12.0
    fwhm = 299.8 / freq / D * factor
    return fwhm


def getGrid(M, w):
    xg = np.linspace(-w, w, M)
    return xg


def makeBeams(xgrid, offsets, fwhm):
    # compute beam values on given grid
    # at offsets given
    # Produces voltage beams with the given FWHM once converted to power.
    wi = 1.368
    wia = wi * fwhm
    Nb = offsets.shape[0]
    tbeams = None
    for i in range(Nb):
        xci, yci = offsets[i]
        ai0 = airy2d(xgrid, xci, yci, wid=wia)
        if i == 0:
            tbeams = ai0
        else:
            tbeams = np.dstack((tbeams, ai0))
    if Nb == 1:
        tbeams = np.expand_dims(tbeams, axis=2)
    abeams = np.transpose(tbeams, (2, 0, 1))
    return abeams


def calcCov(abeams):
    Nb = abeams.shape[0]
    for i in range(Nb):
        psai = []
        ai0 = abeams[i, :, :]
        d0 = (ai0**2).sum()
        for j in range(Nb):
            aia = abeams[j, :, :]
            num = (ai0*aia).sum()**2
            den = d0 * (aia**2).sum()
            psai.append(num/den)
        ra = np.array(psai)

        if i == 0:
            ra2 = ra
        else:
            ra2 = np.vstack((ra2, ra))
    cov = np.matrix(ra2)
    return cov


# def calcCov(abeams):
#     Nb = abeams.shape[0]
#     ra2 = None
#     for i in range(Nb):
#         psai = []
#         ai0 = abeams[i, :, :]
#         for j in range(Nb):
#             aia = abeams[j, :, :]
#             psai.append((ai0 * aia).sum())
#         psai = np.array(psai)
#         ra = psai ** 2 / (ai0 ** 2).sum() ** 2
#         if i == 0:
#             ra2 = ra
#         else:
#             ra2 = np.vstack((ra2, ra))
#     cov = np.matrix(ra2)
#     # print ('cov min,max ', cov.min(), cov.max())
#     return cov
#

def get_cross_sep(offsets):
    N = offsets.shape[0]
    ret = np.zeros([N, N])
    for i in range(N):
        for j in range(i, N):
            sep = np.linalg.norm(offsets[j] - offsets[i])
            ret[i, j] = sep
            ret[j, i] = sep
    return ret


def corr_func(x):
    # An empirically determined function giving beam to beam correlation coefficient depending on
    # beam separation
    # x - array of beam-to-beam separations
    xf = x.flatten()
    # p = [0.8715995, 0.48246021, 0.1284005]
    p = [0.98044135, 0.57611785, 0.0]
    return np.reshape(p[0] * np.exp(-(xf / p[1]) ** 2) + p[2], x.shape)


def cv_modelled(offsets, fwhm):
    cs = get_cross_sep(offsets) / fwhm
    cv = corr_func(cs)
    return cv


def polyval2d(x, y, m):
    order = int(np.sqrt(len(m))) - 1
    ij = itertools.product(range(order + 1), range(order + 1))
    z = np.zeros_like(x)
    for a, (i, j) in zip(m, ij):
        z += a * x ** i * y ** j
    return z


def fnc(x, a, e):
    # note the pattern trimming limit of 4.2 degrees
    y = 1.0 / (1 + (x / a) ** e)
    y[abs(x) > 4.2] = 0.0
    return y


def designMat_2(X, Y, b):
    al = [X, Y]
    for f in [0.71, 1.0, 1.41, 2.0, 2.82]:
        b1 = f * b
        for i in [2, 4, 8]:
            al.append(fnc(X, b1, i) * fnc(Y, b1, i))
    A = np.array(al).T
    return A


def apodizePAF(xgrid, centre=None, posang=0.0, unit=False, fov_method='sefd'):
    if fov_method == 'sefd':
        return apodizePAF_new(xgrid, centre, posang, unit, from_image=False)
    elif fov_method == 'image':
        return apodizePAF_new(xgrid, centre, posang, unit, from_image=True)
    elif fov_method == 'old':
        return apodizePAF_old(xgrid, centre, posang, unit)
    else:
        print ("apodizePAF : unknown FoV method {}".format(fov_method))
        sys.exit()


def apodizePAF_old(xgrid, centre=None, posang=0.0, unit=False):
    # Define an apodizing function that mimics the observed sensitivity variation across the PAF.
    # formed from fit to a set of rational functions, parameters in variable m
    # Expects xgrid (in radians), centre and PA (position angle) both in radians.
    # Needs access to functions designMat and fnc

    # print ("apodizePAF_old ", xgrid.shape, xgrid[:3])
    if centre is None:
        centre = [0.0, 0.0]
    if unit:
        apod = np.ones((xgrid.shape[0], xgrid.shape[0]))
    else:
        designMat = designMat_2
        # coeff = np.array([1.28107531e+01, 4.56911754e-01, 5.17826052e-01,-1.51419796e+02,-1.49542178e+01,
        #         -1.58078435e+00, 6.77485394e+02, 4.67563591e+01, -6.80814573e+00,-1.41500519e+03,
        #          1.23011095e+02, 4.87414906e+01,  1.10677965e+03,  -5.81216252e+02, 1.55424512e+02])

        # These parameters were derived from SBIDs around ~2024 (2016-September) with 48MHz bandwidth
        # near 1304 MHz, using antennas :
        #       ant4,ant5,ant10,ant12,ant13,ant14,ant16,ant24,ant27,ant28,ant30
        coeff = np.array([5.09633567e-04, -6.67986801e-04, -1.53786901e+01, -1.90039866e+00,
                          -5.02886076e-01, 1.10132646e+02, 1.07159428e+01, 9.09866150e-01,
                          -3.56162780e+02, -1.44262434e+01, 3.35535219e+00, 6.17456821e+02,
                          -1.26227972e+02, -2.47940423e+01, -4.38376122e+02, 4.48199146e+02,
                          -2.12011984e+02])
        b = 3.84
        SMALL = 1.0e-4
        cosa, sina = np.cos(posang), np.sin(posang)
        xg, yg = np.meshgrid(xgrid, xgrid)
        Xr = np.degrees(xg.flatten())
        Yr = np.degrees(yg.flatten())
        X = cosa * Xr - sina * Yr
        Y = sina * Xr + cosa * Yr
        xc, yc = centre
        xcd = np.degrees(cosa * xc - sina * yc)
        ycd = np.degrees(sina * xc + cosa * yc)

        xr = (X - xcd)
        yr = (Y - ycd)

        A = designMat(xr, yr, b)
        apod = np.reshape(np.dot(A, coeff), xg.shape)
        # trimming the pattern is done in fnc(x,a,e) with a hard coded value!
        rlim = np.radians(4.7)
        # xylim = np.radians(4.0)
        apod[(xg - xc) ** 2 + (yg - yc) ** 2 > rlim ** 2] = SMALL
        apod[apod < 0.0] = SMALL
        apod /= apod.max()
    return apod


def apodizePAF_new(xgrid, centre=None, posang=0.0, unit=False, from_image=True):
    # Define an apodizing function that mimics the observed sensitivity variation across the PAF.
    # This version is deduced from image sensitivity across 36-beam mosaics.
    # See notebook "FoV_from_rms_tiles"
    # Expects xgrid (in radians), centre and PA (position angle) both in radians.
    # (centre and PA ignored at present.)
    if centre is None:
        centre = [0.0, 0.0]

    SMALL = 1.0e-4

    if unit:
        apod = np.ones((xgrid.shape[0], xgrid.shape[0]))
    else:
        if from_image:
            p = open('/Users/mcc381/software/jupyter/FoV/fov_1.05.pkl', 'rb')
        else:
            p = open('/Users/mcc381/software/jupyter/FoV/fov_sefd_1.05.pkl', 'rb')

        package = pickle.load(p)
        pitch, newp, newm = package

        cosa, sina = np.cos(posang), np.sin(posang)
        xg, yg = np.meshgrid(xgrid, xgrid)
        Xr = np.degrees(xg.flatten())
        Yr = np.degrees(yg.flatten())
        X = cosa * Xr - sina * Yr
        Y = sina * Xr + cosa * Yr
        xc, yc = centre
        xcd = np.degrees(cosa * xc - sina * yc)
        ycd = np.degrees(sina * xc + cosa * yc)

        xr = (X - xcd)
        yr = (Y - ycd)
        xr = xr.reshape(xg.shape)
        yr = yr.reshape(yg.shape)

        zti = griddata(newp, newm, (xr, yr), method='linear', fill_value=SMALL)

        #         apod = np.sqrt(zti/zti.max())
        apod = zti / zti.max()
    return apod


def draw_apod(fov_meth, levels=None, grid_hwid=3.0):
    M = 81
    xgrid = getGrid(M, np.radians(grid_hwid))
    xm, ym = np.meshgrid(xgrid, xgrid)
    apod = apodizePAF(xgrid, fov_method=fov_meth)
    xymax = np.where(apod == apod.max())
    xmax = xm[xymax[0][0], xymax[1][0]]
    ymax = ym[xymax[0][0], xymax[1][0]]

    if levels:
        levs = levels
    else:
        levs = [0.95 * 0.9 ** p for p in range(8)]
    CS = plt.contour(np.degrees(xm), np.degrees(ym), apod, levels=levs)
    plt.clabel(CS, CS.levels, inline=True, fmt="%4.2f", fontsize=10)
    plt.plot([xmax], [ymax], '+', ms=20)


"""
Define PAF map routines
"""


# def make_paf_map(c0, beams, sefds=None):
#     # Expect Matrix C0, the normalised covariance matrix (computed from model beam weights in calCov)
#     #        beams[M,M,Nb] being the power response of each beam on an MxM grid.
#     #   If sefds is defined, it is an array of measured SEFD values (in Jy) in beam order.
#     # Returns  PAF map s in signal variance.
#     #        s is for the given beam covariance matrix
#     M = beams.shape[1]
#     Nb = beams.shape[0]
#     W = np.matrix([1.0] * Nb).transpose()
#     WT = W.transpose()
#
#     if sefds is None:
#         # var = 1900.0 ** 2
#         var = 1.0 ** 2
#         v = np.array([var] * Nb)
#     else:
#         v = sefds ** 2
#
#     C = np.matrix(np.zeros([Nb, Nb]))
#
#     for i in range(Nb):
#         for j in range(Nb):
#             C[i, j] = c0[i, j] * np.sqrt(v[i] * v[j])
#
#     C1 = np.matrix(np.zeros([Nb, Nb]))
#
#     s = np.zeros([M, M])
#     for p in range(M):
#         for q in range(M):
#             for i in range(Nb):
#                 for j in range(Nb):
#                     C1[i, j] = C[i, j] / (beams[i, p, q] * beams[j, p, q])
#             Ci = np.linalg.inv(C1)
#             # si = (WT * Ci * W) ** -1
#             si = Ci.sum() ** -1
#             s[p, q] = si
#     # The following step is necessary to supress negative values that can appear around the edge
#     # of the field, presumably from numerically extreme values that violate assumptions about the
#     # floating point arithmetic.
#     s[s < 0.0] = s.max()
#     return s

def make_paf_map(cov, beams, sefds=None):
    """
    Generate a sensitivity map over the PAF field of view
    :param cov: the normalised covariance matrix (computed from model beam weights in calCov)
    :param beams: the power response of each beam on an MxM grid; shape = (Nb, M, M)
    :param sefds: If  defined, is an array of measured SEFD values (in Jy) in beam order.
    :return: s: the variance across the smae grid defined in beams.
    """

    M = beams.shape[1]
    Nb = beams.shape[0]

    if sefds is None:
        var = 1.0
        v = np.array([var]*Nb)
    else:
        v = sefds**2

    C = np.matrix(np.zeros([Nb, Nb]))

    for i in range(Nb):
        for j in range(Nb):
            C[i, j] = cov[i, j]*np.sqrt(v[i]*v[j])

    covi = np.linalg.inv(C)
    s = np.zeros([M, M])
    for p in range(M):
        for q in range(M):
            b = beams[:, p, q].T
            si = 1.0/np.dot(b.T, np.dot(covi, b).T)
            s[p, q] = si
    s[s<0.0] = s.max()
    return s


# def makePAFmap2(C0, beams):
#     # Expect Matrix C0, the normalised covariance matrix (computed from model beam weights in calCov)
#     #        beams[M,M,Nb] being the powe response of each beam on an MxM grid.
#     # Returns two PAF maps, s and t in signal variance.
#     #        t is for no correlation between beams
#     #        s is for the given beam covariance matrix
#     M = beams.shape[1]
#     Nb = beams.shape[0]
#     W = np.matrix([1.0] * Nb).transpose()
#     D0 = np.diag([1.0] * Nb)
#
#     v = np.array([1.0] * Nb)
#     C = np.matrix(np.zeros([Nb, Nb]))
#     D = np.matrix(np.zeros([Nb, Nb]))
#
#     for i in range(Nb):
#         D[i, i] = D0[i, i] * v[i]
#         for j in range(Nb):
#             C[i, j] = C0[i, j] * np.sqrt(v[i] * v[j])
#
#     C1 = np.matrix(np.zeros([Nb, Nb]))
#     D1 = np.matrix(np.zeros([Nb, Nb]))
#
#     s = np.zeros([M, M])
#     t = np.zeros([M, M])
#     for p in range(M):
#         for q in range(M):
#             for i in range(Nb):
#                 for j in range(Nb):
#                     C1[i, j] = C[i, j] / (beams[i, p, q] * beams[j, p, q])
#                     D1[i, j] = D[i, j] / (beams[i, p, q] * beams[j, p, q])
#             Ci = np.linalg.inv(C1)
#             si = (W.transpose() * Ci * W) ** -1
#             s[p, q] = si
#
#             Di = np.linalg.inv(D1)
#             ti = (W.transpose() * Di * W) ** -1
#             t[p, q] = ti
#
#     return s, t


class pafmap(object):
    def __init__(self, freq, xgrid, pitch):
        # xgrid - 1D grid used to form 2D map
        # fwhm - beam full width at half max
        # fpname - footprint name
        # pitch - beam separation
        # freq - frequency (MHz)
        #
        # All angles in radians.
        #
        # self.fpname = fpname
        self.xg = xgrid
        self.nx = self.xg.shape[0]
        self.nx2 = self.nx / 2
        self.dx = xgrid[1] - xgrid[0]
        self.da = self.dx ** 2
        self.area = self.da * self.nx ** 2
        # self.fwhm = fwhm
        self.pitch = pitch
        # self.pif = pitch / fwhm
        self.freq = freq
        self.hx = max(2, int(self.pitch / self.dx / 2 + 0.5))
        self.maps = []
        self.offsets = []
        self.ripple = []
        self.eqArea = []
        self.centroids = []
        self.mosaic = None
        self.mosaic_ripple = 0.0
        self.mosaic_centroid = []
        self.areaContour = 0.0
        self.equivArea = 0.0
        self.survey_params = []

    def addmap(self, var, offsets):
        # expects the variance map and the footprint interleaving offsets
        self.maps.append(var)
        self.offsets.append(offsets)
        xc, yc = self._calcCentroid(var)
        self.centroids.append((xc, yc))
        # for ripple calculation, centre the region on the footprint centre
        # xc,yc = offsets
        ixc, iyc = int(xc + 0.5), int(yc + 0.5)
        ix, jx = max(0, ixc - self.hx), min(self.nx, ixc + self.hx)
        iy, jy = max(0, iyc - self.hx), min(self.nx, iyc + self.hx)

        cen = np.sqrt(1.0 / var[iy:jy, ix:jx])
        ri = (cen.max() - cen.min()) / cen.mean()
        self.ripple.append(ri)
        iv = 1.0 / var
        self.eqArea.append(iv.sum() / iv.max() * self.da)

    def makeLinMos(self):
        Ni = len(self.maps)
        denom = 1.0 / self.maps[0]
        for s in self.maps[1:]:
            denom += 1.0 / s
        self.mosaic = Ni / denom
        xc, yc = self._calcCentroid(self.mosaic)
        self.mosaic_centroid = (xc, yc)

        # for ripple calculation of the mosaic, use the calculated centroid for the region
        ixc, iyc = int(xc + 0.5), int(yc + 0.5)
        ix, jx = max(0, ixc - self.hx), min(self.nx, ixc + self.hx)
        iy, jy = max(0, iyc - self.hx), min(self.nx, iyc + self.hx)
        # note ordering of indices (y,x) is correct for np arrays
        cen = np.sqrt(1.0 / self.mosaic[iy:jy, ix:jx])
        self.mosaic_ripple = (cen.max() - cen.min()) / cen.mean()
        mosiv = 1.0 / self.mosaic
        moscut = mosiv.max() / np.sqrt(2.0)
        mmosiv = np.ma.masked_array(mosiv, mosiv < moscut)
        self.areaContour = mmosiv.count() * self.da
        self.equivArea = mosiv.sum() / mosiv.max() * self.da

    def getRipple(self):
        return self.ripple, self.mosaic_ripple

    def getSS(self, sigma=1.0e-4, BW=288.e6, Na=36, npol=2):
        # return survey speed in sq deg/hour for the given parmeters:
        # sigma - target image rms (Jy)
        # BW - bandwidth (Hz)
        # Na - number of antennas
        # npol - number of polarizations
        ssFac = BW * npol * Na ** 2 * sigma ** 2 * 3600.
        saFac = self.da * (180.0 / pi) ** 2 * ssFac
        self.survey_params = [sigma, BW, Na, npol]
        return (1.0 / self.maps[0]).sum() * saFac

    def get_survey_params(self):
        return self.survey_params

    # def get_sa_fac(self, sigma=1.0e-4, BW=300.e6, Na=30, npol=2):
    #     # return survey speed in sq deg/hour for the given parmeters:
    #     # sigma - target image rms (Jy)
    #     # BW - bandwidth (Hz)
    #     # Na - number of antennas
    #     # npol - number of polarizations
    #     ssFac = BW * npol * Na ** 2 * sigma ** 2 * 3600.
    #     saFac = self.area * (180.0 / pi) ** 2 * ssFac
    #     return saFac

    def getContArea(self):
        return self.areaContour * (180.0 / pi) ** 2

    def _calcCentroid(self, var):
        nx, nx2 = self.nx, self.nx2
        isig = np.sqrt(1.0 / var)
        xfunc = isig.mean(axis=0)
        yfunc = isig.mean(axis=1)
        cntx = (xfunc * np.arange(0, nx, 1)).sum() / xfunc.sum()
        cnty = (yfunc * np.arange(0, nx, 1)).sum() / yfunc.sum()
        if np.isnan(cntx) or np.isnan(cnty):
            print (var.min(), var.max())
        return cntx, cnty

    @staticmethod
    def _findPeak(var):
        """

        :param var:
        :return:
        """
        xy = np.where(var == var.min())
        cntx = xy[0][0]
        cnty = xy[1][0]
        return cntx, cnty


def makeCircle(rad, x0, y0):
    th = np.arange(0, 361, 1) * pi / 180
    x = x0 + rad * np.cos(th)
    y = y0 + rad * np.sin(th)
    return x, y


def drawFootprint(fp, beamWid, gridHWid, labels=None):
    # fp - footprint object
    # beamWid in degrees
    # gridHWis in degrees
    labels = labels or []
    doLabel = False
    if len(labels) == fp.n_beams:
        doLabel = True
    radius = beamWid / 2.0
    for i in range(fp.n_beams):
        x0, y0 = fp.offsetsRect[i] * 180 / pi
        x0 *= -1.0
        # todo: check why y0 is not sign reversed here
        x, y = makeCircle(radius, x0, y0)
        plt.plot(x, y, '-k', lw=0.5)
        plt.grid()
        plt.text(x0, y0, "%d" % i, va='center', ha='center', fontsize=7)
        if doLabel:
            plt.text(x0, y0 - radius * 0.5, labels[i], va='center', ha='center', fontsize=7)
    for i, p in enumerate(fp.interOffsRect):
        x0, y0 = p * 180 / pi
        r0 = np.sqrt(x0 * x0 + y0 * y0)
        if r0 > 0.0:
            plt.plot([x0], [y0], 'ok', ms=3.0)
            plt.plot([x0], [y0], 'o', mec='k', mfc='none', ms=6.0)
            hw, hl = 0.1, 0.1
            hlf = hl / r0
            plt.arrow(0.0, 0.0, x0 * (1.0 - hlf), y0 * (1.0 - hlf), head_width=hw, head_length=hl, )
    plt.plot([0.0], [0.0], '+k')
    plt.xlim(-gridHWid, gridHWid)
    plt.ylim(-gridHWid, gridHWid)


def draw_footprint_il(fp, beam_wid, grid_hwid, labels=None):
    # fp - footprint object
    # beamWid in degrees
    # gridHWis in degrees
    labels = labels or []
    ax = plt.gca()
    doLabel = False
    if len(labels) == fp.n_beams:
        doLabel = True
    radius = beam_wid / 2.0
    # IL = 0
    cols = ['w', 'b', 'y', 'r']
    for i in range(fp.n_beams):
        x0, y0 = fp.offsetsRect[i] * 180 / pi
        x0 *= -1.0
        # todo: check why y0 is not sign reversed here
        circle = plt.Circle((x0, y0), radius, color=cols[0], alpha=0.5)
        ax.add_artist(circle)
        x, y = makeCircle(radius, x0, y0)
        plt.plot(x, y, '-k', lw=0.5)
        plt.grid()
        plt.text(x0, y0, "%d" % i, va='center', ha='center', fontsize=7)
        if doLabel:
            plt.text(x0, y0 - radius * 0.5, labels[i], va='center', ha='center', fontsize=7)
    for j, p in enumerate(fp.interOffsRect):
        for i in range(fp.n_beams):
            x0, y0 = (p + fp.offsetsRect[i]) * 180 / pi
            x0 *= -1.0
            # todo: check why y0 is not sign reversed here
            circle = plt.Circle((x0, y0), radius, color=cols[j + 1], alpha=0.25)
            ax.add_artist(circle)
            x, y = makeCircle(radius, x0, y0)
            plt.plot(x, y, '-k', lw=0.5)
            plt.grid()
            plt.text(x0, y0, "%d" % i, va='center', ha='center', fontsize=7)
            if doLabel:
                plt.text(x0, y0 - radius * 0.5, labels[i], va='center', ha='center', fontsize=7)
    # plt.plot([0.0],[0.0],'+k')
    # rmax = fp.offsetsPolar[:, 0].max() * 180 / pi + radius
    plt.xlim(-grid_hwid, grid_hwid)
    plt.ylim(-grid_hwid, grid_hwid)


def ASKAP_SEFD(freq):
    # Evaluate the polynomial approximation to measured SEFD for ASKAP (on boresight) for any frequency
    # in the range [700, 1800] MHz.
    # The argument can be a scalar or an ndarray.
    # The SEFD is returned in Jy, as a scalar or ndarray according to the input.
    tsys = ASKAP_tsys_on_eff(freq)
    SEFD = tsys * (1380.0 * 2) / 113.1
    return SEFD


def ASKAP_tsys_on_eff(freq):
    # Evaluate the polynomial approximation to measured Tsys/eff for ASKAP (on boresight) for any frequency
    # in the range [700, 1800] MHz.
    # The argument can be a scalar or an ndarray.
    # The Tsys/eff is returned in K, as a scalar or ndarray according to the input.

    # The following line is written by the fitting routine in python notebook SEFD/full_spectrum
    coeff = [5.18075082126351e-34, -6.766881661087157e-30, 3.8245980771420834e-26,
             -1.1889614543042915e-22, 2.0255289080361158e-19, -1.0077294751671198e-16,
             -3.687374327312008e-13, 1.0505041199723573e-09, -1.4531507807579093e-06,
             0.0012726466808857277, -0.737013079528667, 275.33155694172655, -60388.60533807194,
             5926644.561754142]
    tsys = np.polyval(coeff, freq)
    return tsys


# Define pafmap class, subXaxis and 2d interp for guessing best pitch.


def subXaxis(ax1, scale, label):
    ax2 = ax1.twiny()
    #     pitch = np.degrees(fwhm*np.array(pif))

    pift = np.array(ax1.get_xticks())
    pitcht = ["%4.2f" % a for a in pift * scale]
    # Move twinned axis ticks and label from top to bottom
    ax2.xaxis.set_ticks_position("bottom")
    ax2.xaxis.set_label_position("bottom")

    # Offset the twin axis below the host
    ax2.spines["bottom"].set_position(("axes", -0.15))

    # Turn on the frame for the twin axis, but then hide all
    # but the bottom spine
    ax2.set_frame_on(True)
    ax2.patch.set_visible(False)
    for sp in ax2.spines.values():
        sp.set_visible(False)
    ax2.spines["bottom"].set_visible(True)

    ax2.set_xticks(pift)
    ax2.set_xticklabels(pitcht)
    ax2.set_xlabel(label)
    # ax2.set_xlim(xl, xu)


# def find_best_pitch(fpname, xg, freqs, pitchesf, fov_meth, **kw):
#
#     pitchesf = np.array(pitchesf)
#     ret = {}
#     tune_interp = {}
#     for freq, pitches in zip(freqs, pitchesf):
#         fwhm = empiricalFWHM(freq)
#         print ("Freq = {:6.1f},  FWHM = {:5.2f} deg".format(freq, np.degrees(fwhm)))
#         spds = []
#         for pitch in pitches:
#             fp = fp_factory.make_footprint(fpname, np.radians(pitch))
#             offsets = np.array(fp.offsetsRect)
#
#             ioff = np.array([0., 0.])
#             pmap = pafmap(xg, freq)
#             abeams = makeBeams(xg, offsets, fwhm)
#             C0 = cv_modelled(offsets, fwhm)
#             # C0 = calcCov(abeams)
#             apod = apodizePAF(xg, fov_method=fov_meth)
#             beams = apod * abeams ** 2
#             beams[beams == 0.0] = 1.0e-6
#             s = make_paf_map(C0, beams)
#             pmap.addmap(s, ioff)
#             pmap.makeLinMos()
#             spds.append(pmap.getSS(**kw))
#         spds = np.array(spds)
#         fp = interp1d(pitches, spds, kind='cubic')
#         pfine = np.linspace(pitchesf.min(), pitchesf.max(), 50)
#         mfine = fp(pfine)
#         ipk = np.where(mfine == mfine.max())[0][0]
#         ret[freq] = pfine[ipk]
#         tune_interp[freq] = (pfine, mfine)
#     return ret, tune_interp


def find_best_pitch(fpname, freq, fov_meth):
    # print ("find_best_pitch")
    fp = fp_factory.make_footprint(fpname, 0.01)
    n1 = np.sqrt(fp.n_beams)
    fwhm = empiricalFWHM(freq)

    # pitch0 = estimate_pitch(fpname, freq)
    # lolim, hilim = 0.7 * pitch0, 1.3 * pitch0
    # lolim = max(lolim, fwhm/3.0)
    lolim, hilim = 0.65, 1.3
    pitches = np.array([lolim, hilim])
    M = 81
    grid_size = np.radians(7.0)
    xg = getGrid(M, grid_size)
    ret = {}
    tune_interp = {}

    k = 0
    p1, p3 = np.radians(pitches)
    dp = p3 - p1
    p2 = (p1 + p3)/2.
    xp = np.array([])
    yp = np.array([])
    while k < 3:
        k += 1
        ea1 = get_eq_area(fpname, p1, freq, xg, fov_meth)
        ea2 = get_eq_area(fpname, p2, freq, xg, fov_meth)
        ea3 = get_eq_area(fpname, p3, freq, xg, fov_meth)
        xp = np.concatenate((xp, [p1, p2, p3]))
        yp = np.concatenate((yp, [ea1, ea2, ea3]))
        c, b, a = fit_parabola(xp, yp)
        p2 = -b / (2.0 * a)
        print ('new peak at ', p2 * 180.0 / pi)
        dp /= 2.0
        p1, p3 = p2 - dp / 2, p2 + dp / 2.

    xp *= 180.0/np.pi
    snx = np.argsort(xp)
    # print xp
    # print xp[snx]
    fp = interp1d(xp[snx], yp[snx], kind='cubic')
    pfine = np.linspace(pitches[0], pitches[1], 50)
    mfine = fp(pfine)
    ipk = np.where(mfine == mfine.max())[0][0]
    ret[freq] = pfine[ipk]
    tune_interp[freq] = (pfine, mfine)
    fig, ax = plt.subplots(1, 1)
    ax.plot(pfine, mfine)
    ax.plot(xp, yp, 'o')
    fig.savefig('bp{:.0f}.png'.format(freq))
    return ret, tune_interp


def get_eq_area(fpname, pitch, freq, xg, fov_meth):
    # print ("****** get_eq_area")
    # print (fpname, pitch*180.0/np.pi, freq, xg.shape, fov_meth)
    tiny = 1.0e-9

    fp = fp_factory.make_footprint(fpname, pitch)
    fwhm = empiricalFWHM(freq)
    offsets = np.array(fp.offsetsRect)

    ioff = np.array([0., 0.])
    pmap = pafmap(freq, xg, fp.pitch_scale)
    abeams = makeBeams(xg, offsets, fwhm)
    # C0 = cv_modelled(offsets, fwhm)
    C0 = calcCov(abeams)
    apod = apodizePAF(xg, fov_method=fov_meth)
    beams = apod * abeams ** 2 + tiny
    # beams[beams < 1.0e-6] = 1.0e-6
    s = make_paf_map(C0, beams)
    pmap.addmap(s, ioff)
    pmap.makeLinMos()
    # print (freq, pitch*180.0/np.pi, pmap.equivArea)
    return pmap.equivArea


def estimate_pitch(fpname, freq):
    nb = fp_factory.make_footprint(fpname, 1.0 * pi / 180.).n_beams
    est = np.sqrt(32./nb)
    est = 1.0
    return est


def calcSummary(fpname, freq, fov_meth, **kw):
    tmr = Timer()

    bp, tune_intp = find_best_pitch(fpname, freq, fov_meth)
    bestPitch = bp[freq]
    print ("{:5.2f}  {:6.2f}s".format(bestPitch, tmr.getDelta()))

    pitch = np.radians(bestPitch)
    fp = fp_factory.make_footprint(fpname, pitch)
    iOffsets = np.vstack((np.array([[0.0, 0.0]]), fp.interOffsRect))
    Nb = fp.n_beams
    offsets = np.array(fp.offsetsRect)
    fwhm = empiricalFWHM(freq)

    grid_size = fp.tile_offsets[0][0] + fwhm/2.
    M = 121
    xg = getGrid(M, grid_size)

    sefd = ASKAP_SEFD(freq)
    sefds = np.array([sefd] * Nb)

    pmap = pafmap(freq, xg, pitch)
    for i, ioff in enumerate(iOffsets):
        offsets_i = offsets + ioff
        abeams = makeBeams(xg, offsets_i, fwhm)

        # C0 = cv_modelled(offsets_i, fwhm)
        C0 = calcCov(abeams)

        apod = apodizePAF(xg, centre=ioff, fov_method=fov_meth)
        fig, ax = plt.subplots(1, 1, figsize=(6., 6.))
        ax.imshow(apod, origin='lower')
        fig.savefig("temp_apod_{:d}.pdf".format(i))
        # print ("apod range {:f} {:f}".format(apod.min(), apod.max()))
        beams = apod * abeams ** 2
        beams[beams < 1.0e-6] = 1.0e-6
        fig, ax = plt.subplots(6, 6, figsize=(6., 6.))
        for j, axi in zip(range(36), ax.flat):
            axi.imshow(beams[j], origin='lower')
        fig.savefig("temp_beams_{:d}.pdf".format(i))
        # print ("beams range {:f} {:f}".format(beams.min(), beams.max()))

        s = make_paf_map(C0, beams, sefds=sefds)
        fp_off = np.array([bsect(xg, ioff[0]), bsect(xg, ioff[1])])
        pmap.addmap(s, fp_off)
    pmap.makeLinMos()
    # print ("equiv area {:.2f}".format(pmap.equivArea*(180.0/np.pi)**2))
    surveySpeed = pmap.getSS(**kw)

    do_unit = False
    if do_unit:
        pmapU = pafmap(freq, xg, pitch)
        for i, ioff in enumerate(iOffsets):
            offsets_i = offsets + ioff
            abeams = makeBeams(xg, offsets_i, fwhm)

            # C0 = cv_modelled(offsets_i, fwhm)
            C0 = calcCov(abeams)

            apod = apodizePAF(xg, centre=ioff, unit=True, fov_method=fov_meth)
            beams = apod * abeams ** 2
            beams[beams < 1.0e-6] = 1.0e-6
            s = make_paf_map(C0, beams, sefds=sefds)
            fp_off = np.array([bsect(xg, ioff[0]), bsect(xg, ioff[1])])
            pmapU.addmap(s, fp_off)
            # print ("{:.2f} {:d}  {:6.2f}s".format(pitch*180.0/np.pi, i, tmr.getDelta()))
        pmapU.makeLinMos()
    else:
        pmapU = pmap

    # Now compute a tiled mosaic from four interleaved observations. This is to show the level of FoV
    # ripple.

    tp = fp.tile_offsets
    if len(tp) < 2:
        tp = np.array([1.0,1.0])*bestPitch*6*pi/180.0
    xshift, yshift = tp[0][0], tp[1][1]
    v0 = pmap.mosaic
    m = 1./v0
    f2 = interp2d(xg, xg, m, kind='cubic')
    xh = getGrid(161,np.radians(10))
    u1 = f2(xh+xshift/2.,xh+yshift/2.)
    u2 = f2(xh-xshift/2.,xh+yshift/2.)
    u3 = f2(xh-xshift/2.,xh-yshift/2.)
    u4 = f2(xh+xshift/2.,xh-yshift/2.)
    tol = 1.0e-12
    u1[u1<tol] = tol
    u2[u2<tol] = tol
    u3[u3<tol] = tol
    u4[u4<tol] = tol

    vmos = (u1 + u2 + u3 + u4)
    smos = np.sqrt(vmos)

    print ('Equiv area        : ', pmap.equivArea * (180.0/np.pi)**2)
    print ('Eq area           : ', pmap.eqArea[0] * (180.0/np.pi)**2)
    print ('ripple            : ', pmap.ripple, pmapU.ripple)
    print ('ripple (mosaiced) : ', pmap.mosaic_ripple, pmapU.mosaic_ripple)
    return pmap, pmapU, fp, bestPitch, smos, tune_intp, surveySpeed


def plotFootprint(pmap, fpname, fp, best_pitch, fov_m):
    freq = pmap.freq

    contour = False
    cmap = 'jet'

    plt.clf()
    fig = plt.gcf()
    fwid = 8.5
    fht = 2.9
    fig.set_size_inches([fwid, fht])
    plt.subplots_adjust(wspace=0.12)
    ax1 = fig.add_subplot(1, 3, 1)
    ax2 = fig.add_subplot(1, 3, 2)
    ax3 = fig.add_subplot(1, 3, 3)
    #     ax4 = fig.add_subplot(1,4,4)

    ax1.set_aspect('equal')
    plt.sca(ax1)
    gridHW = 3.5
    drawFootprint(fp, best_pitch, gridHW)
    draw_apod(fov_m, levels=[0.7071], grid_hwid=gridHW)
    plt.xlabel('degrees')
    plt.ylabel('degrees')
    plt.title(fpname)

    the_map = pmap.maps[0]
    xd = np.degrees(pmap.xg)
    ext = [xd[0], xd[-1], xd[0], xd[-1]]

    plt.sca(ax2)
    y = np.sqrt(1.0 / the_map)
    vma = y.max()
    vmi = vma / root2 / root2
    plt.imshow(y, origin='lower', extent=ext, vmin=vmi, vmax=vma, cmap=cmap)
    plt.xlim(gridHW, -gridHW)
    plt.ylim(-gridHW, gridHW)
    plt.xlabel('degrees')

    plt.setp(ax2.get_yticklabels(), visible=False)

    y = np.sqrt(1.0 / pmap.mosaic)
    vma = y.max()
    vmi = vma / root2 / root2
    ax3.set_aspect('equal')
    plt.sca(ax3)
    if not contour:
        plt.imshow(y, origin='lower', extent=ext, vmin=vmi, vmax=vma, cmap=cmap)
    plt.xlim(-gridHW, gridHW)
    plt.ylim(-gridHW, gridHW)
    plt.xlabel('degrees')
    plt.setp(ax3.get_yticklabels(), visible=False)
    if contour:
        y /= vma
        levs = np.logspace(np.log10(1.0 / root2), 0.0, 8)
        #     levs = np.array([1.0, 0.92, 0.8464, 0.778688, 0.716392])
        plt.contourf(xd, xd, y, levels=levs, alpha=.75, cmap='Blues')
        c = plt.contour(xd, xd, y, levels=levs[::3], colors='k')
        plt.clabel(c, c.levels, inline=True, fmt="%4.2f", fontsize=10)

    # titl = "Footprint: %s     f = %6.1f MHz" % (fpname, freq)
    fname = "summary_%s_%d.pdf" % (fpname, int(freq))
    plt.savefig(fname)
    print ("Saved plot file ", fname)
    del fig


def plot_opt(suffix):
    files = glob.glob("results_ak:*{}.pkl".format(suffix))
    files += glob.glob("results_xx:*{}.pkl".format(suffix))
    tmp = [a[8:-4] for a in files]
    fps = []
    for f in tmp:
        if f.endswith(suffix):
            j = f.index(suffix)
            fps.append(f[:j])
        else:
            fps.append(f)
    print (fps)
    ssScale = 1.0

    cols = {'ak:square_6x6': 'k', 'xx:square_8x8': 'b', 'ak:closepack36': 'r', 'closepack30': 'g', 'rectangle_6x6': 'b',
            'xx:closepack70': 'g', 'xx:closepack56': 'c'}
    mrkr = {'ak:square_6x6': 's', 'xx:square_8x8': 's', 'ak:closepack36': 'h', 'closepack30': 'h', 'rectangle_6x6': 'd',
            'xx:closepack70': 'h', 'xx:closepack56': 'h'}
    msize = 4
    for k in fps:
        if k not in cols:
            cols[k] = '0.5'
            mrkr[k] = 'x'

    labs = {'bp': ['Best pitch', '\n', '(deg)'], 'ss': ['Survey speed', '\n', '(sq deg/hr)'],
            'ri': ['Interleaved ripple'], 'ea': ['Equivalent area', '\n', '(sq deg)'],
            'eq': ['Equivalent area', '\n', '(sq deg)'],
            'rr': ['Ripple'], 'tr': ['Tile ripple']}
    # pfunc = {'bp': ax.plot, 'ss': plt.plot, 'ri': plt.plot, 'ea': plt.plot, 'eq': plt.plot, 'rr': plt.plot}
    # vks = ['bp', 'ss', 'eq', 'rr', 'ri', 'tr']
    vks = ['bp', 'ss', 'eq', 'rr', 'ri']
    # iknd = {'bp':'cubic','ss':'cubic','ri':'linear','ea':'cubic'}

    ny = len(vks)
    fig, axes = plt.subplots(ny, 1, figsize=[7., 12.])
    fig.subplots_adjust(wspace=0.65, hspace=0.05)
    for ax in axes.flat:
        ax.label_outer()
    for vk, ax in zip(vks, axes.flat):
        # ax.grid()
        for fpn in fps:
            j = fpn.index(':')+1
            flab = fpn[j:]
            col = cols[fpn]
            mk = mrkr[fpn]
            fpname, resf = pickle.load(open("results_{}{}.pkl".format(fpn, suffix), 'rb'))
            frs = []
            vals = []
            for fr in resf.keys():
                res = resf[fr]
                frs.append(fr)
                if vk == 'rr':
                    vals.append(res[vk][0])
                else:
                    vals.append(res[vk])
            z = zip(frs, vals)
            z.sort()
            frs = np.array([a[0] for a in z])
            vals = np.array([a[1] for a in z])
            #         if vk == 'bp':
            #             fwhm = 300./frs/12.*1.12 * 180./np.pi
            #             vals = vals/fwhm
            if vk == 'ss':
                vals = vals * ssScale
            print ("%16s" % fpn, vk, frs, vals)
            fn = interp1d(frs, vals, kind='quadratic')
            frf = np.linspace(frs[0], frs[-1], 100)
            vf = fn(frf)
            if vk == 'ri' or vk == 'xrr':
                ax.plot(frs, vals, '-', marker=mk, ms=msize, c=col, label=flab)
            else:
                ax.plot(frf, vf, '-', c=col)
                ax.plot(frs[:-1], vals[:-1], marker=mk, ms=msize, ls='none', c=col, label=flab)
        ax.set_xlim(680, 1805)
        ax.grid()
        ax.set_ylabel(' '.join(labs[vk]))
        if vk == vks[-1]:
            ax.set_xlabel('Frequency (MHz)')
        if vk == vks[0]:
            ax.legend(loc='center left', fontsize=10, bbox_to_anchor=(0.75, 0.75))
        if vk == 'ss' and 'sp' in res:
            sp = res['sp']
            sig, bw, na, npol = sp
            x, y = 1580., 200.
            dy = y/10.
            ax.text(x, y, "BW = {:.0f} MHz".format(bw * 1.e-6))
            ax.text(x, y-dy, "{:d} antennas".format(na))
            ax.text(x, y-dy*2, "{:d} polarizations".format(npol))
            ax.text(x, y-dy*3, r'$\sigma$ = {:.3f} mJy'.format(sig * 1.e3))

        ax.yaxis.set_label_coords(-0.075, 0.5)
    pname = 'optimisedVals{}.pdf'.format(suffix)
    fig.savefig(pname, dpi=300)
    print ('Plotted to {}'.format(pname))


def plot_pitch_tuning(suffix):
    files = glob.glob("results_ak:*{}.pkl".format(suffix))
    files += glob.glob("results_xx:*{}.pkl".format(suffix))
    tmp = [a[8:-4] for a in files]
    fps = []
    for f in tmp:
        if f.endswith(suffix):
            j = f.index(suffix)
            fps.append(f[:j])
        else:
            fps.append(f)
    cols = {'ak:square_6x6': 'k', 'xx:square_8x8': 'b', 'ak:closepack36': 'r', 'xx:closepack56': 'c', 'xx:closepack70': 'g'}
    lwi = {'ak:square_6x6': 1.5, 'xx:square_8x8': 1.3, 'ak:closepack36': 1.5, 'xx:closepack56': 1.3, 'xx:closepack70': 1.3}

    tuning = {}
    xlim = [100., 0.]
    ylim = [100., 0.]
    freqs = []
    for fpn in fps:
        fpname, resf = pickle.load(open("results_{}{}.pkl".format(fpn, suffix), 'rb'))
        freqs = sorted(resf.keys())[:-1:2]
        dat = {}
        dat['freq'] = freqs
        xexs, yexs = [], []
        for frq in freqs:
            xex = resf[frq]['ex'][frq][0]
            yex = resf[frq]['ex'][frq][1]
            xexs.append(xex)
            yexs.append(yex)
            xlim[0] = min(xlim[0], xex.min())
            xlim[1] = max(xlim[1], xex.max())
            ylim[0] = min(ylim[0], yex.min())
            ylim[1] = max(ylim[1], yex.max())

        dat['xex'] = xexs
        dat['yex'] = yexs
        tuning[fpn] = dat
    for k in tuning.keys():
        if k not in cols:
            cols[k] = '0.5'
            lwi[k] = 1.0
    ylims = {}
    ymin = 1.0e3
    ymax = 0.0
    for fp in fps:
        for i, frq in enumerate(freqs):
            ymin = min(ymin, tuning[fp]['yex'][i].min())
            ymax = max(ymax, tuning[fp]['yex'][i].max())
            ylims[frq] = [ymin, ymax]

    fpnames = tuning.keys()
    ny, nx = (len(freqs)+1)/2, 2
    fig, axes = plt.subplots(ny, nx, figsize=(8., 5.))
    axt = axes.transpose()
    fig.subplots_adjust(wspace=0.02, hspace=0.03)
    for i, (frq, ax) in enumerate(zip(freqs, axt.flat)):
        for fp in fpnames:
            j = fp.index(':')+1
            flab = fp[j:]
            xex = tuning[fp]['xex'][i]
            # yex = tuning[fp]['yex'][i] / ylims[frq][1]
            yex = tuning[fp]['yex'][i]
            yex /= yex.max()
            ax.plot(xex, yex, c=cols[fp], label=flab, lw=lwi[fp])
            # axes[0,0].plot(xex, yex, c=cols[fp], label=flab, lw=lwi[fp])
        ax.set_xlim(xlim[0], xlim[1])
        # ax.set_ylim(ylims[frq][0], ylims[frq][1])
        ax.set_ylim(0.7, 1.04)
        ax.grid()
        ax.set_xlabel('Pitch (deg)')
        ax.text(1.15, 0.75, "{:.0f} MHz".format(frq), ha='right', va='center')
        if i == 0:
            ax.set_ylabel('Relative' '\n' ' survey speed ', rotation='horizontal')
            ax.yaxis.set_label_coords(-0.05, 1.01)
    for ax in axt.flat:
        ax.label_outer()
    #     ax.set_title('Pitch tuning curve at %d MHz'%frq,loc='left')
    # ax.legend(loc='center left', fontsize=10, bbox_to_anchor=(0.45, 0.28))
    ax.legend()
    pname = 'pitch_tuning{}.pdf'.format(suffix)
    fig.savefig(pname, dpi=300)
    print ('Plotted to {}'.format(pname))


def main():
    # parse command line options
    print (announce)
    args = arg_init().parse_args()
    verbose = args.verbose

    if args.explain:
        print (explanation)
        sys.exit(0)
    if verbose:
        print ("ARGS = ", args)

    suffix = args.output_suffix
    if len(suffix) > 0:
        suffix = '_' + suffix

    fov_meth = args.fov_method
    do_calc = not args.plot_only

    fp_names = args.fpnames
    freqs = args.frequencies

    kw = {'sigma': 100.0e-6, 'BW': 288.e6, 'Na': 36}

    results = {}

    if do_calc:
        for fpname in fp_names:
            resf = {}
            pmaps = {}
            for freq in freqs:
                print (fpname, freq)
                pmap, pmapU, fp, bestPitch, smos, tune_interp, surveySpeed = calcSummary(fpname, freq, fov_meth, **kw)
                plotFootprint(pmap, fpname, fp, bestPitch, fov_meth)
                pmaps[freq] = pmap

                m = smos.shape[0]
                cmin = smos[m-10:m+10, m-10:m+10].min()
                smsk = np.ma.masked_array(smos, mask=(smos < cmin))

                res = {}
                res['fp'] = fpname
                res['fr'] = freq
                res['ss'] = surveySpeed
                res['bp'] = bestPitch
                res['ex'] = tune_interp
                res['ri'] = pmapU.mosaic_ripple
                res['rr'] = pmap.ripple
                res['eq'] = pmap.eqArea[0] * (180 / pi) ** 2
                res['ea'] = pmap.equivArea * (180 / pi) ** 2
                res['tr'] = smsk.std() / smsk.mean()
                res['sp'] = pmap.get_survey_params()
                resf[freq] = res
                plt.clf()
                plt.imshow(smos)
                plt.title("{} {}".format(fpname, freq))
                plt.savefig("smos_{:d}.png".format(int(freq)))
            results[fpname] = resf
            pname = "results_{}{}.pkl".format(fpname, suffix)
            pickle.dump((fpname, resf), open(pname, 'w'))

    plot_opt(suffix)
    plot_pitch_tuning(suffix)


if __name__ == "__main__":
    sys.exit(main())
