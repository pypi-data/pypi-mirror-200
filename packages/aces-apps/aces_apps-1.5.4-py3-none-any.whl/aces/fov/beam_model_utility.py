"""A set of utility routines for various beam modelling exercises"""

__author__ = 'Dave McConnell <david.mcconnell@csiro.au>'

import numpy as np

import scipy.special as ssp

import matplotlib.pylab as plt

import itertools

root2 = np.sqrt(2.0)
pi = np.pi


# todo : remove unused functions


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


def empirical_fwhm(freq):
    # return the empirically determined FWHM as a function of frequency in MHz.
    factor = 1.12
    diameter = 12.0
    fwhm = 299.8 / freq / diameter * factor
    return fwhm


def get_grid(M, w):
    xg = np.linspace(-w, w, M)
    return xg


def make_beams(xgrid, offsets, fwhm):
    # compute beam values on given grid
    # at offsets given
    # Produces voltage beams with the given FWHM once converted to power.
    wi = 1.368
    wia = wi * fwhm
    nb = offsets.shape[0]
    tbeams = None
    for i in range(nb):
        xci, yci = offsets[i]
        ai0 = airy2d(xgrid, xci, yci, wid=wia)
        if i == 0:
            tbeams = ai0
        else:
            tbeams = np.dstack((tbeams, ai0))
    if nb == 1:
        tbeams = np.expand_dims(tbeams, axis=2)
    abeams = np.transpose(tbeams, (2, 0, 1))
    return abeams


def calc_cov(abeams):
    Nb = abeams.shape[0]
    ra2 = None
    for i in range(Nb):
        psai = []
        ai0 = abeams[i, :, :]
        for j in range(Nb):
            aia = abeams[j, :, :]
            psai.append((ai0 * aia).sum())
        psai = np.array(psai)
        ra = psai ** 2 / (ai0 ** 2).sum() ** 2
        if i == 0:
            ra2 = ra
        else:
            ra2 = np.vstack((ra2, ra))
    cov = np.matrix(ra2)
    return cov


def apodize_paf_0(xgrid, centre=None, unit=False):
    # define an apodizing function that mimics the observed sensitivity variation across the PAF.
    # formed from quadratic fit, parameters in variable m
    # No other manipulation of the function is made; see routine apodize_paf.
    if centre is None:
        centre = [0.0, 0.0]
    if unit:
        apod = np.ones((xgrid.shape[0], xgrid.shape[0]))
    else:
        m = [5.68171268e-04, -2.42077280e-04, -2.78766255e-02, 2.68446142e-04,
             1.14317719e-03, -2.17087761e-01, -2.47329723e-02, 1.57161909e-01, -2.94909312e+01]
        x, y = np.meshgrid(xgrid, xgrid)
        xc, yc = centre
        xr = (x - xc) / root2 - (y - yc) / root2
        yr = (x - xc) / root2 + (y - yc) / root2

        apod = polyval2d(xr, yr, m)
        apod[apod < 0.0] = 0.0
        apod /= apod.max()
    return apod


def apodize_paf_posang_0(xgrid, centre=None, unit=False):
    # define an apodizing function that mimics the observed sensitivity variation across the PAF.
    # formed from quadratic fit, parameters in variable m
    # No 45deg rotation is applied.
    if centre is None:
        centre = [0.0, 0.0]
    if unit:
        apod = np.ones((xgrid.shape[0], xgrid.shape[0]))
    else:
        m = [5.68171268e-04, -2.42077280e-04, -2.78766255e-02, 2.68446142e-04,
             1.14317719e-03, -2.17087761e-01, -2.47329723e-02, 1.57161909e-01, -2.94909312e+01]
        x, y = np.meshgrid(xgrid, xgrid)
        xc, yc = centre
        xr = (x - xc)
        yr = (y - yc)

        apod = polyval2d(xr, yr, m)
        apod[apod < 0.0] = 0.0
        apod /= apod.max()
    return apod


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


def design_mat_2(X, Y, b):
    al = [X, Y]
    for f in [0.71, 1.0, 1.41, 2.0, 2.82]:
        b1 = f * b
        for i in [2, 4, 8]:
            al.append(fnc(X, b1, i) * fnc(Y, b1, i))
    A = np.array(al).T
    return A


