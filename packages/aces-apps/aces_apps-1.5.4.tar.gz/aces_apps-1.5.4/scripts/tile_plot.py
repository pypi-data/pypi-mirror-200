#!/usr/bin/env python
from __future__ import print_function

import time
import argparse as ap
import sys
import os
import re

import numpy as np
import matplotlib as mpl

mpl.use('Agg')  # this line must precede pylab import to suppress display
import matplotlib.pylab as plt  # noqa

import aces.obsplan.tile as tile  # noqa
from aces.obsplan.sphere_plotting import SphereView  # noqa

from askap.footprint import Skypos  # noqa
from askap.parset import ParameterSet  # noqa

from aces.obsplan.config import ACESConfig  # noqa
from aces.obsplan import logger  # noqa
from askap import logging  # noqa
from askap.coordinates import parse_direction  # noqa
from aces.askapdata.schedblock import SchedulingBlock  # noqa

explanation = """

Explanation

tile_plot.py produces three files for displaying pointing information from an observing parset or from the SBID of an
observation. They are:
 - <xxx>.png
 - <xxx>.ann
 - <xxx>_footprint.sh

where <xxx> is either the parset name or the SBID. For example:

> tile_plot.py RACS_test3_1.05

access the parset RACS_test3_1.05.parset (which must exist in the working directory) and yields:
 - RACS_test3_1.05.png
 - RACS_test3_1.05.ann
 - RACS_test3_1.05_footprint.sh

whereas
> tile_plot.py 8545
yields:  SBID_8545.png,  SBID_8545.ann, SBID_8545_footprint.sh

The .png file is a plot of the whole sky with tiles marked.
The .ann fle is an overlay file suitable for kvis
The .reg fle is an overlay file using DS9 syntax
The x_footprint.sh file is a bash script that will execute footprint-plan.py for each tile to generate lists of
beam positions and kvis overlay files, one per tile, showing the beam positions.

"""
description = """
Description goes here

"""

# todo: sort plotting projections

FORMAT_FILE = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
FORMAT_CONSOLE = '%(name)s - %(levelname)s - %(message)s'
formatter_console = logging.Formatter(FORMAT_CONSOLE)
formatter_file = logging.Formatter(FORMAT_FILE)
timestr = time.strftime("%Y%m%d-%H%M%S")
logging.basicConfig(filename='survey-plan-{}.log'.format(timestr), level=logging.DEBUG,
                    filemode='w', format=FORMAT_FILE)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(formatter_console)
logging.getLogger('').addHandler(console)


# logger.addHandler(console)


def arg_init():
    aces_cfg = ACESConfig()
    # fp_factory = aces_cfg.footprint_factory
    # fp_names = [f for f in fp_factory.get_footprint_names() if f.startswith('ak:')]

    # Build some help information:

    epilog = '\nSee -x for more explanation'
    north_lim = 48.2

    parser = ap.ArgumentParser(prog='tile_plot', formatter_class=ap.RawDescriptionHelpFormatter,
                               description=description,
                               epilog=epilog)
    parser.add_argument('label', nargs='+', help="Survey label or SB integer identifier")
    parser.add_argument('-x', '--explain', action='store_true', help="Give an expanded explanation")
    parser.add_argument('-v', '--verbose', action='store_true', help="Print extra information to the screen")
    parser.add_argument('-t', '--transform', type=int, default=0, choices=[0, 1, 2, 3, 4],
                        help="Projection [%(default)d]")
    parser.add_argument('-H', '--horiz', nargs=2, type=float, default=[0., 360.], help="Horizontal limits (degrees)")
    parser.add_argument('-V', '--vertical', nargs='*', type=float, default=[-90., north_lim],
                        help="Vertical limits (degrees)")
    # parser.add_argument('-a', '--show_all', action='store_true', help="Show whole tiling")
    parser.add_argument('-s', '--shift', action='store_true', help="Shift tiles for tile-interleave")
    parser.add_argument('-i', '--show_ident', action='store_true', help="Label each tile with ID")
    parser.add_argument('-u', '--subpoint', metavar="'RA,Dec'", help="J2000 position projected centre",
                        default=[0.0, 0.0], action=Celpos)
    parser.add_argument('-p', '--polygons', default="", help="File defining polygons to draw")
    parser.add_argument('-l', '--interleaf', default='ABCD', help='Interleaf to plot : all plotted if -l omitted')
    return parser, aces_cfg


