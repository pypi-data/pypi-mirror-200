#!/usr/bin/env python
from __future__ import print_function
import time
import argparse as ap
import sys
import numpy as np

import aces.obsplan.tile as tile

from askap.footprint import Skypos

from aces.obsplan.config import ACESConfig
from askap.parset import ParameterSet, extract
from aces.obsplan import logger
from askap import logging
from askap.coordinates import parse_direction


# explanation = tilesky.explanation
#This survey-plan.py is an interactive wrapper for tilesky.py
#--------------------------------------------------------------

explanation = """

Script tile_sky
===============
This tiles the sky in the fashion described by Aaron Robotham (UWA), that is tiles arranged along small circles
over a declination band and a polar-cap using the same scheme but centred on the SCP and limited in extent to minimse
overlap with the dec-band section.

The script will transform any tiling into other coordinates, so that the requested survey parameters can 
be expressed as equatorial  ("J2000"), Galactic  ("GALAC") or Magellanic ("MAGEL")
(see http://adsabs.harvard.edu/abs/2008ApJ...679..432N).

The script produces results in several files:
 - <label>.parset  - observing parset; gives the required entries for each tile and its interleaves; at present this
    parset may need editing before submission as an ASKAP observation;
 - <label>.ann - kvis annotations file that shows the tile locations and names on a kvis-displayed image
 - <label>_footprint.sh - shell script that can be run to produce plan-footprint.py output for each tile;
 
The tiling is controlled with these inputs:
1. -m lat1,lat2  the latitude margins of the small-circle section - (default values [-72,72])
2. -c {J2000,GALAC,MAGEL} specifies the coordinate frame - (default is J2000)
3. -r Origin of the tiling in the chosen coordinates (lon,lat) - (default is [0.0,0.0]
4. -p the beam spacing (pitch) - (default is 0.9 deg)
5. -n the name of the footprint - (default is square_6x6)


For a given tiling, a subset of the tiles can be chosen using the "horizontal" and "vertical" limit parameters:
1. -H th1, th2 give the longitude limits
2. -V ph1, ph2 give the latitude limits.


"""
description = """
Description goes here

"""
label_help = """
Name of region being tiled. This is used to name all auxilliary output files:
    kvis annotations file <LABEL>.ann
    plot file <LABEL>.png;
    Shell script for running footprint-plan.py on all tiles <LABEL>_footprint.sh;
    Observing parset <LABEL>.parset (can be overridden with the -o option).\n
The label is also used in naming fields in the parset.
"""

# todo: factor this into a log config_file in ~/.config/aces/aces.pylog_cfg

# todo: Work out roll-axis wrap issues
# todo: check: cycle through sources for repeat?
# todo_done: check northern limit - this should be a filter on the selected tiles;
#       otherwise the whole sky should/could be tiled?
# todo: reconcile tile_plot with jupyter version; deprecate the latter?
# todo_done: change name tilesky
# todo: fix all help
# todo: provide ds9 overlays
# todo: fix PA of tile centred on pole.
# todo: write output as parset; add variables to suit; observing quantities need to be recognised.
# todo: remove the selection function from this; write out the whole tiling into a parset.
# todo: Add ability to define new coordinate with user to provide the three angles
# todo_done: plotting: adjust alpha in patches
# todo_done: plotting: allow plotting of both selected and all_tiles, with different alpha?
# todo_ok_for_now: add molleweide projection
# todo_fixed: check Vanessa's comments on tile numbering.
# todo_done: remove reference to unused parameters "overlaps"