def apodize_paf(xgrid, centre=None, posang=0.0, unit=False):
    # Define an apodizing function that mimics the observed sensitivity variation across the PAF.
    # formed from fit to a set of rational functions, parameters in variable m
    # Expects xgrid (in radians), centre and PA (position angle) both in radians.
    # Needs access to functions design_mat and fnc
    if centre is None:
        centre = [0.0, 0.0]

    if unit:
        apod = np.ones((xgrid.shape[0], xgrid.shape[0]))
    else:
        design_mat = design_mat_2
        # coeff = np.array([1.28107531e+01, 4.56911754e-01, 5.17826052e-01,-1.51419796e+02,-1.49542178e+01,
        #         -1.58078435e+00, 6.77485394e+02, 4.67563591e+01, -6.80814573e+00,-1.41500519e+03,
        #          1.23011095e+02, 4.87414906e+01,  1.10677965e+03,  -5.81216252e+02, 1.55424512e+02])

        coeff = np.array([5.09633567e-04, -6.67986801e-04, -1.53786901e+01, -1.90039866e+00,
                          -5.02886076e-01, 1.10132646e+02, 1.07159428e+01, 9.09866150e-01,
                          -3.56162780e+02, -1.44262434e+01, 3.35535219e+00, 6.17456821e+02,
                          -1.26227972e+02, -2.47940423e+01, -4.38376122e+02, 4.48199146e+02,
                          -2.12011984e+02])
        b = 3.84
        small_value = 1.0e-4
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

        A = design_mat(xr, yr, b)
        apod = np.reshape(np.dot(A, coeff), xg.shape)
        # trimming the pattern is done in fnc(x,a,e) with a hard coded value!
        rlim = np.radians(4.7)
        # xylim = np.radians(4.0)
        apod[(xg - xc) ** 2 + (yg - yc) ** 2 > rlim ** 2] = small_value
        apod[apod < 0.0] = small_value
        apod /= apod.max()
    return apod


def draw_apod(grid_wid=3.0, levels=None, plot_grid=False):
    M = 81
    xgrid = get_grid(M, np.radians(grid_wid))
    xm, ym = np.meshgrid(xgrid, xgrid)
    apod = apodize_paf(xgrid)
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
    if plot_grid:
        plt.grid()


# Define PAF map routines
def make_paf_map(cov, beams, sefds=None):
    # Expect Matrix C0, the normalised covariance matrix (computed from model beam weights in calCov)
    #        beams[Nb,M,M] being the power response of each beam on an MxM grid.
    #   If sefds is defined, it is an array of measured SEFD values (in Jy) in beam order.
    # Returns  PAF map s in signal variance.
    #        s is for the given beam covariance matrix
    M = beams.shape[1]
    Nb = beams.shape[0]

    if sefds is None:
        # var = 1900.0**2
        var = 1.0
        v = np.array([var] * Nb)
    else:
        v = sefds ** 2

    C = np.array(np.zeros([Nb, Nb]))

    for i in range(Nb):
        for j in range(Nb):
            C[i, j] = cov[i, j] * np.sqrt(v[i] * v[j])

    covi = np.linalg.inv(C)
    s = np.zeros([M, M])
    for p in range(M):
        for q in range(M):
            b = beams[:, p, q].T
            si = 1.0 / np.dot(b.T, np.dot(covi, b).T)
            s[p, q] = si
    return s


def make_paf_map2(C0, beams):
    # Expect Matrix C0, the normalised covariance matrix (computed from model beam weights in calCov)
    #        beams[M,M,Nb] being the powe response of each beam on an MxM grid.
    # Returns two PAF maps, s and t in signal variance.
    #        t is for no correlation between beams
    #        s is for the given beam covariance matrix
    M = beams.shape[1]
    Nb = beams.shape[0]
    W = np.array([1.0] * Nb).transpose()
    D0 = np.diag([1.0] * Nb)

    v = np.ones(Nb)
    C = np.array(np.zeros([Nb, Nb]))
    D = np.array(np.zeros([Nb, Nb]))

    for i in range(Nb):
        D[i, i] = D0[i, i] * v[i]
        for j in range(Nb):
            C[i, j] = C0[i, j] * np.sqrt(v[i] * v[j])

    C1 = np.array(np.zeros([Nb, Nb]))
    D1 = np.array(np.zeros([Nb, Nb]))

    s = np.zeros([M, M])
    t = np.zeros([M, M])
    for p in range(M):
        for q in range(M):
            for i in range(Nb):
                for j in range(Nb):
                    C1[i, j] = C[i, j] / (beams[i, p, q] * beams[j, p, q])
                    D1[i, j] = D[i, j] / (beams[i, p, q] * beams[j, p, q])
            Ci = np.linalg.inv(C1)
            si = (W.transpose() * Ci * W) ** -1
            s[p, q] = si

            Di = np.linalg.inv(D1)
            ti = (W.transpose() * Di * W) ** -1
            t[p, q] = ti

    return s, t


