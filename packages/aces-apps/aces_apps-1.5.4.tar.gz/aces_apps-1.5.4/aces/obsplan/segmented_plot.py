
"""
From github contribitor lkilcher at
https://gist.github.com/lkilcher/72a7274fe7b0a064b333

Corrected for this application, allowing jumps in both directions across the boundaries.

"""
from __future__ import division

from matplotlib.pyplot import gca
import numpy as np


class segment_plot(object):

    def __init__(self, lims=None, thresh=0.95):
        if lims is None:
            lims = [0, 24]
        self.lims = lims
        self.thresh = thresh
        self.delta = lims[1] - lims[0]

    def unlink_wrap(self, dat):
        jump = np.nonzero(np.abs(np.diff(dat)) > (self.delta * self.thresh))[0]
        lasti = 0
        for ind in jump:
            yield slice(lasti, ind + 1)
            lasti = ind + 1
        yield slice(lasti, len(dat))

    def pad_segments(self, x, y, slc):
        x_values = x[slc]
        y_values = y[slc]
        if slc.stop + 1 < len(x):
            si = np.sign(x[slc.stop] - x[slc.stop - 1])
            x_values = np.concatenate((x_values, [x[slc.stop + 1] - si * self.delta]))
            y_values = np.concatenate((y_values, [y[slc.stop]]))
        if slc.start > 0:
            si = np.sign(x[slc.start] - x[slc.start - 1])
            x_values = np.concatenate(([x[slc.start - 1] + si * self.delta], x_values))
            y_values = np.concatenate(([y[slc.start - 1]], y_values))
        return x_values, y_values

    def iter(self, x, y):
        for slc in self.unlink_wrap(x):
            yield self.pad_segments(x, y, slc)

    def __call__(self, x, y, ax=None, **kwargs):
        if ax is None:
            ax = gca()

        for x_vals, y_vals in self.iter(x, y):
            ax.plot(x_vals, y_vals, **kwargs)


class segment_3vec(object):
    # todo: derived from segment_plot - needs more work
    def __init__(self, lims=None, thresh=0.95):
        if lims is None:
            lims = [0, 24]
        self.lims = lims
        self.thresh = thresh
        self.delta = lims[1] - lims[0]
        self.pad = False

    def unlink_wrap(self, x, y):
        ang = np.arctan2(y, x)
        jump = np.nonzero(np.abs(np.diff(ang)) > (self.delta * self.thresh))[0]
        lasti = 0
        for ind in jump:
            yield slice(lasti, ind + 1)
            lasti = ind + 1
        yield slice(lasti, len(x))

    def pad_segments(self, x, y, z, slc):
        x_values = x[slc]
        y_values = y[slc]
        z_values = z[slc]
        if self.pad:
            if slc.stop + 1 < len(x):
                si = np.sign(x[slc.stop] - x[slc.stop - 1])
                x_values = np.concatenate((x_values, [x[slc.stop + 1] - si * self.delta]))
                y_values = np.concatenate((y_values, [y[slc.stop]]))
                z_values = np.concatenate((z_values, [z[slc.stop]]))
            #                 print 'a ', slc
            if slc.start > 0:
                si = np.sign(x[slc.start] - x[slc.start - 1])
                x_values = np.concatenate(([x[slc.start - 1] + si * self.delta], x_values))
                y_values = np.concatenate(([y[slc.start - 1]], y_values))
                z_values = np.concatenate(([z[slc.start - 1]], z_values))
        #                 print 'b ', slc

        return x_values, y_values, z_values

    def iter(self, x, y, z):
        for slc in self.unlink_wrap(x, y):
            yield self.pad_segments(x, y, z, slc)

#     def __call__(self, x, y, ax=None, **kwargs):
#         if ax is None:
#             ax = gca()

#         for x_vals, y_vals in self.iter(x, y):
#             ax.plot(x_vals, y_vals, **kwargs)