script_name = 'tile_sky'

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
    fp_factory = aces_cfg.footprint_factory
    fp_names = [f for f in fp_factory.get_footprint_names() if f.startswith('ak:')]
    fp_names = [f.split(':')[1] for f in fp_names]
    coords = tile.Tile.n_pole.keys()
    north_lim = 40.0
    zooms = [1, 2, 4, 8, 16, 32]
    # Build some help information:

    epilog = "Label\n" + label_help + \
             """
             Footprint names
    """ + ','.join(fp_names) + '\nSee -x for more explanation'

    parser = ap.ArgumentParser(prog=script_name, formatter_class=ap.RawDescriptionHelpFormatter,
                               description=description,
                               epilog=epilog)
    parser.add_argument('inFile', nargs="?", help="Survey descriptor held in inFile")
    parser.add_argument('-x', '--explain', action='store_true', help="Give an expanded explanation")
    parser.add_argument('-v', '--verbose', action='store_true', help="Print extra information to the screen")
    parser.add_argument('-P', '--project', default="AS033", help="OPAL project code")
    parser.add_argument('-l', '--label', default="somewhere", help="Label for outputs (see below)")
    parser.add_argument('-n', dest='name', metavar='', choices=fp_names, default="square_6x6",
                        help="Name of footprint (see below for choices) [%(default)s]")
    parser.add_argument('-p', '--pitch', type=float, default=0.9, help="Beam spacing in degrees [%(default).2f]")
    parser.add_argument('-b', '--beamform_pa', default=45.0, help="Beam-forming PA [%(default).1f]")
    parser.add_argument('-X', '--no_interleave', action='store_true', help="Do NOT interleave")
    parser.add_argument('-c', '--coord', default='J2000', choices=coords, help="Coordinate system")
    parser.add_argument('-r', '--reference', metavar="'RA,Dec'", help="Position of tiled origin",
                        default=[0.0, 0.0], action=Celpos)
    parser.add_argument('-m', '--latrange', nargs=2, metavar="'lat1,lat2'", type=float, default=[-72., 72.],
                        help="Latitude SC range (degrees)")
    parser.add_argument('-H', '--horiz', nargs=2, type=float, default=[0., 360.], help="Horizontal limits (degrees)")
    parser.add_argument('-V', '--vertical', nargs=2, type=float, default=[-90., north_lim],
                        help="Vertical limits (degrees)")
    parser.add_argument('-t', '--obs_duration', type=float, default=43200.0,
                        help="Observation duration (sec) [%(default).0f]")
    parser.add_argument('-d', '--dwell_time', type=float, default=300.0,
                        help="Dwell time per pointing (sec) [%(default).0f]")
    parser.add_argument('-f', '--frequency', type=float, default=1290.0, help="Centre frequency (MHz) [%(default).2f]")
    parser.add_argument('-z', '--zoom_mode', type=int, default=1, choices=zooms, help="Zoom mode [%(default)d]")

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
    print ("pair : ", arg)
    return [float(a) for a in arg.split(',')]


