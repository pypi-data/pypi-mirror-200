#!/usr/bin/env python
from __future__ import print_function
import time
import argparse as ap
import sys
import numpy as np
from aces.obsplan.config import ACESConfig
from askap.parset import ParameterSet
from aces.obsplan import logger
from askap import logging
from askap.coordinates import parse_direction
from askap.footprint import Skypos
from askap.footprint import tilesky

explanation = tilesky.explanation
"""
This survey-plan.py is an interactive wrapper for tilesky.py
"""

# todo: factor this into a log config_file in ~/.config/aces/aces.pylog_cfg
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
    fp_names = fp_factory.get_footprint_names()
    parser = ap.ArgumentParser(prog='survey-plan', formatter_class=ap.RawDescriptionHelpFormatter,
                               description='',
                               epilog='See -x for more explanation')
    parser.add_argument('inFile', nargs="?", help="Survey descriptor held in inFile")
    parser.add_argument('-P', '--project', default="AS033", help="OPAL project code")
    parser.add_argument('-l', '--label', default="somewhere", help="Name of region being tiled")
    parser.add_argument('-n', dest='name', choices=fp_names, default="ak:square_6x6", help="Name of footprint.")
    parser.add_argument('-p', '--pitch', type=float, default=0.9, help="Beam spacing in degrees")
    parser.add_argument('-c', '--centre', metavar="'RA,Dec'", action=Celpos, default="00:00:00.0, -00:00:00.0",
                        help="Survey centre position")
    parser.add_argument('-a', '--angle', type=float, default=0.0, help="Inclination of area (degrees)")
    parser.add_argument('-r', '--bfDiff', type=float, default=-45.0,
                        help="BeamForming difference : roll - FP (degrees)")
    parser.add_argument('-b', '--longshift', type=float, default=0.0, help="Shift area in longitude (degrees)")
    parser.add_argument('-s', '--size', metavar="'na,nb'", default=[1, 1], action=WidHt,
                        help="Survey sky area wid,ht in tiles")
    parser.add_argument('-o', '--size_obs', metavar="'ma,mb'", default=[1, 1], action=WidHt,
                        help="Observation area wid,ht in tiles")
    parser.add_argument('-f', '--frequency', type=float, default=1290.0, help="Centre frequency (MHz)")
    parser.add_argument('-t', '--obs_duration', type=float, default=43200.0, help="Observation duration (sec) [43200]")
    parser.add_argument('-d', '--dwell_time', type=float, default=300.0, help="Dwell time per pointing (sec) [300]")
    parser.add_argument('-z', '--no_interleave', action='store_true', help="Do NOT interleave")
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-x', '--explain', action='store_true', help="Give an expanded explanation")
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
        a, b = [q for q in values.split(",") if len(q) > 0]
        rp = [int(a), int(b)]
        # noinspection PyUnresolvedReferences
        setattr(namespace, self.dest, rp)


def write_descriptor(args, centre, fname):
    f = open(fname, 'w')
    f.write("project_code = {}\n".format(args.project))
    f.write("survey.name = {}\n".format(args.label))
    f.write("survey.centre = {},{}\n".format(centre.get_ras(), centre.get_decs()))
    f.write("survey.width = {}\n".format(args.size[0]))
    f.write("survey.height = {}\n".format(args.size[1]))
    f.write("survey.obs_width = {}\n".format(args.size_obs[0]))
    f.write("survey.obs_height = {}\n".format(args.size_obs[1]))
    f.write("survey.position_angle = {}\n".format(args.angle))
    f.write("survey.beamforming_difference = {}\n".format(args.bfDiff))
    f.write("survey.long_shift = {}\n".format(args.longshift))
    f.write("survey.obs_duration = {}\n".format(args.obs_duration))
    f.write("survey.dwell_time = {}\n".format(args.dwell_time))
    f.write("survey.frequency = {}\n".format(args.frequency))
    f.write("survey.footprint_name = {}\n".format(args.name.split(':')[-1]))
    f.write("survey.beam_pitch = {}\n".format(args.pitch))
    if args.no_interleave:
        f.write("survey.interleave = False\n")
    else:
        f.write("survey.interleave = True\n")
    f.close()


def main():
    # parse command line options
    parser, aces_cfg = arg_init()
    args = parser.parse_args()

    # handle default centre position case (which will still be an unconverted string)
    # this is needed because default arguments are not parsed by the argparse.Action object
    if type(args.centre[0]) is str:
        a, b = parse_direction(args.centre)
        args.centre = np.radians(a), np.radians(b)

    fp_factory = aces_cfg.footprint_factory

    if args.explain:
        print(explanation)
        sys.exit(0)

    # If we get here, the survey centre position has been successfully parsed. We can now convert it back to a string
    # for the descriptor file, which should be human-readable.
    # noinspection PyTypeChecker
    centre = Skypos(args.centre[0], args.centre[1])
    if args.inFile:
        survey_parset = ParameterSet(args.inFile)
        fp_parset = fp_factory.footprint_masters['ak:{}'.format(survey_parset.survey.footprint_name)]
        tilesky.main(survey_parset, fp_parset, '.')
    else:
        write_descriptor(args, centre, "{}.descriptor".format(args.label))
        fp_parset = fp_factory.footprint_masters[args.name]
        tilesky.main(ParameterSet("{}.descriptor".format(args.label)), fp_parset, '.')


if __name__ == "__main__":
    sys.exit(main())
