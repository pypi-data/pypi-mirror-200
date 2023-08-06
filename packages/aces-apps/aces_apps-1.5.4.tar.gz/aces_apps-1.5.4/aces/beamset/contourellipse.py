#!/usr/bin/env python
"""
Contains routines for fitting an ellipse to a contour.
Fitting the set of (x,y) points on the first null to an ellipse uses the code
from http://nicky.vanforeest.com/misc/fitEllipse/fitEllipse.html
Also the routine hafLocus to find the locus of points along the half peak level

Copyright (C) CSIRO 2017
"""
import numpy as np
from numpy.linalg import eig, inv
from aces.beamset import model as bm


class ContourEllipse(bm.Model):
    PARAM_NAMES = ['ell_a', 'ell_b',
                   'ell_c', 'ell_d', 'ell_f',
                   'ell_g', 'residual_rms']
    NUM_PARAMS = len(PARAM_NAMES)

    def __init__(self, params=[]):
        bm.Model.__init__(self, params)

        self.params = params
        self.valid = False
        if len(params) >= ContourEllipse.NUM_PARAMS:
            self.a = params[:-1]
            # self.delta = params[-3]
            # self.contrast = params[-2]
            self.rmsResid = params[-1]
            self.valid = True
            self._fill_attributes()

    def fit(self, x, y):
        x1 = x[:, np.newaxis]
        y1 = y[:, np.newaxis]
        D = np.hstack((x1*x1, x1*y1, y1*y1, x1, y1, np.ones_like(x1)))
        S = np.dot(D.T, D)
        C = np.zeros([6, 6])
        C[0, 2] = C[2, 0] = 2
        C[1, 1] = -1
        E, V = eig(np.dot(inv(S), C))
        n = np.argmax(np.abs(E))
        a = V[:, n]
        if a[5] > 0.0:
            a *= -1.0
        self.a = a
        # self.delta = np.dot(a.T, np.dot(S, a))
        # temp = np.sort(np.abs(E))
        # self.contrast = temp[-1]/temp[-2]
        self._fill_attributes()
        if self.valid:
            self.rmsResid = self._calc_residual(x, y)
        else:
            self.rmsResid = 0.0
        self.params = np.concatenate(
            (self.a, [self.rmsResid]))

    def _fill_attributes(self):
        up, down1, down2 = self._get_up_down()
        if up/down1 < 0.0 or up/down2 < 0.0:
            self.valid = False
        elif type(self.a[0]) == np.complex128:
            self.valid = False
        else:
            self.axes = self._ellipse_axis_length()
            self.centre = self._ellipse_center()
            self.angle = self._ellipse_angle_of_rotation()
            self.major_angle = self._ellipse_angle_of_rotation2()
            self.semimajor = self.axes.max()
            self.semiminor = self.axes.min()
            # if self.axes[0] < self.axes[1]:
            #     self.major_angle = (self.angle + pi/2.) % pi
            # else:
            #     self.major_angle = self.angle % pi
            self.eccentricity = np.sqrt(1.0 - (self.semiminor/self.semimajor)**2)
            self.valid = True


    def get_residual_rms(self):
        return self.rmsResid

    def is_good_fit(self):
        # override base
        return self.valid

    def evaluate(self, arg):
        """ For this class, evaluation has no meaning
        """
        print("Method evaluate not implemented for ", self.__class__.__name__)
        return None

    def get_locus50(self, arg):
        """ Returns the locus of (x,y) over the range of
        the input angular arg
        """
        if type(arg) == float:
            phi = np.array([arg])
        else:
            phi = np.array(arg)
        x, y = self._evaluate(phi)
        return x * self.angScale, y * self.angScale

    def _evaluate(self, phi):
        # Computes the locus of (x,y) over the range of
        # the input angular phi
        # a, b = axis lengths
        a, b = self.axes[0], self.axes[1]
        x0, y0 = self._ellipse_center()
        # if a < b:
        #     phi += np.pi/2
        theta = self.angle
        x = x0 + a*np.cos(phi)*np.cos(theta) - b*np.sin(phi)*np.sin(theta)
        y = y0 + a*np.cos(phi)*np.sin(theta) + b*np.sin(phi)*np.cos(theta)
        return x, y

    def _get_abcdfg(self):
        aa = self.a
        return aa[0], aa[1]/2, aa[2], aa[3]/2, aa[4]/2, aa[5]

    def _get_up_down(self):
        a, b, c, d, f, g = self._get_abcdfg()
        # print a,b,c,d,f,g
        up = 2*(a*f*f+c*d*d+g*b*b-2*b*d*f-a*c*g)
        down1 = (b*b-a*c)*(-np.sqrt((a-c)**2+4*b*b)-(c+a))
        down2 = (b*b-a*c)*(np.sqrt((a-c)**2+4*b*b)-(c+a))
        # down2 = (b*b-a*c)*((a-c)*np.sqrt(1+4*b*b/((a-c)*(a-c)))-(c+a))
        return up, down1, down2

    def _ellipse_center(self):
        a, b, c, d, f, g = self._get_abcdfg()
        num = b*b-a*c
        x0 = (c*d-b*f)/num
        y0 = (a*f-b*d)/num
        return np.array([x0, y0])

    def _ellipse_angle_of_rotation(self):
        a, b, c, d, f, g = self._get_abcdfg()
        if a==c:
            return 0.0
        else:
            return 0.5*np.arctan2(2*b, (a-c))
 

    def _ellipse_angle_of_rotation2(self):
        a, b, c, d, f, g = self._get_abcdfg()
        if b == 0:
            if a < c:
                return 0.0
            else:
                return np.pi/2.0
        else:
            if a < c:
                return np.arctan(2*b/(a-c))/2.0
            else:
                return np.pi/2 + np.arctan(2*b/(a-c))/2.0

    def _ellipse_axis_length(self):
        up, down1, down2 = self._get_up_down()
        res1 = np.sqrt(up/down1)
        res2 = np.sqrt(up/down2)
        return np.array([res1, res2])

    def get_translated(self, dxy):
        h,k = self._ellipse_center() + dxy
        u,v = self._ellipse_axis_length()
        th = self._ellipse_angle_of_rotation()
        c,s = np.cos(th),np.sin(th)

        A = (v*c)**2+(u*s)**2
        B = 2*c*s*(v**2 - u**2)
        C = (v*s)**2 + (u*c)**2
        D = -B*k - 2*h*A
        F = -B*h - 2*k*C
        G = u**2*(s**2*h**2 + 2*c*s*h*k + c**2*k**2) + v**2*(c**2*h**2 - 2*c*s*h*k + s**2*k**2) - (u*v)**2
        S1 = 's1 '+','.join(["%9.7f"%q for q in self.a])
        S2 = 's2 '+','.join(["%9.7f"%q for q in [A,B,C,D,F,G]])
        print(S1)
        print(S2)
        new_a = np.array([A, B, C, D, F, G, self.rmsResid])
        return ContourEllipse(new_a)


    # Compute some kind of fitting residual.  For each data point we need to find its distance to
    # the fitted ellipse. Do this in a radial sense - that will be the shortest distance. (True? Not quite, but close for small ellipticity.).
    # 1. For each data point, (xi,yi), subtract the fitted centre to give (dxi,dyi).
    # 2. Compute the datum's angular position from the x-axis: ang = arctan2(dyi,dxi)
    # 3. for each, evaaluate the location of the fitted ellipse (fxi,fyi)
    # 4. Calculate ri, fri from (xi,yi) and (fxi,fyi)
    # 4. Compute sqrt(sum((fri-ri)**2)/Nxy) as the rms residual.
    def _calc_residual(self, x, y):
        xc, yc = self.centre
        dx = x-xc
        dy = y-yc
        ell_ang = self.angle
        if self.axes[0] < self.axes[1]:
            ell_ang += np.pi/2

        ang = np.arctan2(dy, dx) - ell_ang
        r = np.sqrt(x**2+y**2)
        fx, fy = self._evaluate(ang)
        fr = np.sqrt(fx**2+fy**2)
        resid = np.sqrt(((r-fr)**2).sum()/x.shape[0])
        self.fx = fx
        self.fy = fy
        return resid

##########################  end of ellipse fitting routines ################


def greens(seg):
    # returns the area enclosed in the path given in seg.
    # https://math.blogoverflow.com/2014/06/04/greens-theorem-and-area-of-polygons/
    n = seg.shape[0]
    if n > 0:
        segx = np.reshape(np.append(seg, seg[0:1, :]), (n+1, 2))
        x, y = segx[:, 0], segx[:, 1]
        ds = 0.0
        for k in range(len(seg)):
            ds += (x[k+1] + x[k]) * (y[k+1] - y[k])/2
        return abs(ds)
    else:
        return 0.0
