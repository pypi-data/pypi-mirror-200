#!/usr/bin/env python

import argparse as ap
import sys
import os
import time

import aces.obsplan.tile as tile
import numpy as np
from aces.obsplan import logger
from aces.obsplan.config import ACESConfig
from askap import logging
from askap.coordinates import parse_direction
from askap.footprint import Skypos
from askap.parset import ParameterSet, extract

ster_to_sqdeg = (180.0 / np.pi) ** 2

explanation = """

Script tile_sky
===============
This places observing tiles on the celestial sphere to optimise uniformity of sky coverage for a set of ASKAP
observations. The following options are supported:
1. The whole sky is tiled in the fashion described by Aaron Robotham (UWA):  (i) tiles are arranged along small circles
over a latitude band spanning the equator, and (ii) the polar regions are tiled using the same scheme but the small
circles are centred on poles shifted to the equator of the nominated coordinate system.
2. The whole-sky tiling can be masked by a user-supplied polygon: tiles wholly outside the polygon are excluded.
3. Tiles can be placed only over a region defined by a user-defined polygon; in some cases, this method gives a more
efficient distribution of tiles than the second option.

In all cases, tiles north of the telescope's northern limit are excluded.
For the 2nd and 3rd options, several polygons can be given. No check is made for overlap, which could result in
duplicates using option 3.

INPUTS
------
The tiling is controlled with these inputs:
1. -m lat1,lat2  the latitude margins of the small-circle section - (default values [-72,72])
2. -c {J2000,GALAC,MAGEL} specifies the coordinate frame - (default is J2000)
3. -r Origin of the tiling in the chosen coordinates (lon,lat) - (default is [0.0,0.0]
4. -p the beam spacing (pitch) - (default is 0.9 deg)
5. -n the name of the footprint - (default is square_6x6)

User supplied polygons must be presented in a text file with each line corresponding to one polygon described by a
coordinate pair (lon lat) for each vertex. For example, a strip survey along the equator could be:
-40.0 -3.0, 40.0 -3.0, 40.0 3.0, -40.0 3.0
Pairs are separated by commas; longitude and latitude are separated by spaces; values are decimal degrees in the
coordinate system specified by the -c option.
 
The script writes an observing parset file that holds the specifications of each tile wit positions given in J2000
coordinates suitable for ASKAP's control system. However, the script can perform the tiling in other coordinate frames:
currently the supported coordinates are equatorial  ("J2000"), Galactic  ("GALAC") or Magellanic ("MAGEL")
(for Magellanic coordinates see http://adsabs.harvard.edu/abs/2008ApJ...679..432N).

OUTPUTS
-------
The script produces results in several files:
 - <label>.parset  - observing parset; gives the required entries for each tile and its interleaves; at present this
    parset may need editing before submission as an ASKAP observation;
 - <label>.reg - ds9 region file that shows the tile locations and names;
 - <label>.ann - kvis annotations file that shows the tile locations and names on a kvis-displayed image;
 - <label>_footprint_ds9.sh v- shell script to produce plan-footprint.py output with ds9 overlays for each tile;
 - <label>_footprint_kvis.sh - shell script to produce plan-footprint.py output with kvis overlays for each tile.

"""
description = """
This tiles the sky with tiles arranged along small circles over a declination band
within user-specified limits. Outside this, a polar-cap uses the same scheme but centred on the SCP
and limited in extent to minimise overlap with the dec-band section.


"""
label_help = """
Name of region being tiled. This is used to name all auxilliary output files:
    kvis annotations file <LABEL>.ann
    plot file <LABEL>.png;
    Shell script for running footprint-plan.py on all tiles <LABEL>_footprint.sh;
    Observing parset <LABEL>.parset (can be overridden with the -o option).\n
The label is also used in naming fields in the parset.

"""
interleave_help = """
If interleaving is selected (the default), each primary tile will be accompanied by
one or two additional tiles that place beam centres in the minima of the primary tile.
These interleaved tiles are also interleaved in the observing parset. So for a square
footprint, even numbered sources will be the primary 'A' position and odd numbered
the 'B'. For hexagonal patterns there are two additional tiles for each primary:
'B' and 'C'.

 """

