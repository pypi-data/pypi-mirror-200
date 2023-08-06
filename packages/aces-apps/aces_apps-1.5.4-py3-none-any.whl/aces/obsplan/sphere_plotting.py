#!/usr/bin/env python
"""Utiliies to create matplotlib figures of positions on the sky sphere.
"""

import numpy as np
from numpy import cos, sin, arctan2, pi
import matplotlib.pylab as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

from askap.footprint import Skypos

from aces.obsplan.segmented_plot import segment_plot
from aces.obsplan.segmented_plot import segment_3vec


def prefix(word, pfx):
    if word.startswith(pfx):
        return word
    else:
        return pfx + word


def rd_xyz(ra, dec):
    """TBD"""
    v = [np.cos(ra) * np.cos(dec), np.sin(ra) * np.cos(dec),
         np.sin(dec)]
    return v


def xyz_rd(v):
    x, y, z = v
    b2 = np.arcsin(z)
    b1 = (2.0 * np.pi + np.arctan2(y, x)) % (2.0 * np.pi)
    return b1, b2


def mollweide_theta(z):
    ths = []
    for zi in z:
        th = np.arcsin(zi)
        pz = np.pi * zi
        th2 = 2. * th
        thi = th - (th2 + np.sin(th2) - pz) / (2.0 + 2.0 * np.cos(th2))
        while np.abs(thi - th) > 1.0e-5:
            th = thi
            th2 = 2. * th
            thi = th - (th2 + np.sin(th2) - pz) / (2.0 + 2.0 * np.cos(th2))
        ths.append(thi)
    return ths


