#!/usr/bin/env python
"""
Script to read and plot beam fits.

Copyright (C) CSIRO 2017
"""

import argparse as ap
import re
import sys

import matplotlib.pylab as plt
import numpy as np
from numpy import pi

from aces.beamset import beamfactory as bf

explanation = ""

HELP_START = """This provides an example that reads and displays beam model parameters.
There are several numbered options :
1. POSITION:  Plot the mean position difference between antennas over all beams.
              Select channel, antennas.
2. AXES:      Plot major and minor axes of selected beams as a function of frequency.
              Select beams.
3. SHAPE:     Plot the mean axis length and eccentricity of selected beams against frequency.
              Select beams
4. FOOTPRINT: Plot the fitted ellipses for all beams at a selected frequency, for selected antennas.
              Select channel
5. FLAGS:     Show flagged fits over all antennas, beams vs frequency channels

6. GOODNESS:  Show fit residuals over all antennas, beams vs frequency channels

7. SHAPE-STATS: Plot shape statistics over antennas as function of frequency. Select a beam, and
                the desired set of antennas.

8. SIZE-STATS: Plot shape statistics over frequency as function of beam. Select 
                the desired set of antennas.


"""
POSITION = 1
AXES = 2
SHAPE = 3
FOOTPRINT = 4
FLAGS = 5
GOODNESS = 6
STATS = 7
SIZESTATS = 8

# Dish diameter
DISHDIAMETER = 12.0


def arg_init():
    """Define the interprestation of command line arguments.
    """
    parser = ap.ArgumentParser(prog='measure_usage',
                               formatter_class=ap.RawDescriptionHelpFormatter,
                               description=HELP_START,
                               epilog='See -x for more explanation')
    parser.add_argument('inFile', nargs="?", help="Beam measure file (hdf5 format)")
    parser.add_argument('-o', '--option', default=1, type=int, help="Option number [%(default)d]")
    parser.add_argument('-c', '--channel', default=[1], action=intList, help="Channel number [%(default)s]")
    parser.add_argument('-a', '--antennas', default=list(range(1, 37)), action=intList,
                        help="Antennas to select [%(default)s]")
    parser.add_argument('-b', '--beams', default=list(range(37)), action=intList,
                        help="Antennas to select [%(default)s]")
    parser.add_argument('-p', '--polarizations', default=['XX', 'YY'], action=polList,
                        help="Polarizations to model [%(default)s]")
    parser.add_argument('-d', '--display', action='store_true', help="Display plot on screen")
    parser.add_argument('-m', '--movie', action='store_true', help="Plot sequence for animation")
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


