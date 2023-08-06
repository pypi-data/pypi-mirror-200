#!/usr/bin/env python

import argparse as ap
import sys
import time
import re

import numpy as np
from aces.obsplan import logger
from aces.obsplan.config import ACESConfig
from askap import logging
from askap.parset import ParameterSet, extract

explanation = """


Script obs-preamble
===============
This prepares the preamble section of an observation parset.

The script produces results in several files:
 - <label>.parset  - observing parset preamble.
    parset may need editing before submission as an ASKAP observation;



"""
description = """
This ...


"""
label_help = """
Name of parset: <label>_preamble.parset.

"""

# todo: factor this into a log config_file in ~/.config/aces/aces.pylog_cfg

# todo: fix all help
# todo_done: provide ds9 overlays
# todo: write output as parset; add variables to suit; observing quantities need to be recognised.

script_name = 'obs-preamble'

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


def arg_init():
    aces_cfg = ACESConfig()
    fp_factory = aces_cfg.footprint_factory
    fp_names = [f for f in fp_factory.get_footprint_names() if f.startswith('ak:')]
    fp_names = [f.split(':')[1] for f in fp_names]
    zooms = [1, 2, 4, 8, 16, 32]
    # Build some help information:

    epilog = "Label" + label_help + \
             "Footprint names\n  " + ', '.join(fp_names) + \
             "\n\nSee -x for more explanation\n"

    parser = ap.ArgumentParser(prog=script_name, formatter_class=ap.RawDescriptionHelpFormatter,
                               description=description,
                               epilog=epilog)
    # parser.add_argument('inFile', nargs="?", help="Survey descriptor held in inFile")
    parser.add_argument('-x', '--explain', action='store_true', help="XX-Give an expanded explanation")
    parser.add_argument('-v', '--verbose', action='store_true', help="Print extra information to the screen")
    parser.add_argument('-l', '--label', default="somewhere", help="Label for outputs (see below)")
    parser.add_argument('-n', dest='name', metavar='', choices=fp_names, default="square_6x6",
                        help="Name of footprint (see below for choices) [%(default)s]")
    parser.add_argument('-p', '--pitch', type=float, default=0.9, help="Beam spacing in degrees [%(default).2f]")
    parser.add_argument('-s', '--select', default="", help="File defining polygons to be tiled")
    parser.add_argument('-M', '--mask', default="", help="File defining polygons to mask a tiling")
    parser.add_argument('-P', '--project', default="AS033", help="OPAL project code")
    parser.add_argument('-b', '--beamform_pa', default=45.0, help="Beam-forming PA [%(default).1f]")
    parser.add_argument('-S', '--force_symmetry', action='store_true', help="Force north-south symmetry (polygons)")
    parser.add_argument('-X', '--no_interleave', action='store_true', help="Do NOT interleave")
    parser.add_argument('-I', '--tile_interleave_quad', type=int, default=-1, choices=[-1, 0, 1, 2, 3],
                        help='Select quadrant for tile interleave (default is none)')
    parser.add_argument('-t', '--obs_duration', type=float, default=43200.0,
                        help="Observation duration (sec) [%(default).0f]")
    parser.add_argument('-d', '--dwell_time', type=float, default=300.0,
                        help="Dwell time per pointing (sec) [%(default).0f]")
    parser.add_argument('-f', '--frequency', type=float, default=1296.0, help="Centre frequency (MHz) [%(default).2f]")
    parser.add_argument('-z', '--zoom_mode', type=int, default=1, choices=zooms, help="Zoom mode [%(default)d]")

    return parser, aces_cfg