# todo: factor this into a log config_file in ~/.config/aces/aces.pylog_cfg

# todo: Work out roll-axis wrap issues
# todo: check: cycle through sources for repeat?
# todo_done: check northern limit - this should be a filter on the selected tiles;
#       otherwise the whole sky should/could be tiled?
# todo: reconcile tile_plot with jupyter version; deprecate the latter?
# todo: fix all help
# todo_done: provide ds9 overlays
# todo: fix PA of tile centred on pole.
# todo: write output as parset; add variables to suit; observing quantities need to be recognised.

script_name = 'tile_sky'

FORMAT_FILE = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
FORMAT_CONSOLE = '%(name)s - %(levelname)s - %(message)s'
formatter_console = logging.Formatter(FORMAT_CONSOLE)
formatter_file = logging.Formatter(FORMAT_FILE)
timestr = time.strftime("%Y%m%d-%H%M%S")
# logging.basicConfig(filename='survey-plan-{}.log'.format(timestr), level=logging.DEBUG,
#                     filemode='w', format=FORMAT_FILE)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(formatter_console)
# logging.getLogger('').addHandler(console)


# logger.addHandler(console)


def arg_init():
    aces_cfg = ACESConfig()
    fp_factory = aces_cfg.footprint_factory
    fp_names = [f for f in fp_factory.get_footprint_names() if f.startswith('ak:')]
    fp_names = [f.split(':')[1] for f in fp_names]
    coords = tile.Tile.n_pole.keys()
    north_lim = 40.0
    # Build some help information:

    epilog = "Label" + label_help + \
             "Interleaving" + interleave_help + \
             "Footprint names\n  " + ', '.join(fp_names) + \
             "\n\nSee -x for more explanation\n"

    parser = ap.ArgumentParser(prog=script_name, formatter_class=ap.RawDescriptionHelpFormatter,
                               description=description,
                               epilog=epilog)
    parser.add_argument('label', help="Survey label or SB integer identifier")
    parser.add_argument('-x', '--explain', action='store_true', help="Give an expanded explanation")
    parser.add_argument('-n', dest='name', metavar='', choices=fp_names, default="square_6x6",
                        help="Name of footprint (see below for choices) [%(default)s]")
    parser.add_argument('-p', '--pitch', type=float, default=0.9, help="Beam spacing in degrees [%(default).2f]")
    parser.add_argument('-c', '--coord', default='J2000', choices=coords, help="Coordinate system")
    parser.add_argument('-m', '--latrange', nargs=2, metavar=('lat1', 'lat2'), type=float, default=[-72., 72.],
                        help="Latitude SC range (degrees)")
    parser.add_argument('-r', '--reference', metavar='RA,Dec', help="Position of tiled origin",
                        default=[0.0, 0.0], action=Celpos)
    parser.add_argument('-M', '--mask', default="", help="File defining polygons to mask a tiling")
    parser.add_argument('-s', '--select', default="", help="File defining polygons to be tiled")
    parser.add_argument('-b', '--beamform_pa', default=45.0, help="Beam-forming PA [%(default).1f]")
    parser.add_argument('-S', '--force_symmetry', action='store_true', help="Force north-south symmetry (polygons)")
    parser.add_argument('-X', '--no_interleave', action='store_true', help="Do NOT interleave")
    parser.add_argument('-I', '--tile_interleave_quad', type=int, default=-1, choices=[-1, 0, 1, 2, 3],
                        help='Select quadrant for tile interleave (default is none)')
    parser.add_argument('-v', '--verbose', action='store_true', help="Print extra information to the screen")

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


