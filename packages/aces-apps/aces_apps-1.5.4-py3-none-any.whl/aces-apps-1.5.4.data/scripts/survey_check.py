#!/usr/bin/env python
"""
This checks that the filename.csv file successfully indexes product files.

"""

import sys
from pathlib import Path
import argparse as ap
import glob
from aces.survey.survey_class import ASKAP_Survey_factory

explanation = __doc__


def arg_init():
    # code_path = os.path.dirname(os.path.abspath(survey.__file__))

    parser = ap.ArgumentParser(prog='survey_validation', formatter_class=ap.RawDescriptionHelpFormatter,
                               description=__doc__,
                               epilog='See -x for more explanation')
    # noinspection PyTypeChecker
    # parser.add_argument('fld_name', nargs=1, help='Survey field name; no default')
    parser.add_argument('-n', '--numbers', type=int, nargs='*', help="Row numbers to process")
    parser.add_argument('-b', '--bounds', type=int, nargs='*', help="Row number bounds")
    parser.add_argument('-S', '--sbid', type=int, nargs=1, help="Select by SBID")
    parser.add_argument('-C', '--calsbid', type=int, nargs=1, help="Select by CAL SBID")

    parser.add_argument('-e', '--epoch', type=int, default=0, help="Survey epoch")
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-x', '--explain', action='store_true', help="give an expanded explanation")
    return parser


def check_filenames_csv(survey, inx):
    fn = survey.survey_files.file_name
    s_files = survey.survey_files
    abs_names = s_files.lookup.keys()
    for abs_name in abs_names:
        file_name = fn(abs_name, inx)
        print("{:23s} {} {}".format(abs_name, file_name.exists(), file_name))
    print(" ")
    for abs_name in abs_names:
        file_name = str(fn(abs_name, inx))
        if '*' in file_name:
            files = glob.glob(file_name)
            print('For "{}", {:d} files found.'.format(abs_name, len(files)))
            for f in files:
                print("       {}".format(f))
            print(" ")


def main():
    args = arg_init().parse_args()

    if args.explain:
        print(explanation)
        sys.exit()
    verbose = args.verbose

    print("")
    print("Running survey_check.py with the following input:")
    print("ARGS = ", args)
    print("")

    epoch = args.epoch
    survey = ASKAP_Survey_factory(verbose=False, epoch=epoch)

    crit = [['STATE', '!=', '--NULL--']]

    if args.calsbid:
        crit.append(['CAL_SBID', '==', args.calsbid])
    elif args.sbid:
        crit.append(['SBID', '==', args.sbid])

    rows = survey.select_indices(crit)

    # Now, if specific numbers or ranges are given, use them instead.
    if args.numbers is not None:
        if len(args.numbers) > 0:
            rows = args.numbers
    if args.bounds is not None:
        if len(args.bounds) == 2:
            bounds = args.bounds
            rows = range(bounds[0], bounds[1])
    for row in rows:
        check_filenames_csv(survey, row)


if __name__ == "__main__":
    sys.exit(main())
