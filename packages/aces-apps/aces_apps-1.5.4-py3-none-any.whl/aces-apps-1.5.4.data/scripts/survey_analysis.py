#!/usr/bin/env python
"""
This works on image files in FITS format. It is given the name of a FITS file,
or a name with wild-cards (to be interpreted by glob.glob), or the name of
a file containing a list of fits file names. The list file name should be prefixed with @.

Outputs are written to the working directory; this is either the current directory, or the directory
given with the -d option.

Input file names must successfully address the input files from the working directory.

Two kinds of output are produced:
1. <workdir>/racs_stats_<run_date>.csv is created and statistics and PSF details are written to it.
2. <workdir>/<image_file_name>.rms.fits is created; this is the rms image from which statistics are determined.
-------------------------------------------------------------

"""
from __future__ import print_function
import sys
import os
import time
import argparse as ap
from pathlib import Path
import numpy as np
import warnings

from astropy.io import ascii
from astropy.io import fits
from astropy.io.votable import parse_single_table
from astropy.wcs import WCS
from astropy.table import Table, unique
from astropy.utils.exceptions import AstropyWarning

from aces.racs.racs_survey import ASKAP_Survey_factory
import aces.racs.survey_utils as sut
import aces.racs.racs_survey as aks
import aces.misc.image_stats as ims

NOFORMAT = '{noformat}\n'

b_err_colnames = ['RA_DEG', 'DEC_DEG', 'BR_MIN', 'BR_MAX']
b_err_coltypes = ['f4', 'f4', 'f4', 'f4']
b_err_types = {k: v for k, v in zip(b_err_colnames, b_err_coltypes)}

stats_colnames = ['FLD_NAME', 'SBID', 'MED_RMS_uJy', 'MODE_RMS_uJy', 'STD_RMS_uJy', 'MIN_RMS_uJy',
                  'MAX_RMS_uJy']
stats_coltypes = ['S20', 'i4', 'f4', 'f4', 'f4', 'f4', 'f4']
stats_types = {k: v for k, v in zip(stats_colnames, stats_coltypes)}

explanation = __doc__


def arg_init():
    # code_path = os.path.dirname(os.path.abspath(survey.__file__))

    parser = ap.ArgumentParser(prog='racs_analysis', formatter_class=ap.RawDescriptionHelpFormatter,
                               description=__doc__,
                               epilog='See -x for more explanation')
    # noinspection PyTypeChecker
    parser.add_argument('img_name', nargs='*', help='RACS img name; no default')
    parser.add_argument('-n', '--noise_statistics', action='store_true', help="Determine rms noise")
    parser.add_argument('-q', '--quartile', action='store_true', help="Determine rms noise from IQR")
    parser.add_argument('-b', '--bright_src_errs', action='store_true', help="Assess fluctuations near bright sources")
    parser.add_argument('-m', '--median', action='store_true', help="Determine image median")
    parser.add_argument('-r', '--replace', action='store_true', help="Replace existing rms file")
    parser.add_argument('-e', '--epoch', default=0, type=int, help="Survey observation epoch")
    parser.add_argument('-l', '--literal', action='store_true', help='Input file as given')
    parser.add_argument('-d', '--workdir', default=os.getcwd(), help="Working directory")
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-x', '--explain', action='store_true', help="give an expanded explanation")
    return parser


def do_noise_statistics(in_files, survey, replace=False, fcor_stats=True, method='rms'):
    kw = {'db_update': False, 'do_replace': replace, 'fcor_stats': fcor_stats}
    n = 0
    for in_fits_file in in_files:
        inx = survey.get_row_from_prod_name(in_fits_file)
        s, f, pol = aks.parse_filename(in_fits_file)
        # print(in_fits_file, inx)
        if inx < 0:
            print("DB entry for {} not found".format(in_fits_file))
        else:
            print('inx = {:d}'.format(inx))
            st = sut.func_stats_info(survey, row_num=inx, stokes=pol, method=method, **kw)
            if st is not None:
                mos_st, rms_st = st
                fld, sb = survey.get_field_data(inx, ['FIELD_NAME', 'SBID'])

                out_row = [fld, sb, mos_st['NPIXV'], mos_st['MINIMUM'], mos_st['MAXIMUM'],
                           rms_st['median'], rms_st['mode'], rms_st['std'],
                           rms_st['minimum'], rms_st['maximum']]
                outfile = survey.db_dir.joinpath(aks.make_statistics_name(sb, fld))
                tab = Table(names=sut.stats_colnames, dtype=sut.stats_coltypes)
                tab.add_row(out_row)
                tab.write(str(outfile), format='ascii.csv', overwrite=True)
                print("out put to {}".format(str(outfile)))
                n += 1

    return n


def filter(hsib, flux_peak):
    ret = []
    for k, (h, f) in enumerate(zip(hsib, flux_peak)):
        if not h and f > 200.0:
            ret.append(k)
    return ret


def get_filtered_sources(beam_table):
    has_siblings = "col_has_siblings"
    flux_peak = "col_flux_peak"

    hs = beam_table.array[has_siblings]
    fpeak = beam_table.array[flux_peak]
    k0 = filter(hs, fpeak)
    return k0