class WidHt(ap.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        logger.debug('ACTION : %r %r %r' % (namespace, values, option_string))
        # print 'WidHt : ', values
        a, b = [q for q in values.split(",") if len(q) > 0]
        rp = [int(a), int(b)]
        # noinspection PyUnresolvedReferences
        setattr(namespace, self.dest, rp)


class TwoFloats(ap.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        logger.debug('ACTION : %r %r %r' % (namespace, values, option_string))
        a, b = [q for q in values.split(",") if len(q) > 0]
        rp = [float(a), float(b)]
        # noinspection PyUnresolvedReferences
        setattr(namespace, self.dest, rp)


def sky_to_centre_frequency(f, z, forward=True):
    """
    Given "sky_frequency", the frequency parameter required by the control software, return the
    resultant centre frequency.
    # Assuming 288 MHz continuum bandwidth (6 48_MHz blocks), and the sky_frequency is 2.5 blocks from
    # the lower end,
    # return the band centre frequency, adjusted according to the selected zoom mode.
    # f - sky_frequency in MHz
    # z -zoom  out of (1, 2, 4, 8, 16, 32)
    :param f:  (float)     sky_frequency in MHz (or centre frequency)
    :param z: (int) zoom  out of (1, 2, 4, 8, 16, 32)
    :param forward: (bool) Default True. If False, convert from centre to sky_frequency
    :return  (float) Centre frequency (or sky_frequency)
    """
    if forward:
        f1 = f - 2.5 * 48.0 / z
        ret = f1 + 3.0 * 48. / z
    else:
        f1 = f - 3.0 * 48. / z
        ret = f1 + 2.5 * 48. / z
    return ret


def prefix(word, pfx):
    if word.startswith(pfx):
        return word
    else:
        return pfx + word


def parset_init(beam_weights, duration, fp, sky_frequency, corrmode, beamform_pa):
    ps = ParameterSet()
    name = fp.name
    pitch = np.degrees(fp.pitch_scale)

    z = 1
    iz = re.findall('[0-9]+', corrmode)
    if len(iz) == 1:
        z = int(iz[0])
    if (sky_frequency - 700.0) * z >= 120.0:
        if (1200.5 - sky_frequency) * z >= 168.0:
            band_filter = 'FILTER_1200'
        elif (1440.5 - sky_frequency) * z >= 168.0:
            band_filter = 'FILTER_1450'
        elif (1800.5 - sky_frequency) * z >= 168.0:
            band_filter = 'FILTER_1800'
        else:
            print("Incompatible values of sky_frequency ({:f}) and corrmode ({})".format(sky_frequency, corrmode))
            band_filter = 'illegal'
    else:
        band_filter = 'illegal'

    if band_filter == "illegal":
        print("Incompatible values of sky_frequency ({:f}) and corrmode ({})".format(sky_frequency, corrmode))

    bf_res = 1
    preamble = ['common.antennas =',
                'common.enable_cp = true',
                'common.enable_datacapture = true',
                'common.target.src%d.beam_weights = {}'.format(beam_weights),
                'common.target.src%d.corrmode = {}'.format(corrmode),
                'common.target.src%d.datacapture = cal',
                'common.target.src%d.bf_resolution = {:d}'.format(bf_res),
                'common.target.src%d.duration = {:f}'.format(duration),
                'common.target.src%d.footprint.name = {}'.format(name),
                'common.target.src%d.footprint.pitch = {:.3f}'.format(pitch),
                'common.target.src%d.footprint.rotation = {:.3f}'.format(beamform_pa),
                'common.target.src%d.filter_band = {}'.format(band_filter),
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

    parset_name = "{}_preamble.parset".format(label)

    duration = args.dwell_time
    centre_frequency = args.frequency
    zoom_mode = args.zoom_mode
    if zoom_mode == 1:
        corrmode = "standard"
    else:
        corrmode = "zoom{:d}x".format(zoom_mode)
    sky_frequency = sky_to_centre_frequency(centre_frequency, zoom_mode, forward=False)

    # Get footprint related details
    fp_factory = aces_cfg.footprint_factory
    name = prefix(args.name, 'ak:')
    beam_pitch = np.radians(args.pitch)
    fp = fp_factory.make_footprint(name, beam_pitch)

    bf_pa = args.beamform_pa
    beam_weights = ""

    ps = parset_init(beam_weights, duration, fp, sky_frequency, corrmode, bf_pa)

    centre_frequency = sky_to_centre_frequency(sky_frequency, zoom_mode)
    band_edges = [centre_frequency - 144.0 / zoom_mode, centre_frequency + 144. / zoom_mode]
    print("Centre frequency    : {:.2f} MHz".format(centre_frequency))
    print("Frequency band      : {:.2f} - {:.2f} MHz".format(band_edges[0], band_edges[1]))
    print("Sky frequency       : {:.2f} MHz (input to TOS)".format(sky_frequency))

    ps.set_value('common.tiling.source', script_name)
    ps.set_value('common.tiling.command', input_command)

    ps.to_file(parset_name)


if __name__ == "__main__":
    sys.exit(main())