class SphereView(object):
    # positions are passed in as Skypos instances.
    # angles are give in radians
    npole = Skypos(0.0, np.pi / 2)
    spole = Skypos(0.0, -np.pi / 2)
    origin = Skypos(0.0, 0.0)

    def __init__(self, projection='CAR', axis=None):
        mpl_projection = SphereView.get_projection(projection)
        # proj_mpl = [u'aitoff', u'hammer', u'lambert', u'mollweide', u'polar', u'rectilinear']
        # if projection == 'CAR' or projection == 'ORTH':
        #     mpl_projection = u'rectilinear'
        # elif projection == 'MOLL':
        #     mpl_projection = u'mollweide'
        # elif projection in proj_mpl:
        #     mpl_projection = projection
        # else:
        #     print ("Projection {} not recognised".format(projection))
        #         self.axis = figure.add_axes(rect, projection=mpl_projection)
        if axis is None:
            fig = plt.gcf()
            self.axis = fig.add_subplot(111, projection=mpl_projection)
        else:
            self.axis = axis
        self.projection = projection
        self.mpl_projection = mpl_projection
        self.subpoint = Skypos(0.0, 0.0)
        self.m1 = np.array([[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]])
        self.grid_style = {'color': '0.7', 'lw': 0.2}
        self.style = {'color': 'k', 'lw': 0.2, 'alpha': 0.6}
        self.fill_style = {'color': 'b', 'alpha': 0.4}
        # if self.projection in ['CAR','ORTH']:
        self._set_axes()

    def set_projection(self, projection):
        self.projection = projection

    def set_subpoint(self, sub):
        self.subpoint = sub
        self.m1 = self._make_matrix()

    def set_style(self, style):
        self.style = style

    def draw_point(self, p1, **style):
        # Draw point p1 on the sphere
        vectors = np.array([p1.get_vec()])
        self.style['marker'] = 'o'
        self._draw(vectors, **style)
        del self.style['marker']

    def draw_gc(self, p1, p2, **style):
        # Draw the great circle between p1 and p2
        vectors = self._get_gc_vec(p1, p2)
        self._draw(vectors, **style)

    def draw_gc_c(self, p1, **style):
        # Draw the great circle between p1 and p2
        vectors = self._get_gc_vec_c(p1)
        self._draw(vectors, **style)

    def draw_sc(self, p, radius, ends=None, **style):
        # Draw a small circle about p at the given radius
        if ends is None:
            l1, l2 = 0.0, 2.0 * np.pi
            nseg = 80
        else:
            l1, l2 = ends
            nseg = abs(int((l2 - l1) / (2.0 * np.pi) * 80.))
        ps = [p.offset([radius, pa]) for pa in np.linspace(l1, l2, nseg)]
        vectors = np.array([a._vec for a in ps])
        self._draw(vectors, **style)

    def join_gc(self, p_array, close=False, **style):
        for i in range(1, len(p_array)):
            self.draw_gc(p_array[i - 1], p_array[i], **style)
        if close:
            self.draw_gc(p_array[-1], p_array[0], **style)

    def join_gc_fill(self, p_array, **style):
        for i in range(1, len(p_array)):
            vectors = self._get_gc_vec(p_array[i - 1], p_array[i])
            x, y = self._project(vectors)
            pn = np.array([x[~x.mask], y[~y.mask]])
            pn = np.swapaxes(pn, 0, 1)
            if i > 1:
                pnts = np.concatenate([pnts, pn])
            else:
                pnts = pn
        self.fill(pnts, **style)

    def fill(self, pnts, **style):
        if len(pnts) > 1:
            eps = 0.3
            dmax, dmin = np.diff(pnts[:, 0]).max(), np.diff(pnts[:, 0]).min()
            # print dmax, np.pi * 2.0 - eps
            if dmax > np.pi + eps:
                imax, imin = np.where(dmax == np.diff(pnts[:, 0]))[0][0], np.where(dmin == np.diff(pnts[:, 0]))[0][0]
                jmin = min(imax, imin)
                jmax = max(imax, imin)
                # print jmin, jmax
                xmi = np.pi * np.sign(pnts[jmin, 0])
                xma = np.pi * np.sign(pnts[jmax, 0])
                buf = np.array([[xmi, pnts[jmin, 1]], [xmi, pnts[jmax + 1, 1]]])
                pnts1 = np.concatenate((pnts[0:jmin, :], buf, pnts[jmax + 1:, :]))
                bufa = np.array([[xma, pnts[jmin + 1, 1]]])
                bufb = np.array([[xma, pnts[jmax, 1]]])

                pnts2 = np.concatenate((bufa, pnts[jmin + 1:jmax, :], bufb))
                poly1 = Polygon(pnts1, True)
                poly2 = Polygon(pnts2, True)
                polys = [poly1, poly2]


            else:
                polygon = Polygon(pnts, True)
                polys = [polygon]
            if len(style) == 0:
                style = self.fill_style

            p = PatchCollection(polys, **style)
            self.axis.add_collection(p)

    def draw_text(self, p, text, **style):
        vectors = np.array([p._vec])
        self._text(vectors, text, **style)

    def draw_outline(self):
        if self.projection == 'ORTH':
            nseg = 360
            vectors = np.zeros([nseg, 3])
            ths = np.linspace(0.0, 2.0 * np.pi, 360)
            y = np.cos(ths)
            z = np.sin(ths)
            vectors[:, 0] = 0.001
            vectors[:, 1] = y
            vectors[:, 2] = z
            self._draw(vectors, rotate=False)
        if self.projection == "MOLL":
            npole, spole = SphereView.npole, SphereView.spole
            p = [npole, Skypos(pi, 0.0), spole]
            self.join_gc(p)
            eps = 1.0e-5
            p = [npole, Skypos(-pi + eps, 0.0), spole]
            self.join_gc(p)

    def draw_coord_grid(self, dlon=15., dlat=10.):
        # if self.projection == "MOLL":
        #     plt.sca(self.axis)
        #     plt.grid()

        if True:
            npole, spole = SphereView.npole, SphereView.spole
            eqpnts = [Skypos(a, 0.0) for a in np.arange(0.0, 2.0 * np.pi, dlon * np.pi / 180.)]
            lon_set = [[npole, a, spole] for a in eqpnts]
            radii = np.arange(0., np.pi, dlat * np.pi / 180.)
            g_style = self.grid_style.copy()
            for i, p in enumerate(lon_set):
                if i == 0:
                    g_style['color'] = 'k'
                else:
                    g_style['color'] = self.grid_style['color']
                self.join_gc(p, **g_style)

            for i, r in enumerate(radii[1:]):
                if i == 8:
                    g_style['color'] = 'k'
                else:
                    g_style['color'] = self.grid_style['color']

                self.draw_sc(npole, r, **g_style)

    def draw_label(self):
        xl = self.axis.get_xlim()
        yl = self.axis.get_ylim()
        x = 0.99 * xl[0] + 0.01 * xl[1]
        y = 0.99 * yl[0] + 0.01 * yl[1]
        st = {'fontsize': 9}
        self.axis.text(x, y, self.projection, **st)

    def _set_axes(self):
        ax = self.axis
        #         ax.set_aspect(1.0)
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

        if self.projection == 'CAR':
            ax.set_xlim(-np.pi, np.pi)
            ax.set_ylim(-np.pi / 2, np.pi / 2)
        elif self.projection == 'ORTH':
            ax.set_aspect(1.0)
            ax.set_xlim(-1.1, +1.1)
            ax.set_ylim(-1.1, +1.1)

    def _project(self, vectors, rotate=True):
        # Takes a set of 3-vectors (x,y,x) of points on a sphere.
        # Returns 2-vectors (x,y) as the projection of this points onto a plane according
        # to the projection code in self.projection.
        # Recognised projections:
        #  CAR  - (Plate Carre) - Equirectangular projection
        #  ORTH - Orthographic projection - view from infinity, only one side of the sphere visible
        #  MOLL - Mollweide projection
        if rotate:
            t_vectors = self._rotate_vectors(self.m1, vectors)
        else:
            t_vectors = vectors
        if self.projection in ['CAR', 'MOLL', 'aitoff', 'hammer']:
            # convert x,y into azimuthal angle and plot as x
            # plot z as y
            x = np.arctan2(t_vectors[:, 1], t_vectors[:, 0])
            y = np.arcsin(t_vectors[:, 2])
            msk = False
        elif self.projection == 'ORTH':
            # The view is from the x = + infinity position:
            # Take x as "depth" and use to flag horizontal and vertical
            # Take y as horizontal, and z as vertical
            z = t_vectors[:, 0]
            msk = (z < 0.0)
            x = t_vectors[:, 1]
            y = t_vectors[:, 2]

        x = np.ma.masked_array(x, mask=msk)
        y = np.ma.masked_array(y, mask=msk)

        return x, y

    def _draw_y(self, vectors, rotate=True, **style):
        x, y = self._project(vectors, rotate)
        if len(style) == 0:
            style = self.style
        ax = self.axis
        plt.sca(ax)
        seg_plotter = segment_plot(lims=[-np.pi, np.pi], thresh=0.6)
        seg_plotter(x, y, **style)

    def _draw(self, vectors, rotate=True, **style):
        style_final = self.style.copy()
        for k, v in style.items():
            style_final[k] = v
        segs = segment_3vec(lims=[-np.pi, np.pi], thresh=0.6)
        for x0, y0, z0 in segs.iter(vectors[:, 0], vectors[:, 1], vectors[:, 2]):
            vecseg = np.swapaxes(np.vstack([x0, y0, z0]), 0, 1)
            x, y = self._project(vecseg, rotate)
            if len(style) == 0:
                style = self.style
            ax = self.axis
            plt.sca(ax)
            seg_plotter = segment_plot(lims=[-np.pi, np.pi], thresh=0.6)
            seg_plotter(x, y, **style_final)

    def _text(self, vectors, text, rotate=True, **style):
        x, y = self._project(vectors, rotate)
        if x.count() > 0:
            if len(style) == 0:
                style = self.style
            ax = self.axis
            plt.sca(ax)
            plt.text(x, y, text, va='center', ha='center', **style)

    def _make_matrix(self):
        a = -self.subpoint.ra
        b = -self.subpoint.dec
        ca, sa = np.cos(a), np.sin(a)
        cb, sb = np.cos(b), np.sin(b)
        m1 = np.array([[cb * ca, -cb * sa, -sb], [sa, ca, 0.], [sb * ca, -sb * sa, cb]])

        return m1

    @staticmethod
    def _rotate_vectors(m, vectors):
        ret = np.zeros(vectors.shape)
        for i in range(vectors.shape[0]):
            ret[i, :] = np.dot(m, vectors[i, :])
        return ret

    @staticmethod
    def _get_gc_vec(p, q):
        nseg = max(2, int(p.d_pa(q)[0] / 0.04))
        M = np.array((p._dvecx, p._dvecy, p._dvecz))
        Mt = np.array(np.matrix(M).T)
        alpha, phi = xyz_rd(np.dot(M, q._vec))
        phii = np.linspace(np.pi / 2, phi, nseg)
        vi = [rd_xyz(alpha, ph) for ph in phii]
        veci = [np.dot(Mt, v) for v in vi]
        return np.array(veci)

    @staticmethod
    def _get_gc_vec_c(p):
        cp, sp = cos(pi / 2 - p.dec), sin(pi / 2 - p.dec)
        ca, sa = cos(p.ra), sin(p.ra)
        nseg = 200
        t = np.linspace(0.0, 2 * pi, nseg)
        ct = cos(t)
        st = sin(t)
        vec = np.array([cp * ca * ct - sa * st, cp * sa * ct + ca * st, -sp * ct])
        return np.swapaxes(vec, 0, 1)

    @classmethod
    def get_projection(cls, projection):
        proj_mpl = [u'aitoff', u'hammer', u'lambert', u'mollweide', u'polar', u'rectilinear']
        if projection == 'CAR' or projection == 'ORTH':
            mpl_projection = u'rectilinear'
        elif projection == 'MOLL':
            mpl_projection = u'mollweide'
        elif projection in proj_mpl:
            mpl_projection = projection
        else:
            print("Projection {} not recognised".format(projection))
        return mpl_projection


