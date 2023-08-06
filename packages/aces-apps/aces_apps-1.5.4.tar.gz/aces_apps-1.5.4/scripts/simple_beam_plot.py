#!/usr/bin/env python
"""
Example use of BeamSet and subclasses BeamMeasure.

Copyright (C) CSIRO 2017
"""
import sys
import argparse as ap

import aces.beamset.mapset as ms
import matplotlib.pylab as plt

import numpy as np

explanation = """This provides an example of a simple plotting of beams from a MapSet.
"""
help_start = """Plots beams in the given input file. All beams for the given antenna and
channel number are plotted on a single page. If the beam maps are one-
dimensional (cuts), a line plot is drawn for each. Raw map data are
interpolated onto a finer grid if requested with '-i'.
"""
explanation += "/n%s" % help_start


def arg_init():
    parser = ap.ArgumentParser(prog='simple_beam_plot.py',
                               formatter_class=ap.RawDescriptionHelpFormatter,
                               description=help_start,
                               epilog='See -x for more explanation')
    parser.add_argument('inFile', nargs="?", help="Data file (hdf5 format)")
    parser.add_argument('-o', '--output', default='simple.png',
                        help="Name of plot file [%(default)s]")
    parser.add_argument('-a', '--antenna', type=int, default=4,
                        help="Antenna number to plot [%(default)d]")
    parser.add_argument('-c', '--channel', type=int, default=0,
                        help="Channel to plot [%(default)d]")
    parser.add_argument('-i', '--interp', type=float, default=0.2,
                        help="Interpolation grid spacing [%(default).2f] (deg)")
    parser.add_argument('-g', '--do_log', action='store_true', help="Logarithmic intensity coding")
    parser.add_argument('-0', '--zero_phase', action='store_true', help="Set phase component of raster to zero")
    parser.add_argument('-p', '--plot_phase', action='store_true', help="Plot phase instead of amplitude")
    parser.add_argument('-d', '--display', action='store_true', help="Display plot on screen")
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-x', '--explain', action='store_true',
                        help="Give an expanded explanation")
    return parser


def get_nx_ny(n):
    # for n plots, arrange in a nx by ny grid
    nx = int(np.sqrt(1.0*n))
    ny = int(n/nx)
    if nx*ny < n:
        ny += 1
    return nx, ny


def main():
    # parse command line options
    print("\n     simple plot example\n\n")

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

    do_show = args.display

    # Prepare for plotting.
    plt.clf()
    fig = plt.gcf()
    fig.set_size_inches(6, 6)
    plt.subplots_adjust(wspace=0.04, hspace=0.04)

    # Load MapSet
    maps = ms.MapSet(filename=infile)
    if args.zero_phase:
        maps.set_phase_to_zero()
    maps.print_summary()

    maps.set_interp(args.interp)

    seli = {'times': 'all',
            'beams': 'all',
            'channels': args.channel}
    selv = {'antennas': args.antenna}

    selector = maps.get_selector(indices=seli, values=selv)
    freq = maps.metadata['frequencies']

    # Decide on a plot layout:
    nx, ny = get_nx_ny(maps.Nb)
    ip_label = (nx - 1) * ny + 1
    ip = 1
    for s in selector:
        t, ant, beam, pol, freq = maps.get_vector(s)
        print(ant, beam, pol, freq)
        if args.plot_phase:
            m = maps.get_map(s, maptype='phase', normalise=True)
        else:
            m = maps.get_map(s, maptype='amplitude', normalise=True)
        if m.is_one_dim():
            asp = 'auto'
        else:
            asp = 'equal'
        fig.add_subplot(nx, ny, ip, aspect=asp)
        # Label bottom left patch
        xl, yl = False, False
        if ip == ip_label:
            yl = True
            xl = True
        m.plot(log=args.do_log, xlabels=xl, ylabels=yl)
        plt.grid()
        ip += 1
    fig.suptitle('AK{:02d}  {:d} MHz'.format(ant, int(freq)))
    fname = "beams_AK{:02d}_{:04d}MHz.png".format(ant, int(freq))
    print('savefig ', fname)
    plt.savefig(fname)
    if do_show:
        plt.show()


if __name__ == "__main__":
    sys.exit(main())