class Celpos(ap.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed")
        super(Celpos, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        logger.debug('ACTION : %r %r %r' % (namespace, values, option_string))
        a, b = parse_direction(values)
        rp = [np.radians(a), np.radians(b)]
        # noinspection PyUnresolvedReferences
        setattr(namespace, self.dest, rp)


class WidHt(ap.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        logger.debug('ACTION : %r %r %r' % (namespace, values, option_string))
        # print 'WidHt : ', values
        a, b = [q for q in values.split(",") if len(q) > 0]
        rp = [int(a), int(b)]
        # noinspection PyUnresolvedReferences
        setattr(namespace, self.dest, rp)


def float_pair(arg):
    return [float(a) for a in arg.split(',')]


class TwoFloats(ap.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        logger.debug('ACTION : %r %r %r' % (namespace, values, option_string))
        a, b = [q for q in values.split(",") if len(q) > 0]
        rp = [float(a), float(b)]
        # noinspection PyUnresolvedReferences
        setattr(namespace, self.dest, rp)


def prefix(word, pfx):
    if word.startswith(pfx):
        return word
    else:
        return pfx + word


def prepare_tiles(idents, tile_positions, do_label=True):
    n_tiles = 0
    t_pos = []
    tile_corners = []
    fpcmd = []
    over_ann = []
    over_ds9 = []
    # print('prepare_tiles (idents) : ', idents)
    print(len(tile_positions))
    for ident in idents:
        tp = tile_positions[ident]
        # print (id, tp)
        ti = tile.Tile(ident, tp[0], tp[1], tp[2])
        n_tiles += 1
        # print('# ', id, ti.name, ti.skypos, ti.posang)
        t_pos.append(ti.j2000)
        cs = ti.get_corners()
        cs = np.concatenate((cs, cs[:1]))
        tile_corners.append(cs)
        fpcmd.append(ti.get_footprint_cmd())
        over_ann.append(ti.get_overlay(kind='kvis'))
        over_ds9.append(ti.get_overlay(kind='ds9'))
        if do_label:
            over_ds9.append(ti.get_overlay_label("", kind='ds9'))
    return t_pos, tile_corners, fpcmd, over_ann, over_ds9


def get_idents(targets):
    ks0 = [a.split('.')[0] for a in targets.keys()]
    ks = []
    for a in ks0:
        if a not in ks:
            if re.match("src[0-9]+", a):
                ks.append(a)
    return [int(a[3:]) for a in ks]


def main():
    # parse command line options
    parser, aces_cfg = arg_init()
    args = parser.parse_args()
    if args.verbose:
        print("ARGS = ", args)
    if args.explain:
        print(explanation)
        return

    # Establish output file names, and initialise
    user_input = args.label
    parset = ParameterSet()
    if user_input[0].isdigit():
        sbid = int(user_input[0])
        try:
            sb = SchedulingBlock(sbid)
        # except Ice.ConnectTimeoutException:
        except:
            print('No connection to SchedBlocks')
            return 0
        par = sb.get_parameters()
        var = sb.get_variables()
        for k, v in var.items():
            if 'xec' in k:
                print(k, v)
        for k, v in par.items():
            parset.set_value(k, v)
        label = "SBID_{:d}".format(sbid)
    else:
        label = args.label[0]
        parset_name = "{}.parset".format(label)
        parset = ParameterSet(parset_name)

    polygons = []
    if args.polygons:
        poly_file = args.polygons
        if os.path.exists(poly_file):
            polygons = tile.get_polygons(poly_file)

    plot_interleaf = args.interleaf
    # todo: Decide whether tile selection is a function to be supported.
    hr = np.radians(np.array(args.horiz))
    vr = np.radians(np.array(args.vertical))
    if hr[0] < 0.0:
        hr[0] += 2.0 * np.pi
    if hr[1] < 0.0:
        hr[1] += 2.0 * np.pi

    show_all = True
    show_selected = False
    show_ident = args.show_ident

    kvis_ann_name = '{}.ann'.format(label)
    ds9_name = '{}.reg'.format(label)
    footprint_cmd_name = '{}_footprint.sh'.format(label)
    plot_file_name = '{}.png'.format(label)

    ann = open(kvis_ann_name, 'w')
    s1 = 'COLOR GREEN'
    ann.write(s1 + '\n')

    ds9 = open(ds9_name, 'w')

    fpcmds = open(footprint_cmd_name, 'w')

    fp_factory = aces_cfg.footprint_factory
    name = parset['common.target.src%d.footprint.name']
    beam_pitch = parset['common.target.src%d.footprint.pitch'] * np.pi / 180.0
    bf_pa = parset['common.target.src%d.footprint.rotation']
    name = prefix(name, 'ak:')

    fp = fp_factory.make_footprint(name, beam_pitch)
    if 'common.targets' in parset:
        targets = parset['common.targets']
    else:
        ks = parset.to_dict()['common']['target']
        targets = [a for a in ks.keys() if '%' not in a]

    tiling = {'idents': [], 'tiles': []}
    for target in targets:
        ident = int(re.findall('[0-9]+', target)[0])
        fd = parset['common.target.{}.field_direction'.format(target)]
        pa = parset['common.target.{}.pol_axis'.format(target)]
        na = parset['common.target.{}.field_name'.format(target)]
        il = na[-1]
        # If field names lack interleaf designator, select what would have been 'A'.
        # (See tile.py get_parset_entry)
        if il in '0123456789':
            il = 'A'
        if il in plot_interleaf:
            tpos = Skypos(fd[0], fd[1])
            ra = tpos.ra
            dec = tpos.dec
            tpa = bf_pa + float(pa[1])
            tiling['tiles'].append((ra, dec, tpa))
            tiling['idents'].append(ident)
    # Assume the following defaults
    origin = Skypos(0.0, 0.0)
    bf_pa = 45.0
    coord = 'J2000'
    tile.Tile.initialise(origin, label, fp, bf_pa, coord=coord)

    tile_pos_list = tiling['tiles']
    tile_idents = tiling['idents']
    tile_positions = {}
    idents = []
    for ident, tp in zip(tile_idents, tile_pos_list):
        tile_positions[ident] = tp
        h, v, p = tp
        if ident == 20:
            print("{:d}  {:f} {:f}".format(ident, h, v))
        h = (h + 2.0 * np.pi) % (2.0 * np.pi)
        # print 'for tile_ident ... ', tp, hr, vr
        if hr[0] < hr[1]:
            h_range = hr[0] <= h <= hr[1]
        else:
            h_range = hr[0] <= h or h < hr[1]
        if h_range and vr[0] <= tp[1] <= vr[1]:
            idents.append(ident)

    t_pos, tile_corners, fpcmd, o_ann, o_ds9 = prepare_tiles(idents, tile_positions, do_label=show_ident)
    print('All tiles : ', len(t_pos))
    for cmd in fpcmd:
        fpcmds.write(cmd)
    fpcmds.close()

    for cmd in o_ann:
        ann.write(cmd + '\n')
    ann.close()

    for cmd in o_ds9:
        ds9.write(cmd + '\n')
    ds9.close()

    # Produce a png plot
    fig = plt.Figure(figsize=[8., 8.])
    # ax.set_aspect(1.0)
    proj = args.transform
    projname = {0: 'CAR', 1: 'ORTH', 2: 'MOLL', 3: 'aitoff', 4: 'hammer'}
    sphere = SphereView(projection=projname[proj])
    subp = Skypos(args.subpoint[0], args.subpoint[1])
    sphere.set_subpoint(subp)
    sphere.draw_outline()
    sphere.draw_coord_grid()
    sphere.axis.set_axis_off()
    # sphere.draw_label()
    # rgb = [0.99197232, 0.54131488, 0.23197232]
    rgb = [0.1, 0.4, 0.7]

    style = {"alpha": 0.3, 'color': rgb}
    poly_style = {"lw": 0.5, 'color': rgb, "ls": "-."}
    for cs in tile_corners:
        sphere.join_gc(cs)
        sphere.join_gc_fill(cs, **style)
    if show_all:
        if show_ident and not show_selected:
            txt_style = {"fontsize": 4}
            for i, p in zip(idents, t_pos):
                sphere.draw_text(p, "{:d}".format(i), **txt_style)
    if show_selected:
        if show_ident:
            for i, p in zip(idents, t_pos):
                sphere.draw_text(p, "{:d}".format(i))

    for poly in polygons:
        sphere.join_gc(poly, close=True, **poly_style)

    plt.savefig(plot_file_name, dpi=300, bbox_inches='tight', transparent=True)
    print('trans = True')
    n_tiles = len(idents)
    print("{:d} tiles selected for requested coverage".format(n_tiles))


if __name__ == "__main__":
    sys.exit(main())