class TwoFloats(ap.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        logger.debug('ACTION : %r %r %r' % (namespace, values, option_string))
        a, b = [q for q in values.split(",") if len(q) > 0]
        rp = [float(a), float(b)]
        # noinspection PyUnresolvedReferences
        setattr(namespace, self.dest, rp)


# class Overlay(object):
#     overlay_types = ['kvis', 'vot']
#     file_ext = {'kvis': 'ann', 'vot': 'vot'}
#     def __init__(self, overlay_type='kvis', name):
#         self.o_type = overlay_type
#         self.name = name
#         self.output_name = name + '.' + Overlay.file_ext[self.o_type]
#         self.output = open(self.output_name, 'w')
#
#     def

def sky_to_centre_frequency(f, z):
    # Assuming 288 MHz continuum bandwidth (6 48_MHz blocks), and the sky_frequency is 2.5 blocks from
    # the lower end,
    # return the band centre frequency, adjusted according to the selected zoom mode.
    # f - sky_frequency in MHz
    # z -zoom  out of (1, 2, 4, 8, 16, 32)
    f1 = f - 2.5 * 48.0/z
    return f1 + 3.0 * 48./z


def prefix(word, pfx):
    if word.startswith(pfx):
        return word
    else:
        return pfx + word


def parset_init(beam_weights, duration, fp, sky_frequency, corrmode, beamform_pa):
    ps = ParameterSet()
    name = fp.name
    pitch = np.degrees(fp.pitch_scale)
    preamble = ['common.antennas =',
                'common.enable_cp = true',
                'common.enable_datacapture = true',
                'common.target.src%d.beam_weights = {}'.format(beam_weights),
                'common.target.src%d.corrmode = {}'.format(corrmode),
                'common.target.src%d.datacapture = cal',
                'common.target.src%d.duration = {:f}'.format(duration),
                'common.target.src%d.footprint.name = {}'.format(name),
                'common.target.src%d.footprint.pitch = {:.3f}'.format(pitch),
                'common.target.src%d.footprint.rotation = {:.3f}'.format(beamform_pa),
                'common.target.src%d.sky_frequency = {:f}'.format(sky_frequency)]
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
    if args.verbose:
        print("ARGS = ", args)
    if args.explain:
        print(explanation)
        return

    # Establish output file names, and open files

    label = args.label

    parset_name = "{}.parset".format(label)

    footprint_cmd_name = '{}_footprint.sh'.format(label)
    fpcmds = open(footprint_cmd_name, 'w')

    kvis_ann_name = '{}.ann'.format(label)
    ann = open(kvis_ann_name, 'w')
    s1 = 'COLOR GREEN'
    ann.write(s1 + '\n')

    duration = args.dwell_time
    sky_frequency = args.frequency
    zoom_mode = args.zoom_mode
    if zoom_mode == 1:
        corrmode = "standard"
    else:
        corrmode = "zoom{:d}x".format(zoom_mode)

    # Get footprint related details
    fp_factory = aces_cfg.footprint_factory
    name = prefix(args.name, 'ak:')
    beam_pitch = np.radians(args.pitch)
    fp = fp_factory.make_footprint(name, beam_pitch)

    coord = args.coord
    do_interleave = not args.no_interleave
    bf_pa = args.beamform_pa
    beam_weights = ""

    # Generate coordinate transformation based on user's preference position: place it at the origin.
    refpos = args.reference
    ra, dec = refpos
    origin = Skypos(ra, dec)
    print ('Reference position lon, lat ', origin.get_ras(), origin.get_decs())
    tile.Tile.initialise(origin, label, fp, bf_pa, coord=coord)

    ps = parset_init(beam_weights, duration, fp, sky_frequency, corrmode, bf_pa)

    tile_offsets = np.array(fp.get_tile_offsets())
    tile_pitches = [tile_offsets[0][0], tile_offsets[1][1]]
    latrange = np.radians(np.array(args.latrange))
    hr = np.radians(np.array(args.horiz))
    vr = np.radians(np.array(args.vertical))

    tiling = tile.tile_pol_to_pol(tile_pitches, beam_pitch, latrange, do_north=True)
    tile_positions = tiling['tiles']
    tile_idents = tiling['idents']
    total_area = tiling['area_total']
    total_double = tiling['double_total']
    polar_boundary = tiling['lat_limits']
    print("Sky tiling :  {:d} tiles".format(len(tile_positions)))
    print("Total area : {:.1f} sq deg".format(total_area))
    print("Doubled    : {:.1f} sq deg  ({:.1f}%)".format(total_double, 100. * total_double / total_area))
    print("Polar boundary : {:.2f}".format(polar_boundary[0]*180.0/np.pi))
    if do_interleave:
        print("Doing interleaving")
    else:
        print("NOT interleaving")
    centre_frequency = sky_to_centre_frequency(sky_frequency, zoom_mode)
    band_edges = [centre_frequency - 144.0/zoom_mode, centre_frequency + 144./zoom_mode]
    print("Centre frequency : {:.2f} MHz".format(centre_frequency))
    print("Frequency band   : {:.2f} - {:.2f} MHz".format(band_edges[0], band_edges[1]))

    # Plan to record the following in a parset rather than a pickle file.
    # Variables that have standard names:
    # package['source'] goes to:
    # package['tile_def'] goes to:
    #                   'common.tiling.polar_boundaries = [{:.3f}, {:.3f}]'.format(polar_boundary[0], polar_boundary[1])
    #                   (tile_pitches can and should be determined from footprint spec.)
    # package['coord'] goes to:
    #                   'common.tiling.coord = {}'.format(coord)

    # package['refpos'] goes to:
    #                   'common.tiling.reference_position = [{}, {}].format(origin.get_ras(), origin.get_decs())
    # package['footprint'] goes to:
    #                 'common.target.src%d.footprint.name = {}'.format(name),
    #                 'common.target.src%d.footprint.pitch = {:.3f}'.format(pitch),
    #                 'common.target.src%d.footprint.rotation = {:.3f}'.format(beamform_pa),
    # package['tiling'] goes to:
    #   for tp, id in zip(tile_positions, tile_idents):
    #       ti = tile.Tile(id, tp[0], tp[1], tp[2])
    #       pe = ti.get_parset_entry(with_interleave=do_interleave)
    # iks = pe.keys()
    # for ik in iks:
    #     src_num = id
    #     src_list.append("src{:d}".format(src_num))
    #     for pei in pe[ik]:
    #         kv, c = extract(pei)
    #         # print src_num, ' ---  ', "kv[0] % src_num, kv[1]
    #         ps.set_value(kv[0] % src_num, kv[1])

    #       common.target.srcN.field_direction = [09:50:57.841, -70:53:48.51, J2000]
    #       common.target.srcN.field_name = junk_0945-70B
    #       common.target.srcN.pol_axis = [pa_fixed, -189.803]
    #   ** Here package['tiling'] holds
    # package['selected_idents']goes to:
    #       common.targets
    ps.set_value('common.tiling.source', script_name)
    ps.set_value('common.tiling.command', input_command)
    ps.set_value('common.tiling.polar_boundaries', '[{:.3f}, {:.3f}]'.format(np.degrees(polar_boundary[0]),
                                                                             np.degrees(polar_boundary[1])))
    ps.set_value('common.tiling.coord', '{}'.format(coord))
    ps.set_value('common.tiling.reference_position', '[{}, {}]'.format(origin.get_ras(), origin.get_decs()))
    for tp, ident in zip(tile_positions, tile_idents):
        ti = tile.Tile(ident, tp[0], tp[1], tp[2])

        pe = ti.get_parset_entry(with_interleave=do_interleave)
        iks = pe.keys()
        for ik in iks:
            src_num = ident
            # src_list.append("src{:d}".format(src_num))
            for pei in pe[ik]:
                kv, c = extract(pei)
                # print (src_num, ' ---  ', kv[0] % src_num, kv[1])
                ps.set_value(kv[0] % src_num, kv[1])

    if hr[0] < 0.0:
        hr[0] += 2.0 * np.pi
    if hr[1] < 0.0:
        hr[1] += 2.0 * np.pi

    # package['selection'] = [hr, vr]
    n_tiles = 0
    n_inaccessible = 0
    for tile_ident, tp in enumerate(tile_positions):
        h, v, p = tp
        h = (h + 2.0 * np.pi) % (2.0 * np.pi)
        # print 'for tile_ident ... ', tp, hr, vr
        if hr[0] < hr[1]:
            h_range = hr[0] <= h <= hr[1]
        else:
            h_range = hr[0] <= h or h < hr[1]
        if h_range and vr[0] <= tp[1] <= vr[1]:
            ti = tile.Tile(tile_ident, tp[0], tp[1], tp[2])
            if not ti.check_accessible():
                n_inaccessible += 1
            else:
                # if tile_ident in select:
                n_tiles += 1
                # package['selected_idents'].append(tile_ident)
                ann.write(ti.get_ann_outline())
                ann.write(ti.get_ann_label())
                fpcmds.write(ti.get_footprint_cmd())
                # print('# ', ti.name)
    #             pe = ti.get_parset_entry(with_interleave=do_interleave)
    #             iks = pe.keys()
    #             for ik in iks:
    #                 src_num += 1
    #                 src_list.append("src{:d}".format(src_num))
    #                 for pei in pe[ik]:
    #                     kv, c = extract(pei)
    #                     # print src_num, ' ---  ', "kv[0] % src_num, kv[1]
    #                     ps.set_value(kv[0] % src_num, kv[1])
    #
    # ps.set_value("common.targets", '[' + ','.join(src_list) + ']')
    print("\n{:d} tiles are not accessible: north of Declination {:.2f}".format(n_inaccessible,
                                                                                np.degrees(tile.Tile.northern_limit)))

    ps.to_file(parset_name)


if __name__ == "__main__":
    sys.exit(main())