def get_gc_intersect(s1, s2):
    """
    Given two great circles, specified by their poles, find the two intersection points.
    :param s1: Pole of first great circle as Skypos object
    :param s2: Pole of second great circle as Skypos object
    :return: A list of the two Skypos objects representing the two intersection points.
    """

    cp1, sp1 = cos(pi / 2 - s1.dec), sin(pi / 2 - s1.dec)
    ca1, sa1 = cos(s1.ra), sin(s1.ra)
    cp2, sp2 = cos(pi / 2 - s2.dec), sin(pi / 2 - s2.dec)
    ca2, sa2 = cos(s2.ra), sin(s2.ra)

    v = -sp1 * ca1 * sa2 + sp1 * sa1 * ca2
    u = sp1 * ca1 * cp2 * ca2 + sp1 * sa1 * cp2 * sa2 - cp1 * sp2
    alpha = arctan2(v, u)
    t = alpha - pi / 2.
    st2, ct2 = sin(t), cos(t)
    M = np.array([[cp1 * ca1, cp1 * sa1, -sp1], [-sa1, ca1, 0.], [sp1 * ca1, sp1 * sa1, cp1]])
    Mt = np.array(np.matrix(M).T)
    xyz = np.array([cp2 * ca2 * ct2 - sa2 * st2, cp2 * sa2 * ct2 + ca2 * st2, -sp2 * ct2])
    x, y, z = np.dot(M, xyz)
    vec = np.dot(Mt, [x, y, z])
    rd = xyz_rd(vec)

    return Skypos(rd[0], rd[1]), Skypos(rd[0] + pi, -rd[1])
