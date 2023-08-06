from __future__ import print_function

"""
Tool for quick image assessment.

Copyright (C) CSIRO 2019
"""

__author__ = 'Dave McConnell <david.mcconnell@csiro.au>'

import shutil
import time
import casacore.images as cim
from aces.obsplan.config import ACESConfig  # noqa
from astropy.io import fits

import numpy as np
import scipy.optimize as op
from scipy import signal
from scipy.stats import iqr
import pickle
import matplotlib as mpl

mpl.use('Agg')  # this line must precede pylab import to suppress display
import matplotlib.pyplot as plt  # noqa


def fit_func2(p, x):
    return p[0] * np.exp(-((x - p[1]) / p[2]) ** 2)


def err_func2(p, x, y):
    # Distance to the target function
    return fit_func2(p, x) - y


funcs = {'gau': (fit_func2, err_func2)}


def fit_g(x, y, p0, fkey='gau'):
    """

    :param x: independent coordinate (bin centres)
    :param y: histogram frequencies
    :param p0: initial guess fit params
    :param fkey: Selects function to fit
    """
    func = funcs[fkey][0]
    errf = funcs[fkey][1]
    xx = np.array(x)
    yy = np.array(y)
    #    p0 = [max(yy), mean(xx), min(yy)] # Initial guess for the parameters
    opres = op.least_squares(errf, p0, jac='3-point', args=(xx, yy))
    p = opres['x']
    xf = np.linspace(xx.min(), xx.max(), 100)
    yf = func(p, xf)
    res = 0.0
    for u, v in zip(xx, yy):
        res += errf(p, u, v) ** 2
    res = res / len(xx)
    return p, xf, yf, res


def find_mode(data, parameters, diag_plot=False):
    """
    Estimates and returns the mode of those input data that lie within the limits set by the parameters.
    The mode is determined by fitting a guassian function to the peak of the histogram of the logarithms of
    the values.

    :param data: np.array of real values
    :param parameters: dictionary giving the data value bounds
    :param diag_plot: used for debugging histogram analysis
    :return:
    """

    no_fit = [0.0, -1.0]

    lower = parameters['lower']
    upper = parameters['upper']
    if 'nbins' in parameters:
        nbins = parameters['nbins']
    else:
        nbins = 100
    if data.max() < lower:
        return [lower]
    if data.min() > upper:
        return [upper]
    # cdata = data.compressed()
    cdata = data
    if len(cdata) > 0:
        hist_range = (lower, upper)
        histdata = np.histogram(cdata, bins=nbins, range=hist_range)
        # print(lower, upper, cdata.min(), cdata.max())
        # print("{:d} NaNs".format(sum(~np.isnan(cdata))))

        hy = np.array(histdata[0])
        hx = np.array(histdata[1])
        hxc = (hx[:-1] + hx[1:]) / 2
        imode = np.where(hy == hy.max())[0][0]
        fit_wid = 500
        i1, i2 = max(0, imode - fit_wid), imode + fit_wid
        p0 = [hy.max(), hxc[imode], 200.]
        if p0[0] > 0:
            rfit = fit_g(hxc[i1:i2], hy[i1:i2], p0)
            if diag_plot:
                pfile = 'distfit_%f.png' % (time.time() - 1561192988)
                pkfile = open('distfit_%f.pkl' % (time.time() - 1561192988), 'w')
                pickle.dump((lower, upper, cdata), pkfile)
                pkfile.close()
                tf, ax = plt.subplots()
                ax.plot(hxc, hy)
                ax.plot(rfit[1], rfit[2])
                #             plt.xlim(7.0, 9.0)
                tf.savefig(pfile)
                plt.close(tf)
            if rfit[0][1] < lower:
                return [p0[1], rfit[0][2]]
            else:
                return rfit[0][1:]
        else:
            return no_fit
    else:
        return no_fit


def shrink_mask(data, n=25):
    dm = data.mask.astype(int)
    con = np.ones([n, n])
    con /= con.sum()
    dmc = signal.convolve2d(dm, con, boundary='symm', mode='same')
    datan = np.ma.masked_array(data, mask=dmc > 0.2)
    return datan