def do_bright_src_errs(in_file, survey):
    inx = survey.get_row_from_prod_name(in_file)
    if inx < 0:
        print("DB entry for {} not found".format(in_file))
        sys.exit()

    rows = []

    ima = sut.get_product_name(survey, inx, 'mosaic')
    wgt = sut.get_product_name(survey, inx, 'weights')
    xml = sut.get_product_name(survey, inx, 'selavy-components')
    if ima.exists() and wgt.exists() and xml.exists():
        table = parse_single_table(xml)
        hdul_i = fits.open(ima)
        hdr = hdul_i[0].header
        data = np.squeeze(hdul_i[0].data)
        hdul_w = fits.open(wgt)
        wgts = np.squeeze(hdul_w[0].data)
        wgt_lim = np.nanmax(wgts) * 0.5
        w = WCS(hdr)
        refpix = [[int(hdr['CRPIX1']), int(hdr['CRPIX2']), 0, 0]]
        rw = w.wcs_pix2world(refpix, 0)
        w2, w3 = rw[0, 2], rw[0, 3]

        kinx = get_filtered_sources(table)
        print("{}  Found {:d}".format(in_file, len(kinx)))

        ras = table.array["col_ra_deg_cont"]
        decs = table.array["col_dec_deg_cont"]
        flux_peak = table.array["col_flux_peak"]
        flux_int = table.array["col_flux_int"]

        # k = kinx[0]
        world = np.array([[ras[k], decs[k], w2, w3] for k in kinx])
        # peaks = np.array([flux_peak[k] for k in kinx])
        # flux_i = np.array([flux_int[k] for k in kinx])
        pixel = w.wcs_world2pix(world, 0)
        print(wgt_lim)
        for p, w in zip(pixel, world):
            i, j = int(p[1]), int(p[0])
            if wgts[i, j] > wgt_lim:
                r1 = np.nanmin(data[i - 30:i + 30, j - 30:j + 30])
                r2 = np.nanmax(data[i - 30:i + 30, j - 30:j + 30])
                if not (np.isnan(r1) or np.isnan(r2)):
                    row = np.concatenate((w, [r1, r2]))
                    rows.append(row)
                else:
                    print(i, j, wgts[i, j], w[:2], r1, r2)
    else:
        print("ima/wgt/xml {} {} {}".format(ima.exists(), wgt.exists(), xml.exists()))
    return inx, np.array(rows)


def write_b_err(db, fld, sb, data):
    b_name = aks.make_brt_err_csv_name(sb, fld)
    b_path = db.joinpath(b_name)

    b_tab = Table(names=b_err_colnames, dtype=b_err_coltypes)
    for r in data:
        rad, decd = r[:2]
        brmin, brmax = r[4:]
        row = [rad, decd, brmin, brmax]
        b_tab.add_row(row)
    b_tab.sort('BR_MAX', reverse=True)
    b_tab.write(str(b_path), format='ascii.csv', overwrite=True)


def write_stats(db, in_table):
    s_name = aks.image_stats_name
    s_path = db.joinpath(s_name)
    if s_path.exists():
        stats_table = ascii.read(s_path, format='csv')
    else:
        stats_table = Table(names=stats_colnames, dtype=stats_coltypes)
    flds = stats_table['FLD_NAME']
    sbids = stats_table['SBID']
    for r in in_table:
        stats_table.add_row(r)
    stats_table = unique(stats_table, keys=['FLD_NAME', 'SBID'], keep='last')
    stats_table.write(str(s_path), format='ascii.csv', overwrite=True)


def set_warn_filters():
    warnings.filterwarnings('ignore', category=AstropyWarning, append=True)


def main():
    set_warn_filters()

    args = arg_init().parse_args()
    run_date = time.strftime("%Y%m%d-%H%M%S")

    if args.explain:
        print(explanation)
        sys.exit()

    print("")
    print("Running survey_analysis.py with the following input:")
    print("ARGS = ", args)
    print("")

    epoch = args.epoch
    survey = ASKAP_Survey_factory(epoch=epoch, verbose=args.verbose)

    print("")
    cwd = os.getcwd()
    print("CWD = {}".format(cwd))
    in_files = args.img_name
    if args.img_name:
        in_files = args.img_name
        if in_files[0].startswith('@'):
            in_list = in_files[0][1:]
            print("\nList of files in {}".format(in_list))
            files = open(in_list, 'r').readlines()
            in_files = [f.strip() for f in files]

    os.chdir(args.workdir)  # change to working directory
    if args.verbose:
        print("-----------")
        for fi in in_files:
            print(fi)
        print("-----------")
    ops = []
    if args.noise_statistics:
        ops.append('rms')
    if args.quartile:
        ops.append('iqr')
    if args.median:
        ops.append('med')

    replace = args.replace
    # ------------------------------------------------------------------------------------------------------------------
    db = survey.db_dir
    # out_dir = Path(survey.get_data_root())
    if args.literal:
        for in_file in in_files:
            for op in ops:
                file = Path(in_file)
                outdir = Path('.')
                print(str(file.stem))
                mos_st, stats, fname = ims.image_cell_statistic(file, outdir, statistic=op, replace_old=replace)
    else:
        for op in ops:
            n = do_noise_statistics(in_files, survey, replace=replace, method=op)
            print("{:d} images processed".format(n))

    if args.bright_src_errs:
        for in_file in in_files:
            inx, rows = do_bright_src_errs(in_file, survey)
            for r in rows:
                print("{:6.2f}, {:6.2f}  {:7.1f} {:6.1f}".format(r[0], r[1], r[4] * 1000.0, r[5] * 1000.0))
            fld, sb = survey.get_field_data(inx, ['FIELD_NAME', 'SBID'])
            write_b_err(db, fld, sb, rows)


if __name__ == "__main__":
    sys.exit(main())