def parset_init(fp, beamform_pa):
    ps = ParameterSet()
    name = fp.name
    pitch = np.degrees(fp.pitch_scale)

    preamble = ['common.target.src%d.footprint.name = {}'.format(name),
                'common.target.src%d.footprint.pitch = {:.3f}'.format(pitch),
                'common.target.src%d.footprint.rotation = {:.3f}'.format(beamform_pa)]
    for pr in preamble:
        k, v = pr.split('=')
        ps.set_value(k.strip(), v.strip())
    return ps


def main():
    # save input command
    input_command = ' '.join(sys.argv)
    # parse command line options
    parser, aces_cfg = arg_init()
    args = parser.parse_args()
    verbose = args.verbose
    label = args.label
    print('label = ', args.label)
    if args.verbose:
        print("ARGS = ", args)
    if args.explain:
        print(explanation)
        return

    logging.basicConfig(filename='tile_sky-{}.log'.format(timestr), level=logging.INFO,
                    filemode='w', format=FORMAT_FILE)
    logging.getLogger('').addHandler(console)
    # Establish output file names, and open files

    parset_name = "{}.parset".format(label)

    footprint_cmd_name_ds9 = '{}_footprint_ds9.sh'.format(label)
    fpcmds_ds9 = open(footprint_cmd_name_ds9, 'w')
    footprint_cmd_name_ann = '{}_footprint_kvis.sh'.format(label)
    fpcmds_ann = open(footprint_cmd_name_ann, 'w')

    kvis_ann_name = '{}.ann'.format(label)
    ann = open(kvis_ann_name, 'w')
    s1 = 'COLOR GREEN'
    ann.write(s1 + '\n')

    ds9_name = '{}.reg'.format(label)
    ds9 = open(ds9_name, 'w')

    # Get footprint related details
    fp_factory = aces_cfg.footprint_factory
    name = prefix(args.name, 'ak:')
    beam_pitch = np.radians(args.pitch)
    fp = fp_factory.make_footprint(name, beam_pitch)

    coord = args.coord
    do_interleave = not args.no_interleave
    bf_pa = args.beamform_pa

    do_tile_interleave = args.tile_interleave_quad >= 0
    interleave_quad = args.tile_interleave_quad

    # Generate coordinate transformation based on user's preference position: place it at the origin.
    refpos = args.reference
    ra, dec = refpos
    origin = Skypos(ra, dec)
    print('Reference position lon, lat ', origin.get_ras(), origin.get_decs())

    polygons = []
    poly_file = ""
    if args.select:
        poly_file = args.select
        if os.path.exists(poly_file):
            polygons = tile.get_polygons(poly_file)
    elif args.mask:
        poly_file = args.mask
        if os.path.exists(poly_file):
            polygons = tile.get_polygons(poly_file)

    tile.Tile.initialise(origin, label, fp, bf_pa, coord=coord)

    ps = parset_init(fp, bf_pa)

    tile_offsets = np.array(fp.get_tile_offsets())
    tile_pitches = [tile_offsets[0][0], tile_offsets[1][1]]
    tile_area = tile.rectangle_area(tile_pitches)
    latrange = np.radians(np.array(args.latrange))
    force_sym = args.force_symmetry

    if args.verbose:
        print("Tile pitches {}".format(tile_pitches))
        print("Beam pitch {:.3f}".format(beam_pitch))
        print("Lat range  {}".format(latrange))

    all_sky, tiles_masked = True, False
    if args.select and len(polygons) > 0:
        tiling = {}
        for i, poly in enumerate(polygons):
            ptiling = tile.tile_polygon(tile_pitches, poly, force_symmetry=force_sym)
            num_untrimmed = len(ptiling['tiles'])
            tmask = tile.mask_tiles(ptiling['tiles'], tile_pitches, [poly])
            tiles = ptiling['tiles'][~tmask]
            num_trimmed = len(tiles)
            ptiling['tiles'] = tiles
            ptiling['area_tiles'] *= (num_trimmed / num_untrimmed)
            if i == 0:
                for k, v in ptiling.items():
                    tiling[k] = v
            else:
                tiling['tiles'] = np.concatenate([tiling['tiles'], ptiling['tiles']])
                tiling['area_survey'] += ptiling['area_survey']
                tiling['area_tiles'] += ptiling['area_tiles']
                tiling['lat_limits'] = [min(tiling['lat_limits'][0], ptiling['lat_limits'][0]),
                                        max(tiling['lat_limits'][1], ptiling['lat_limits'][1])]
        all_sky = False
    else:
        tiling = tile.tile_pol_to_pol(tile_pitches, beam_pitch, latrange, do_north=True)
        if args.mask and len(polygons) > 0:
            tiles_masked = True
            tmask = tile.mask_tiles(tiling['tiles'], tile_pitches, polygons)
            tiles = tiling['tiles'][~tmask]
            tiling['tiles'] = tiles
            tiling['area_survey'] = np.array([tile.polygon_area(poly) for poly in polygons]).sum() * ster_to_sqdeg
            tiling['area_tiles'] = len(tiles) * tile_area * ster_to_sqdeg

    # tile_positions = tiling['tiles']
    tiles = tiling['tiles']

    total_area = tiling['area_survey']
    tiles_area = tiling['area_tiles']
    surplus = tiles_area - total_area
    polar_boundary = tiling['lat_limits']
    if all_sky:
        print("All sky tiling in {} coordinates".format(coord))
        if tiles_masked:
            print("Masked with {}".format(poly_file))
    else:
        print("Polygon tiled in {} coordinates using {}".format(coord, poly_file))
    if do_interleave:
        print("Doing interleaving")
    else:
        print("NO interleaving")
    print("Sky tiling          :  {:d} tiles".format(len(tiles)))
    print("Total survey area   : {:.1f} sq deg".format(total_area))
    print("Tile area           : {:.1f} sq deg".format(tile_area * ster_to_sqdeg))
    print("Aggregate tile area : {:.1f} sq deg".format(tiles_area))
    print("Surplus             : {:.1f} sq deg  ({:.1f}%)".format(surplus, 100. * surplus / total_area))
    # print("Polar boundary    : {:.2f}".format(polar_boundary[0] * 180.0 / np.pi))
    print()

    ps.set_value('common.tiling.source', script_name)
    ps.set_value('common.tiling.command', input_command)
    # ps.set_value('common.tiling.polar_boundaries', '[{:.3f}, {:.3f}]'.format(np.degrees(polar_boundary[0]),
    #                                                                          np.degrees(polar_boundary[1])))
    ps.set_value('common.tiling.coord', '{}'.format(coord))
    ps.set_value('common.tiling.reference_position', '[{}, {}]'.format(origin.get_ras(), origin.get_decs()))
    ps.set_value('common.tiling.tile_interleaving_quadrant', '{:d}'.format(interleave_quad))
    n_inaccessible = 0
    src_num = 0
    for tp in tiles:
        if do_tile_interleave:
            ti = tp.get_interleaved_tile(interleave_quad)
        else:
            ti = tp
        # Need to check accessibility again - interleaved tile may fall to far north.
        if ti.check_accessible():
            pe = ti.get_parset_entry(with_interleave=do_interleave)
            iks = pe.keys()
            for ik in iks:
                for pei in pe[ik]:
                    kv, c = extract(pei)
                    ps.set_value(kv[0] % src_num, kv[1])
                src_num += 1
        else:
            if verbose:
                print("Inaccessible :  at {}".format(ti.skypos))
            n_inaccessible += 1

    # print("\n{:d} tiles are not accessible: north of Declination {:.2f}".format(n_inaccessible,
    #                                                                             np.degrees(tile.Tile.northern_limit)))
    for ti in tiles:
        ann.write(ti.get_overlay(kind='kvis'))
        ann.write(ti.get_overlay_label(ti.name, kind='kvis'))
        ds9.write(ti.get_overlay(kind='ds9'))
        fpcmds_ds9.write(ti.get_footprint_cmd(kind='ds9'))
        fpcmds_ann.write(ti.get_footprint_cmd(kind='kvis'))

    ps.to_file(parset_name)


if __name__ == "__main__":
    sys.exit(main())