def get_beam_offsets(fp_name, fp_pitch, fp_ang):
    aces_cfg = ACESConfig()
    fp_factory = aces_cfg.footprint_factory
    fp = fp_factory.make_footprint(fp_name, fp_pitch, fp_ang)

    offsets = np.array(fp.offsetsRect)
    return offsets


# todo: Ensure reference position and pixel are correct.


def do_statistics(y, incr, do_mask=True):
    """

    :param y: image masked array
    :param incr: pixel increment in radians
    :param do_mask: if True, expand mask (shrink unmasked area)
    """
    if do_mask:
        y_masked = shrink_mask(y, n=30)
    else:
        y_masked = y
    # Get statistics
    med = np.ma.median(y_masked)
    lo, hi = med * 0.4, med * 2.0
    if lo > hi:
        loo = lo
        lo = hi
        hi = loo
    par = {'lower': lo, 'upper': hi}
    print(y.shape, med, lo, hi)
    fm = find_mode(y_masked, par)
    if len(fm) == 2:
        mode = fm[0]
        # mode = find_mode(y_masked, par)[0]
    else:
        mode = np.NaN
    statistics = {'minimum': y_masked.min(),
                  'maximum': y_masked.max(),
                  'mean': y_masked.mean(),
                  'std': y_masked.std(),
                  'median': med,
                  'mode': mode}

    ys = np.float32(1.0 / y ** 2)
    da = np.degrees(incr[0]) ** 2
    speed = ys.sum() * da
    statistics['speed'] = speed
    return statistics


