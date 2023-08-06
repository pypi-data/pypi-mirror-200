#!/usr/bin/env python
"""
Example use of BeamSet and subclasses BeamModel.

Copyright (C) CSIRO 2017
"""

import numpy as np
from numpy import pi

import aces.beamset.contourellipse as ce
import aces.beamset.gaussfitter as gf
import aces.beamset.model as bm

GAUSS_WID_FACT = np.sqrt(2.0 * np.log(2.0))


def guess_params(bmap):
    conts = bmap.get_contour(0.5)
    ret = None
    if len(conts) == 1 and conts[0][1]:
        xy = conts[0][0]
        area = ce.greens(xy) * (180.0 / np.pi) ** 2
        if area > 0.6:
            ell = ce.ContourEllipse()
            seg = conts[0][0]
            ell.fit(seg[:, 0], seg[:, 1])
            if ell.valid:
                cnt = ell.get_centre()
                angl = ell.get_major_angle()
                axl = ell.get_axes() / GAUSS_WID_FACT

                # ht = np.median(bmap.data)
                ht = 0.0
                amp = bmap.data.max() - ht
                resid_rms = 0.0
                ret = (ht, amp, cnt[0], cnt[1], axl[0], axl[1], angl, resid_rms)
        # print "Ellipse fit success"
    # else:
    #     print 'Ellipse fit failure'
    return ret


class SurfaceGaussian(bm.Model):
    PARAM_NAMES = ['baseHeight', 'amplitude',
                   'xPos', 'yPos', 'xWidth',
                   'yWidth', 'rotation', 'residual_rms']
    NUM_PARAMS = len(PARAM_NAMES)
    FUNCTION_NAME = "2D gaussian"
    SHORT_NAME = "gauss2D"

    # def __init__(self, bmap, paramGuess, indexGuess=False):
    def __init__(self, params=[]):
        """ This performs a simple transformation between index and world parameters
        and it assumes the x scales and y scales are the same.
        """
        bm.Model.__init__(self, params)

        self.params = params

        self.worldParam = params[:-1]
        self.rmsResid = params[-1]
        self.bmap = None
        self.indexParam = None
        self.fitted = None
        self._fill_attributes()

    def fit(self, bmap):
        assert bmap.dx == bmap.dy, "X and Y grid spacings must be equal."
        self.bmap = bmap
        indexParam = self._world_to_indexPar(self.worldParam)
        fixed = np.repeat(False, 7)
        fixed[0] = True
        self.indexParam = gf.gaussfit(bmap.data, params=indexParam, fixed=fixed)
        self.worldParam = self._index_to_worldPar(self.indexParam)
        self._fill_attributes()

    def _fill_attributes(self):
        self.g = gf.twodgaussian(self.worldParam)
        self.base = self.params[0]
        self.amplitude = self.params[1]
        self.axes = self.params[4:6]
        self.centre = self.params[2:4]
        self.angle = self.params[6]

        self.semimajor = max(self.axes) * GAUSS_WID_FACT
        self.semiminor = min(self.axes) * GAUSS_WID_FACT
        if self.axes[0] < self.axes[1]:
            self.major_angle = (self.angle + pi / 2.) % pi
        else:
            self.major_angle = self.angle % pi
        self.eccentricity = np.sqrt(1.0 - (self.semiminor / self.semimajor) ** 2)

        if self.bmap:
            self.fitted = self.evaluate(self.bmap.x, self.bmap.y)
            diff = self.fitted - self.bmap.data
            # Compute an RMS residual. Any non-zero mean will increase this.
            self.rmsResid = np.sqrt((diff ** 2).mean())
            self.params = self.worldParam + [self.rmsResid]

    def get_residual_rms(self):
        return self.rmsResid

    def evaluate(self, xw, yw):
        xg, yg = np.meshgrid(xw, yw)
        # NOTE: the returned g function expects x,y in reverse order, allowing
        #        python-style indices to be used
        return self.g(yg, xg)

    def get_locus50(self, arg):
        # Returns the locus of (x,y) over the range of
        # the input angular arg
        if type(arg) == float:
            phi = np.array([arg])
        else:
            phi = np.array(arg)
        x, y = self._locus50(phi)
        return x * self.angScale, y * self.angScale

    def _locus50(self, phi):
        # For this class, Evaluate returns the locus of (x,y) over the range of
        # the input angular phi
        # a, b = axis lengths
        a, b = self.semimajor, self.semiminor
        x0, y0 = self.centre
        if a < b:
            phi += np.pi / 2
        theta = self.angle
        x = x0 + a * np.cos(phi) * np.cos(theta) - b * np.sin(phi) * np.sin(theta)
        y = y0 + a * np.cos(phi) * np.sin(theta) + b * np.sin(phi) * np.cos(theta)
        return x, y

    def get_world_params(self):
        return self.worldParam

    def get_index_params(self):
        return self.indexParam

    def _world_to_indexPar(self, wp):
        ip = list(wp)
        bmap = self.bmap
        ip[2] = (wp[2] - bmap.x[0]) / bmap.dx
        ip[3] = (wp[3] - bmap.y[0]) / bmap.dy
        ip[4] = wp[4] / bmap.dx
        ip[5] = wp[5] / bmap.dy
        return ip

    def _index_to_worldPar(self, ip):
        wp = list(ip)
        bmap = self.bmap
        wp[2] = ip[2] * bmap.dx + bmap.x[0]
        wp[3] = ip[3] * bmap.dy + bmap.y[0]
        wp[4] = ip[4] * bmap.dx
        wp[5] = ip[5] * bmap.dy
        return wp

    # def _world_to_index(self, wx, wy):
    #     # Expects world coordinates in np.ndarray
    #     ix = (wx - self.x[0])/self.dx
    #     iy = (wy - self.y[0])/self.dy
    #     return ix, iy

    # def _index_to_world(self, ix, iy):
    #     # Expects world coordinates in np.ndarray
    #     wx = ix*self.dx + self.x[0]
    #     wy = iy*self.dy + self.y[0]
    #     return wx, wy