class pafmap(object):
    def __init__(self, xgrid, fwhm, fpname, pitch, freq):
        # xgrid - 1D grid used to form 2D map
        # fwhm - beam full width at half max
        # fpname - footprint name
        # pitch - beam separation
        # freq - frequency (MHz)
        #
        # All angles in radians.
        #
        self.fp_name = fpname
        self.xg = xgrid
        self.nx = self.xg.shape[0]
        self.nx2 = self.nx / 2
        self.dx = xgrid[1] - xgrid[0]
        self.da = self.dx ** 2
        self.area = self.da * self.nx ** 2
        self.fwhm = fwhm
        self.pitch = pitch
        self.pif = pitch / fwhm
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

    def addmap(self, var, offsets):
        # expects the variance map and the footprint interleaving offsets
        self.maps.append(var)
        self.offsets.append(offsets)
        xc, yc = self._calc_centroid(var)
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

    def make_lin_mos(self):
        Ni = len(self.maps)
        denom = 1.0 / self.maps[0]
        for s in self.maps[1:]:
            denom += 1.0 / s
        self.mosaic = Ni / denom
        xc, yc = self._calc_centroid(self.mosaic)
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

    def get_ripple(self):
        return self.ripple, self.mosaic_ripple

    def get_survey_speed(self, sigma=1.0e-4, bandwidth=300.e6, num_antennas=30, npol=2):
        # return survey speed in sq deg/hour for the given parmeters:
        # sigma - target image rms (Jy)
        # bandwidth - bandwidth (Hz)
        # Na - number of antennas
        # npol - number of polarizations
        ssFac = bandwidth * npol * num_antennas ** 2 * sigma ** 2 * 3600.
        saFac = self.area * (180.0 / pi) ** 2 * ssFac
        return (1.0 / self.mosaic).mean() * saFac

    def get_cont_area(self):
        return self.areaContour * (180.0 / pi) ** 2

    def _calc_centroid(self, var):
        nx, nx2 = self.nx, self.nx2
        isig = np.sqrt(1.0 / var)
        xfunc = isig.mean(axis=0)
        yfunc = isig.mean(axis=1)
        cntx = (xfunc * np.arange(0, nx, 1)).sum() / xfunc.sum()
        cnty = (yfunc * np.arange(0, nx, 1)).sum() / yfunc.sum()
        return cntx, cnty

    @staticmethod
    def _find_peak(var):
        xy = np.where(var == var.min())
        cntx = xy[0][0]
        cnty = xy[1][0]
        return cntx, cnty


def make_circle(rad, x0, y0):
    th = np.arange(0, 361, 1) * pi / 180
    x = x0 + rad * np.cos(th)
    y = y0 + rad * np.sin(th)
    return x, y


def draw_footprint(fp, beam_wid, grid_wid, labels=None):
    # fp - footprint object
    # beamWid in degrees
    # gridHWis in degrees
    if labels is None:
        labels = []
    do_label = False
    if len(labels) == fp.nBeams:
        do_label = True
    radius = beam_wid / 2.0
    for i in range(fp.nBeams):
        x0, y0 = fp.offsetsRect[i] * 180 / pi
        x0 *= -1.0
        # todo: check why y0 is not sign reversed here
        x, y = make_circle(radius, x0, y0)
        plt.plot(x, y, '-k', lw=0.5)
        plt.grid()
        plt.text(x0, y0, "%d" % i, va='center', ha='center', fontsize=7)
        if do_label:
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
    plt.xlim(-grid_wid, grid_wid)
    plt.ylim(-grid_wid, grid_wid)


def draw_footprint_il(fp, beam_wid, grid_wid, labels=None):
    # fp - footprint object
    # beamWid in degrees
    # gridHWis in degrees
    if labels is None:
        labels = []
    ax = plt.gca()
    doLabel = False
    if len(labels) == fp.nBeams:
        doLabel = True
    radius = beam_wid / 2.0
    cols = ['w', 'b', 'y', 'r']
    for i in range(fp.nBeams):
        x0, y0 = fp.offsetsRect[i] * 180 / pi
        x0 *= -1.0
        # todo: check why y0 is not sign reversed here
        circle = plt.Circle((x0, y0), radius, color=cols[0], alpha=0.5)
        ax.add_artist(circle)
        x, y = make_circle(radius, x0, y0)
        plt.plot(x, y, '-k', lw=0.5)
        plt.grid()
        plt.text(x0, y0, "%d" % i, va='center', ha='center', fontsize=7)
        if doLabel:
            plt.text(x0, y0 - radius * 0.5, labels[i], va='center', ha='center', fontsize=7)
    for j, p in enumerate(fp.interOffsRect):
        for i in range(fp.nBeams):
            x0, y0 = (p + fp.offsetsRect[i]) * 180 / pi
            x0 *= -1.0
            # todo: check why y0 is not sign reversed here
            circle = plt.Circle((x0, y0), radius, color=cols[j + 1], alpha=0.25)
            ax.add_artist(circle)
            x, y = make_circle(radius, x0, y0)
            plt.plot(x, y, '-k', lw=0.5)
            plt.grid()
            plt.text(x0, y0, "%d" % i, va='center', ha='center', fontsize=7)
            if doLabel:
                plt.text(x0, y0 - radius * 0.5, labels[i], va='center', ha='center', fontsize=7)

    plt.xlim(-grid_wid, grid_wid)
    plt.ylim(-grid_wid, grid_wid)