def image_cell_statistic(in_file, out_dir, cellsize=100, statistic='rms', do_mask=True, replace_old=True):
    """
    Compute some statistic over square cells in an image
    :param in_file: input image as fits file
    :param cellsize: cell size in pixels
    :param statistic: what statistic to compute.
    :param do_mask: Modify masked portion image to eliminate annoying edge effects, particularly in rms.
    :param replace_old: If True, replace previous statistics image.
    :return:
    """
    file_extensions = {'rms': 'rms', 'min': 'min', 'rat': 'ratio', 'iqr': 'iqr', 'std': 'std', 'med': 'med'}

    if statistic not in file_extensions.keys():
        raise NotImplementedError("unsupported statistic")

    nf = "{}.{}.fits".format(in_file.stem, file_extensions[statistic])
    out_name = out_dir.joinpath(nf)
    casa_temp = str(out_dir.joinpath("{}.{}".format(in_file.stem, file_extensions[statistic])))

    fname = out_name
    process_image = True
    y = None
    new_incr = None

    if out_name.exists():
        if replace_old:
            print("File {} being overwritten".format(fname))
        else:
            # print("Opening {}".format(fname))
            casa_im = cim.image(str(fname))
            co = casa_im.coordinates()
            new_incr = co["direction"].get_increment()
            data = np.squeeze(casa_im.getdata())
            y = np.ma.masked_invalid(data)

            process_image = False

    # fmin = 0.0
    # fmax = 0.0
    # npixv = 0

    print("Opening {}".format(in_file))

    casa_im = cim.image(str(in_file))
    # data = np.squeeze(casa_im.getdata())
    data = casa_im.getdata()
    fmin = np.nanmin(data)
    fmax = np.nanmax(data)
    npixv = np.count_nonzero(~np.isnan(data))

    if process_image:
        data = np.ma.masked_invalid(data) * 1.0e6

        parameters = {}
        if statistic == 'rms':
            vals = np.float32(np.percentile(data.compressed(), [10., 90.]) * 4.)
            parameters['lower'] = vals[0]
            parameters['upper'] = vals[1]
            parameters['nbins'] = 60
        elif statistic == 'rat':
            parameters['clip'] = 40000.

        # empirically determined factor: gaussian width to std.
        if statistic == 'iqr':
            # See https://en.wikipedia.org/wiki/Interquartile_range
            factor = 1.0/1.349
        else:
            # Empirical. about 3% low.
            factor = 538. / 787.

        co = casa_im.coordinates()
        incr = co["direction"].get_increment()
        refp = co["direction"].get_referencepixel().astype(int)

        N = cellsize

        data4 = data
        print("Data shape : {}  len = {:d}".format(data.shape, len(data.shape)))
        print(np.expand_dims(data, axis=0).shape)
        if len(data.shape) == 2:
            data4 = np.expand_dims(np.expand_dims(data, axis=0), axis=0)
        nf, ns, n1, n2 = data4.shape

        ir = refp[0] % 100
        k1 = np.arange(0, n1 // N) * N + ir + N // 2
        ir = refp[1] % 100
        m1 = np.arange(0, n2 // N) * N + ir + N // 2

        i0 = refp[0] - N / 2
        j0 = refp[1] - N / 2

        refp_new = [(i0 - k1[0]) // N, (j0 - m1[0]) // N]
        new_incr = incr * N

        rows = []
        print("Input image :")
        print("      size       {:d} x {:d}".format(n1, n2))
        print("      ref pixel  {:.0f}   {:.0f}".format(refp[0], refp[1]))
        print("Output image :")
        print("      size       {:d} x {:d}".format(len(k1), len(m1)))
        print("      ref pixel  {:.0f}   {:.0f}".format(refp_new[0], refp_new[1]))
        print("      cell size {0:d} x {0:d} input pixels ".format(N))

        for i in k1:

            col = []
            il, iu = i, i + N

            for j in m1:
                jl, ju = j, j + N
                # Mask out zero values - swarp writes masked pixels as 0.0
                subim = np.ma.masked_equal(data4[0, 0, il:iu, jl:ju], 0.0)
                sq = subim.compressed()
                st = np.NaN
                if len(sq) > 100:
                    if statistic == 'rms':
                        x = find_mode(sq - np.median(sq), parameters)
                        try:
                            mo, wd = x
                            st = abs(wd) * factor
                        except:
                            st = np.NaN
                    elif statistic == 'min':
                        st = sq.min()
                    elif statistic == 'rat':
                        st = 0.0
                        if sq.max() > parameters['clip']:
                            # print (sq.min(), sq.max())
                            st = -sq.min() / sq.max()
                    elif statistic == 'iqr':
                        st = factor * iqr(sq)
                    elif statistic == 'med':
                        st = np.median(sq)
                    elif statistic == 'std':
                        st = np.std(sq)
                else:
                    st = np.NaN
                col.append(st)
            rows.append(col)
        substd = np.array(rows)
        substd.min(), substd.max(), substd.shape, np.median(substd)

        substduJy = np.ma.masked_invalid(substd)
        if statistic == 'med':
            y = substduJy
        else:
            y = np.ma.masked_less(substduJy, 0.0)

        s_im = casa_im.subimage(dropdegenerate=False)
        co_new = s_im.coordinates()
        co_new["direction"].set_referencepixel(refp_new)
        co_new["direction"].set_increment(new_incr)

        ys = np.float32(y)
        co_new.summary()

        if len(co_new.get_referencepixel()) > 1:
            new_shape = [1, 1] + list(ys.shape)
        else:
            new_shape = ys.shape

        out_data = np.reshape(ys, new_shape)
        print(" shapes ", ys.shape, new_shape, out_data.shape)
        print(co_new.get_referencepixel())
        im_new = cim.image(casa_temp, shape=new_shape, coordsys=co_new)
        im_new.put(out_data)

        im_new.tofits(str(out_name))
        print('Written {} to {}'.format(statistic, out_name))

        del im_new
        shutil.rmtree(casa_temp)

        # Now fix the header in astropy
        hdu_in = fits.open(str(in_file))
        hdulist = fits.open(str(out_name), 'update')
        hdr1 = hdulist[0].header

        hdr1['BUNIT'] = 'Jy/beam'
        hdr1['BSCALE'] = (1.0e-6, 'PHYSICAL = PIXEL*BSCALE + BZERO')
        hdulist.flush()


    mos_stats = {'MINIMUM': fmin, 'MAXIMUM': fmax, 'NPIXV': npixv}
    stats = do_statistics(y, new_incr, do_mask)
    return mos_stats, stats, fname
