#!/usr/bin/env python
"""
Defines the BeamMap class

Copyright (C) CSIRO 2017
"""
import numpy as np
import matplotlib.pyplot as plt
# noinspection PyProtectedMember
# from matplotlib import _cntr as cntr

from aces.beamset import mapset as ms


class BeamMap(object):
    """
    BeamMap is a 2D ndarray representing an antenna/beam quantity as a function of direction.
    It isn't sufficient to define the quantities stored.  Most of the metadata defining the
    quantities is in the BeamSet class.  BeamMap is more of a convenience class used to implement
    the BeamSet class.  It doesn't stand on it's own. (?)
    """

    def __init__(self, x, y, data, maptype, flag, vector):
        """
        :param x: list of x grid positions (nominally l in tangent plane meeting sphere at antenna boresight)
        :param y: list of y grid positions (nominally m in tangent plane meeting sphere at antenna boresight)
        :param data: 2D ndarray representing an antenna/beam quantity as a function of direction (x,y)
        :param maptype: string with one of these values defining the type of quantity in data and how it is ploted
                        amp - scalar voltage amplitude (currently normalised to peak)
                        ph - voltage phase (in degrees)
                        pwr - total power = amp**2 (scalar, currently normalised to peak)
        :param flag: Boolean, copy of flag from BeamSet level, True if BeamMap is valid
        :param vector: tuple of metadata (time, ant, beam, pol, freq)
            time: this map's time
            ant: int, antenna number, assumed ASKAP only for now
            beam: int, beam number
            pol: str, polarization
            freq: float, frequency (in MHz)
        """
        self.x = x
        self.y = y
        self.data = data
        self.type = maptype
        self.flag = flag
        self.vector = vector
        if maptype not in ms.MapSet.allowedMapTypes:
            raise ValueError("Invalid map type %s" % maptype)

        self.nx = len(self.x)
        self.ny = len(self.y)
        self.is1D = False
        if self.nx == 1:
            self.is1D = True
            self.delta = np.diff(self.y).mean()
        elif self.ny == 1:
            self.is1D = True
            self.delta = np.diff(self.x).mean()
        else:
            self.dx = np.diff(self.x).mean()
            self.dy = np.diff(self.y).mean()
            self.delta = max(self.dx, self.dy)

    def is_one_dim(self):
        return self.is1D

    def get_data(self):
        return self.data

    def get_contour(self, level):
        """
        Calculate contour of 2D data at given level, in this class it's used only to put a mark at the estimated
        centre of the beam, but has general use, for example in fitting and parameter estimation.

        :param level: level at which to calculate contour
        :return: list of contour segments [(segs, closed)]
        """
        ret = []
        if self.is1D:
            ret = []
        else:
            xg, yg = np.meshgrid(self.x, self.y)
            # c = cntr.Cntr(xg, yg, self.data)
            # res = c.trace(level)
            # n_segments = len(res) // 2
            # ret = []
            # for i_segment in range(n_segments):
            #     seg, codes = res[i_segment], res[i_segment + 1]
            #     ret.append((seg, self._seg_closed))
        return ret

    def normalise(self):
        """
        Normalise the data array: divide the whole array by the maximum of its absolute value.
        """
        self.data /= np.abs(self.data).max()

    def mask_below(self, level):
        """ Convert the map data to a masked array, and mask all values
        below the given level.
        """
        self.data = np.ma.masked_array(self.data, mask=(self.data < level))

    @staticmethod
    def _seg_closed(seg):
        """
        Determines if a contour segment is a closed loop
        :return: Boolean, True if contour segment is closed
        """
        return seg[0][0] == seg[-1][0] and seg[0][1] == seg[-1][1]

    def plot(self, log=False, title=False, xlabels=False, ylabels=False, bar=False, cmap=None, **kwargs):
        """
        Plot a BeamMap
        :param log: bool, plot on a dB scale (only used if BeamMap type is power)
        :param title: str, plot title
        :param bool xlabels: plot x axis labels if true
        :param bool ylabels: plot y axis labels if true
        :param bar: bool, plot colorbar if true
        :param cmap: str, matplotlib colormap [rainbow]
        :param kwargs: 'vmin', 'vmax' allow default data limits to be overriden

        """
        # Get information about the axes window:
        fig = plt.gcf()
        ax = plt.gca()
        ax_box = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
        small = 8
        if cmap is None:
            cmap = 'rainbow'
        my_cmap = plt.get_cmap(cmap)

        # get instance data:
        vec = self.vector
        mt = self.type
        nx = self.nx
        xs, ys, data = np.degrees(self.x), np.degrees(self.y), self.data
        is1D = self.is1D

        time, ant, beam, pol, freq = vec

        toplev = 0.5 * data.max()
        tit_template = "AK%02d Beam %d, Freq %d, %s, %s"
        if mt == 'power':
            if log:
                data = data - np.min(data) + 1E-6
                data = 10.0 * np.log10(data / np.max(data))
                toplev = data.max() - 0.1
                vmin = -50.0
                vmax = 0.0
                blabel = "Power (dB)"
                levs = [-3.0, -1.0]
            else:
                vmin = data.min()
                vmax = data.max()
                blabel = "Relative power"
                levs = [0.5]
        elif mt in ['amplitude', 'real', 'imag']:
            vmin = data.min()
            vmax = data.max()
            blabel = "Rel. amplitude"
            levs = [0.5]
        elif mt == 'complex':
            # data = np.abs(self.data)
            vmin = data.min()
            vmax = data.max()
            blabel = "Rel. amplitude"
            levs = [0.5]
        elif mt == 'phase':
            vmin = -180.0
            vmax = 180.0
            blabel = "Phase (deg)"
            levs = [0.0]
        else:
            raise (ValueError, 'Invalid BeamMap.type {}' % mt)

        if 'o_title' in kwargs:
            plot_title = kwargs['o_title']
        else:
            plot_title = tit_template % (ant, beam, freq, pol, blabel)

        ext = [xs[0], xs[-1], ys[0], ys[-1]]
        if is1D:
            if nx == 1:
                xp = ys
            else:
                xp = xs
            plt.plot(xp, data)
        else:
            # Override data limits if requested
            if 'vmin' in kwargs:
                vmin = kwargs['vmin']
            if 'vmax' in kwargs:
                vmax = kwargs['vmax']
            plt.imshow(data, my_cmap, origin='lower', extent=ext, vmin=vmin, vmax=vmax)

        if title:
            plt.title(plot_title)

        if xlabels:
            plt.xlabel("Offset (deg)")
            if ax_box.width < 2.0:
                for tick in ax.xaxis.get_major_ticks():
                    tick.label.set_fontsize(small)

        else:
            plt.gca().axes.get_xaxis().set_ticklabels([])

        if not is1D:
            if ylabels:
                plt.ylabel("Offset (deg)")
                if ax_box.width < 2.0:
                    for tick in ax.yaxis.get_major_ticks():
                        tick.label.set_fontsize(small)
            else:
                plt.gca().axes.get_yaxis().set_ticklabels([])

            if bar:
                cb1 = plt.colorbar(orientation="horizontal")
                cb1.set_label(blabel)

            # fsize = 'x-small'
            plt.rcParams['contour.negative_linestyle'] = 'solid'
            # X, Y = np.meshgrid(xs, ys)
            plt.contour(xs, ys, data, levels=levs, colors='k',
                        linewidths=[0.5, 0.5])

            # Plot contour and locate peak, approx
            p = self.get_contour(toplev)
            if len(p) == 1:
                seg, closed = p[0]
                x, y = seg[:, 0], seg[:, 1]

                bcx = np.degrees((np.min(x) + np.max(x)) / 2.0)
                bcy = np.degrees((np.min(y) + np.max(y)) / 2.0)

                plt.plot(bcx, bcy, '+')

    def is_equiv(self, other):
        """Check equivalence of grid and maptype of self and other map object
        """
        ret = (self.x == other.x).all() and \
              (self.y == other.y).all() and \
              self.type == other.type
        return ret

    def multiply(self, other):
        """Create and return a new map object which is the product of self and other
           TBD: modify the vector of the returned map in some consistent way. Perhaps need extension
           of the vector or the BeamMap class.
        """
        if self.is_equiv(other) and self.type == 'amplitude':
            x = self.x
            y = self.y
            maptype = 'power'
            flag = self.flag or other.flag
            data = self.data * other.data
            vector = self.vector
            return BeamMap(x, y, data, maptype, flag, vector)
        else:
            raise RuntimeError("BeamMaps not equivalent, or wrong type for multiplication")

    def divide(self, other):
        """Create and return a new map object which is the quotient : self / other
           TBD: modify the vector of the returned map in some consistent way. Perhaps need extension
           of the vector or the BeamMap class.
        """
        if self.is_equiv(other):
            x = self.x
            y = self.y
            maptype = self.type
            flag = self.flag or other.flag
            data = self.data / other.data
            vector = self.vector
            return BeamMap(x, y, data, maptype, flag, vector)
        else:
            raise RuntimeError("BeamMaps not equivalent")

    def add(self, other):
        """Create and return a new map object which is the sum of self and other
           TBD: modify the vector of the returned map in some consistent way. Perhaps need extension
           of the vector or the BeamMap class.
        """
        if self.is_equiv(other):
            x = self.x
            y = self.y
            maptype = self.type
            flag = self.flag or other.flag
            data = self.data + other.data
            vector = self.vector
            return BeamMap(x, y, data, maptype, flag, vector)
        else:
            raise RuntimeError("BeamMaps not equivalent")

    def subtract(self, other):
        """Create and return a new map object which is the difference of self and other
           TBD: modify the vector of the returned map in some consistent way. Perhaps need extension
           of the vector or the BeamMap class.
        """
        if self.is_equiv(other):
            x = self.x
            y = self.y
            maptype = self.type
            flag = self.flag or other.flag
            data = self.data - other.data
            vector = self.vector
            return BeamMap(x, y, data, maptype, flag, vector)
        else:
            raise RuntimeError("BeamMaps not equivalent")