class polList(ap.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        # print 'ACTION : %r %r %r' % (namespace, values, option_string)
        pols = ['XX', 'YY', 'XY', 'YX', 'I', 'Q', 'U', 'V']
        rp = []
        for p in pols:
            if p in values:
                rp.append(p)
        setattr(namespace, self.dest, rp)


def show_plot(do_show):
    print("Displaying plot ...")
    if do_show:
        plt.show()


def make_gen(shape):
    """Shape is always 5 long
    """
    for i in range(shape[0]):
        for j in range(shape[1]):
            for k in range(shape[2]):
                for l in range(shape[3]):
                    for m in range(shape[4]):
                        yield np.s_[i, j, k, l, m]


def unlink_wrap(dat, lims=[-np.pi, np.pi], thresh=0.95):
    """
    Iterate over contiguous regions of `dat` (i.e. where it does not
    jump from near one limit to the other).

    This function returns an iterator object that yields slice
    objects, which index the contiguous portions of `dat`.

    This function implicitly assumes that all points in `dat` fall
    within `lims`.

    """
    jump = np.nonzero(np.abs(np.diff(dat)) > ((lims[1] - lims[0]) * thresh))[0]
    lasti = 0
    for ind in jump:
        yield slice(lasti, ind + 1)
        lasti = ind + 1
    yield slice(lasti, len(dat))


# noinspection PyTypeChecker
def main():
    """All the processing starts in here.
    """
    # parse command line options

    args = arg_init().parse_args()
    if args.explain:
        print(explanation)
        sys.exit(0)
    if args.verbose:
        print("ARGS = ", args)

    if args.inFile:
        infile = args.inFile
    else:
        print("Try -h for help")
        sys.exit(0)

    verbose = args.verbose
    do_show = args.display
    for_animation = args.movie
    pfile = None

    # Read the new hdf5 file, extract a particular map, interpolate and display.
    mod = bf.load_beamset_class(infile)
    mod.print_summary()
    frequencies = mod.metadata['frequencies']
    nchans = len(frequencies)

    option = args.option

    ants = [a for a in args.antennas if a in mod.metadata['antennas']]
    beams = np.array([a for a in args.beams if a in mod.metadata['beams']])
    pols = [a for a in args.polarizations if a in mod.metadata['polarizations']]
    assert len(ants) > 0, "No selected antennas in input file"
    assert len(beams) > 0, "No selected beams in input file"
    assert len(pols) > 0, "No selected polarizations in input file"

    if mod.metadata['holographySBID'] > 0:
        sbid = mod.metadata['holographySBID']
    else:
        print(infile)
        sbid = int(re.findall('[0-9]{4}', infile)[0])

    if option in [POSITION, AXES, SHAPE, STATS, SIZESTATS]:
        seli, selv = None, None
        if option == POSITION:
            # This section only works for a single channel: choose the first if more than one given
            # Also, it looks for mean position across beams, so select all.
            ichan = args.channel[0]
            if len(args.channel) > 1:
                print('Plotting for channel {:d} only'.format(ichan))
            seli = {'times': 0, 'beams': 'all', 'channels': ichan}
            selv = {'ant': ants, 'pol': pols[0]}
        elif option in [AXES, SHAPE, STATS]:
            # These options explore variation with frequency; take all channels
            seli = {'times': 0, 'channels': list(range(nchans))}
            selv = {'ant': ants, 'beams': beams, 'pol': pols[0]}
        elif option in [SIZESTATS]:
            # This option explotes variation with beam, averaged over frequency
            seli = {'times': 0, 'channels': list(range(nchans))}
            selv = {'ant': ants, 'beams': beams, 'pol': pols[0]}

        # Use these to construct the iterator for source and target arrays.
        try:
            selector, sub_shape = mod.get_selector_subshape(seli, selv)
        except ValueError as ve:
            print('Failure: ', ve)
            sys.exit()

        out_sel = make_gen(sub_shape)

        cnts = np.ma.masked_array(np.zeros(sub_shape + [2]), mask=False)
        axls = np.ma.masked_array(np.zeros(sub_shape + [2]), mask=False)
        angls = np.ma.masked_array(np.zeros(sub_shape), mask=False)

        frqs = np.zeros(sub_shape)
        out_flags = np.zeros(sub_shape, np.bool)
        offsets = np.zeros(sub_shape + [2])
        for s, so in zip(selector, out_sel):
            freq = frequencies[s[4]]
            frqs[so] = freq
            out_flags[so] = mod.flags[s]
            offsets[so] = mod.get_beam_offset(s[2]) * [-1, 1]
            if not mod.flags[s]:
                mea = mod.get_model(s)
                mea.set_ang_unit('degree')
                cnt = mea.get_centre()
                angl = mea.get_position_angle()
                axl = mea.get_axes() * 2
                cnts[so] = cnt
                axls[so] = axl
                angls[so] = angl

        # Transfer flags to the derived quantities:
        cnts.mask = np.tile(np.expand_dims(out_flags, axis=5), 2)
        axls.mask = np.tile(np.expand_dims(out_flags, axis=5), 2)
        angls.mask = out_flags

        lambonD = 300. / frequencies / DISHDIAMETER

        if option == POSITION:
            # Next line very dodgy. Needs to be improved.
            # Now (2018-05-23) improved: detect degenerate case when only one antenna; add dimension so that
            # all the slices below work.
            y = np.squeeze(cnts)
            if y.ndim == 2:
                y = np.expand_dims(y, 0)

            yrel = (cnts - offsets) * 60.
            yma = np.squeeze(yrel.mean(axis=2))
            ystd = np.squeeze(yrel.std(axis=2))
            fig, axis = plt.subplots(1, 1)
            axis.set_aspect('equal')
            plt.plot(yma[:, 0], yma[:, 1], 'ok')
            to = -0.5
            print("\n         dx              dy               Dist (arcmin)")
            if yrel.shape[2] > 1:
                for ia in range(0, len(ants)):
                    dx, dy = yma[ia, :]
                    sx, sy = ystd[ia, :]
                    dist = np.sqrt(dx * dx + dy * dy)
                    print("AK{:02d}  {:6.2f} ({:5.2f})  {:6.2f} ({:5.2f})    {:5.1f}".format(ants[ia], dx, sx, dy, sy,
                                                                                             dist))
                    plt.errorbar(yma[ia, 0], yma[ia, 1], xerr=sx, yerr=sy, ecolor='k')
                    plt.text(yma[ia, 0] + to, yma[ia, 1] + to, "{:d}".format(selv["ant"][ia]), va="top", ha="right")

            plt.grid()
            plt.xlabel('Offsets from expected (arcmin)')
            plt.ylabel('Offsets from expected (arcmin)')
            plt.title(infile + ' ' + selv['pol'])
            pfile = '{:d}_offsets_{}.png'.format(sbid, selv['pol'])
            fig.savefig(pfile, dpi=300)
            show_plot(do_show)
            # End OPTION 1 POSITION

        if option in [AXES, SHAPE, STATS]:
            pol = selv['pol']
            x = frqs[0, 0, 0, 0, :]
            # cols = ['k', 'b', 'r']

            if option == STATS:
                # Generate array y with shape (nants, nbeams, nfreq, axes)
                pc_lower = 16.
                pc_upper = 84.
                for i, ib in enumerate(beams):
                    y = np.radians(axls[0, :, i, 0, :, :])
                    y = np.ma.masked_array(y, mask=(y == 0.0))
                    width = y.mean(axis=2)
                    ecc = np.sqrt(1 - y[:, :, 1] / y[:, :, 0])
                    ecc = np.ma.masked_array(ecc, mask=(ecc == 0.0))
                    pa = angls[0, :, i, 0, :]
                    pa = np.ma.masked_array(pa, mask=(pa == 0.0))

                    ymed = np.ma.masked_invalid([np.median(width[:, ic]) for ic in range(nchans)])
                    ymax = np.ma.masked_array([np.max(width[:, ic]) for ic in range(nchans)], mask=ymed.mask)
                    ymin = np.ma.masked_array([np.min(width[:, ic]) for ic in range(nchans)], mask=ymed.mask)
                    yp32 = np.ma.masked_array([np.percentile(width[:, ic], pc_lower) for ic in range(nchans)],
                                              mask=ymed.mask)
                    yp68 = np.ma.masked_array([np.percentile(width[:, ic], pc_upper) for ic in range(nchans)],
                                              mask=ymed.mask)

                    ymed = np.ma.masked_values(ymed, 0.0) / lambonD
                    ymin = np.ma.masked_array(ymin, mask=ymed.mask) / lambonD
                    ymax = np.ma.masked_array(ymax, mask=ymed.mask) / lambonD
                    yp32 = np.ma.masked_array(yp32, mask=ymed.mask) / lambonD
                    yp68 = np.ma.masked_array(yp68, mask=ymed.mask) / lambonD

                    emed = np.ma.masked_invalid([np.median(ecc[:, ic]) for ic in range(nchans)])
                    emed = np.ma.masked_equal(emed, 0.0)
                    emax = np.ma.masked_array([np.max(ecc[:, ic]) for ic in range(nchans)], mask=emed.mask)
                    emin = np.ma.masked_array([np.min(ecc[:, ic]) for ic in range(nchans)], mask=emed.mask)
                    ep32 = np.ma.masked_array([np.percentile(ecc[:, ic], pc_lower) for ic in range(nchans)],
                                              mask=emed.mask)
                    ep68 = np.ma.masked_array([np.percentile(ecc[:, ic], pc_upper) for ic in range(nchans)],
                                              mask=emed.mask)
                    pmed = np.ma.masked_invalid([np.median(pa[:, ic]) for ic in range(nchans)])
                    pmed = np.ma.masked_equal(pmed, 0.0)
                    pmax = np.ma.masked_array([np.max(pa[:, ic]) for ic in range(nchans)], mask=pmed.mask)
                    pmin = np.ma.masked_array([np.min(pa[:, ic]) for ic in range(nchans)], mask=pmed.mask)
                    pp32 = np.ma.masked_array([np.percentile(pa[:, ic], pc_lower) for ic in range(nchans)],
                                              mask=pmed.mask)
                    pp68 = np.ma.masked_array([np.percentile(pa[:, ic], pc_upper) for ic in range(nchans)],
                                              mask=pmed.mask)
                    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex='col', figsize=(8, 6))
                    fig.subplots_adjust(hspace=0.04)

                    lwid = 2.5
                    range_args = {'c': '0.85', 'lw': lwid}
                    rms_args = {'c': '0.6', 'lw': lwid}
                    med_args = {'c': '0.0', 'lw': lwid}

                    for xi, y1, y2 in zip(x, ymin, ymax):
                        ax1.plot([xi, xi], [y1, y2], **range_args)
                    ax1.plot([], [], label="range", **range_args)

                    for xi, y1, y2 in zip(x, yp32, yp68):
                        ax1.plot([xi, xi], [y1, y2], **rms_args)
                    ax1.plot([], [], label=r'$\pm 1 \sigma$', **rms_args)
                    ax1.plot(x, ymed, label="Median", **med_args)

                    for xi, y1, y2 in zip(x, emin, emax):
                        ax2.plot([xi, xi], [y1, y2], **range_args)
                    for xi, y1, y2 in zip(x, ep32, ep68):
                        ax2.plot([xi, xi], [y1, y2], **rms_args)
                    ax2.plot(x, emed, **med_args)

                    for xi, y1, y2 in zip(x, pmin, pmax):
                        ax3.plot([xi, xi], [y1, y2], **range_args)
                    for xi, y1, y2 in zip(x, pp32, pp68):
                        ax3.plot([xi, xi], [y1, y2], **rms_args)
                    ax3.plot(x, pmed, **med_args)

                    ax1.set_ylim(0.84, 1.41)
                    ax2.set_ylim(0.0, 0.6)
                    ax3.set_ylim(0.0, 180.0)
                    ax1.set_ylabel(r'Mean axis length ($\lambda$/D)')
                    ax2.set_ylabel('Eccentricity')
                    ax3.set_ylabel('Pos angle (deg)')
                    ax1.grid()
                    ax2.grid()
                    ax3.grid()
                    ax1.legend()
                    ax2.set_xlabel('Frequency (MHz)')
                    ax1.set_title(" SBID {:d}  Beam {:d}  Pol {}. Distribution over {:d} antennas".
                                  format(sbid, beams[i], pol, y.shape[0]))
                    pfile = '{:d}_beamshape-distribution_B{:02d}-{}.png'.format(sbid, beams[i], pol)
                    fig.savefig(pfile, dpi=300)
                    show_plot(do_show)
                    plt.close()
                    # END OPTION 7 STATS
            else:
                for ia in range(len(ants)):
                    ant = ants[ia]
                    # Generate array y with shape (nbeams, npols, nfreq)
                    y = np.radians(axls[0, ia, :, 0, :, :])
                    y = np.ma.masked_array(y, mask=(y == 0.0))
                    pa = angls[0, ia, :, 0, :]
                    if option == AXES:
                        fig, axis = plt.subplots(1, 1)
                        for ib, beam in enumerate(beams):
                            plt.plot(x, y[ib, :, 0] / lambonD, lw=1.5, label="Beam %2d" % beam)
                            plt.plot(x, y[ib, :, 1] / lambonD, lw=1.5)
                        plt.ylim(0.74, 1.51)
                        plt.ylabel(r'Mean axis length ($\lambda$/D)')
                        plt.grid()
                        plt.legend()
                        plt.xlabel('Frequency (MHz)')
                        plt.title("AK%02d Pol %s" % (ant, pol))
                        pfile = '{:d}_AK{:02d}_beamshape.png'.format(sbid, ant)
                        fig.savefig(pfile, dpi=300)
                        show_plot(do_show)

                    if option == SHAPE:
                        fig, axes = plt.subplots(3, 1, sharex='col')
                        ax1, ax2, ax3 = axes
                        plt.subplots_adjust(hspace=0.04)
                        kw_args = {'c': 'k', 'lw': 1.5}
                        for ib, beam in enumerate(beams):
                            ax1.plot(x, y[ib, :, :].mean(axis=1) / lambonD,
                                     label="Beam %2d" % beam, **kw_args)
                            ax2.plot(x, np.sqrt(1 - y[ib, :, 1] / y[ib, :, 0]),
                                     **kw_args)
                            paw = pa[ib, :]
                            for slc in unlink_wrap(paw, lims=[0.0, 180.0]):
                                ax3.plot(x[slc], paw[slc], **kw_args)

                            # ax3.plot(x, pa[ib, :], lw=1.5)
                        ax1.set_ylim(0.74, 1.51)
                        ax2.set_ylim(0.0, 0.6)
                        ax3.set_ylim(0.0, 180.0)
                        ax1.grid()
                        ax2.grid()
                        ax3.grid()
                        ax1.legend()
                        plt.xlabel('Frequency (MHz)')
                        ax1.set_ylabel(r'Mean axis length ($\lambda$/D)')
                        ax2.set_ylabel('Eccentricity')
                        ax3.set_ylabel('Pos angle (deg)')
                        ax1.set_title("AK%02d Pol %s" % (ant, pol))
                        pfile = '{:d}_AK{:02d}_{}_sizeecc.png'.format(sbid, ant, pol)
                        fig.savefig(pfile, dpi=300)
                        show_plot(do_show)
        if option == SIZESTATS:
            print("axls shape ", axls.shape)
            pol = selv['pol']
            ant = ants[0]
            meanaxes = np.radians(axls.mean(axis=5))
            for i in range(axls.shape[2]):
                meanaxes[0, 0, i, 0, :] /= lambonD
            meanfrq = np.squeeze(meanaxes.mean(axis=4))
            std_frq = np.squeeze(meanaxes.std(axis=4))
            for m, s in zip(meanfrq, std_frq):
                print("  {:.3f}  {:.3f}".format(m, s))
            print("{:.3f} {:.3f}".format(meanfrq.mean(), np.median(meanfrq)))
            fig, axes = plt.subplots(1, 1, figsize=(8., 4.))
            plt.errorbar(beams - 1, meanfrq, yerr=std_frq, fmt='o-', color='k')
            plt.xlabel('Beam number')
            plt.ylabel(r'Mean axis length ($\lambda$/D)')
            plt.title("AK%02d Pol %s" % (ant, pol))
            plt.grid()
            pfile = '{:d}_AK{:02d}_{}_size_beams.png'.format(sbid, ant, pol)
            fig.savefig(pfile, dpi=300)
            show_plot(do_show)

    elif option == FOOTPRINT:
        pols = mod.metadata['polarizations']
        npol = len(pols)
        ts = np.arange(0.0, 2.0 * pi + 0.1, 0.1)
        fs = (9, 6)
        if len(pols) == 3:
            fs = (14, 6)
        elif len(pols) == 2:
            fs = (11.8, 6)

        # Now establish the loop over freuency channels
        seli_ch = {'times': 0, 'antennas': 0, 'beams': 0, 'polarizations': 0, 'channels': args.channel}
        try:
            sel_ch = mod.get_selector(seli_ch)
        except ValueError as ve:
            print('Failure: ', ve)
            sys.exit()

        schan = 0
        for sch in sel_ch:
            ichan = sch[4]
            seli = {'times': 0, 'channels': ichan}
            for ant in ants:
                selv = {'antennas': ant, 'beams': mod.metadata['beams'], 'pol': pols}
                try:
                    sel, sub_shape = mod.get_selector_subshape(seli, selv)
                except ValueError as ve:
                    print('Failure: ', ve)
                    sys.exit()

                fig, axes = plt.subplots(1, npol, sharey='row', figsize=fs)
                fig.subplots_adjust(wspace=0.02)
                do_save_file = False
                if npol == 1:
                    pol = pols[0]
                    ax = {pol: axes}
                else:
                    ax = {}
                    for j, pol in enumerate(pols):
                        ax[pol] = axes[j]

                for pol in pols:
                    ax[pol].set_aspect('equal')
                for sm in sel:
                    vecm = mod.get_vector(sm)
                    t, a, beam, pol, freq = vecm
                    # Plot the requested beam position (from footprint).
                    # TBD: make these symbols always in the background. ??
                    x_off, y_off = mod.get_beam_offset(sm[2])
                    x_off *= -1.0
                    ax[pol].plot([x_off], [y_off], 'o', c='0.7', mec='none', ms=5, zorder=-1)

                    if mod.flags[sm]:
                        if verbose:
                            print("beam {:d} flagged".format(beam))
                    else:
                        mea = mod.get_model(sm)
                        mea.set_ang_unit('degree')
                        if mea.is_good_fit():
                            cnt = mea.get_centre()
                            angl = mea.get_major_angle()
                            axl = mea.get_axes()
                            if beam in range(1,37):
                                print('beam {:d} angle = {:.2f} {:.2f} {:.2f}'.format(beam, angl, axl[0], axl[1]))

                            xy0 = mea.get_locus50(ts)
                            xmaj, ymaj = mea.get_locus50([0.0, np.pi])
                            xt, yt = cnt

                            ax[pol].text(xt, yt, "{:d}".format(beam), color='0.5', fontsize=9,
                                         ha='left', va='center')
                            ax[pol].plot([xt], [yt], 'ok', ms=3)
                            ax[pol].plot(xy0[0], xy0[1], 'k')
                            ax[pol].plot(xmaj, ymaj, '-k')
                            do_save_file = True
                for pol in pols:
                    ax[pol].grid()
                    ax[pol].set_xlim(-4.0, 4.0)
                    ax[pol].set_ylim(-4.0, 4.0)
                    ax[pol].set_title(pol)
                fig.suptitle("%d AK%02d  %.0f MHz" % (sbid, ant, freq))
                show_plot(do_show)
                if do_save_file:
                    if for_animation:
                        pfile = "{:d}_AK{:02d}_c-{:03d}_beams.png".format(sbid, ant, schan)
                        schan += 1
                    else:
                        pfile = "{:d}_AK{:02d}_{:04d}_beams.png".format(sbid, ant, int(freq + 0.5))
                    fig.savefig(pfile, dpi=300)
                    print("Plot saved to {}".format(pfile))
                else:
                    print("No valid models for AK{:02d} channel {:d}".format(ant, ichan))
                plt.close()

    elif option == FLAGS:
        na = mod.Na
        nb = mod.Nb
        ny = mod.Nf
        nx = na * nb
        flags = mod.flags
        dflgs = np.zeros([ny, nx], np.bool_)
        for a in range(na):
            j = a * nb
            dflgs[:, j:j + nb] = flags[0, a, :, 0, :].transpose()
        f1, f2 = mod.metadata['frequencies'][[0, -1]]

        fig, axis = plt.subplots(1, 1, figsize=(12., 8.))
        ext = [0.0, na * 1.0, f1, f2]

        ax2 = axis.twinx()
        ax2.plot([2.0, 2.0], [0., mod.Nf], '.w')
        ax2.set_ylabel("Channels")
        ax2.set_ylim(0.0, mod.Nf)
        ax2.set_xlim(ext[0], ext[1])

        axis.imshow(dflgs, origin='lower', aspect='auto', interpolation='nearest',
                           extent=ext, cmap='Greys', vmin=-2.1, vmax=1.1)
        axis.set_xticks(list(range(na)))
        axis.xaxis.set_ticklabels(["  {:02d}".format(a) for a in mod.metadata['antennas']])
        for label in axis.xaxis.get_ticklabels():
            label.set_horizontalalignment('left')

        axis.set_ylabel('Frequency (MHz)')
        axis.set_xlabel('Antennas by number; all beams for each')
        axis.grid(c='w', lw=1)

        axis.set_title('%d flagged beams (I)' % sbid)
        pfile = '{:d}_flags.png'.format(sbid)
        fig.savefig(pfile, dpi=300)
        show_plot(do_show)
        # END option 5 FLAGS

    elif option == GOODNESS:
        na = mod.Na
        nb = mod.Nb
        ny = mod.Nf
        nx = na * nb
        seli = {'times': 0, 'antennas': 'all', 'beams': 'all',
                'polarizations': 0, 'frequencies': 'all'}

        try:
            selector, sub_shape = mod.get_selector_subshape(seli)
        except ValueError as ve:
            print('Failure: ', ve)
            sys.exit()

        d_goodness = np.zeros([ny, nx], np.float)
        for sel in selector:
            it, ia, ib, ip, ich = sel
            z = mod.data[sel][-1]
            d_goodness[ich, ia * nb + ib] = z * 180.0 / pi

        d_goodness = np.ma.masked_equal(d_goodness, 0.0)
        f1, f2 = mod.metadata['frequencies'][[0, -1]]

        fig, axis = plt.subplots(1, 1, figsize=(14., 8.))
        ext = [0, na, f1, f2]
        print("RMS residual range           %f - %f" % (d_goodness.min(), d_goodness.max()))
        vmin = d_goodness[d_goodness > 0.0].min()
        vmax = np.percentile(d_goodness, 90)
        print("RMS residual range (plotted) %f - %f" % (vmin, vmax))
        imsh = axis.imshow(d_goodness, origin='lower', aspect='auto', interpolation='nearest',
                           extent=ext, vmin=vmin, vmax=vmax)
        axis.set_xticks(list(range(na)))
        axis.xaxis.set_ticklabels(["  {:02d}".format(a) for a in mod.metadata['antennas']])
        for label in axis.xaxis.get_ticklabels():
            label.set_horizontalalignment('left')

        axis.set_ylabel('Frequency (MHz)')
        axis.set_xlabel('Antennas by number; all beams for each')
        axis.grid(c='w', lw=1)
        cb1 = plt.colorbar(imsh, orientation="vertical")
        cb1.set_label("Residual rms (deg)")

        axis.set_title('%d rms fit residual (%s)' % (sbid, pols[0]))
        pfile = '{:d}_goodness.png'.format(sbid)
        fig.savefig(pfile, dpi=300)
        show_plot(do_show)
    else:
        print("Unknown option %d" % option)

    if pfile:
        print("Plot file {} written.".format(pfile))


if __name__ == "__main__":
    sys.exit(main())
