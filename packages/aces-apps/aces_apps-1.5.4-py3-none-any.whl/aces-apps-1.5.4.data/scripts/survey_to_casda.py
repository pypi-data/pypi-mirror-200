#!/usr/bin/env python
"""
This writes the input parset for the casdaupload script.

See https://www.atnf.csiro.au/computing/software/askapsoft/sdp/docs/current/utils/casdaupload.html

-------------------------------------------------------------

"""
import sys
import os
import re
import time
import argparse as ap
from pathlib import Path
import glob
from aces.racs.racs_survey import ASKAP_Survey_factory
import aces.racs.survey_utils as sut
from astropy.time import Time
from astropy.io import fits
import tarfile

NOFORMAT = '{noformat}\n'

explanation = __doc__

casda_production = '/group/casda/prd/'
casda_test = '/group/casda/at'
got_leakage = False

general = """# General
outputdir                       = "{}"
useAbsolutePaths                = true
telescope                       = ASKAP
sbid                            = {:d}
# No other sbids provided.
obsprogram                      = RACS
writeREADYfile                  = true

"""

image = {'cont_restored_T0': ['mosaic_fcor_tt0', 'mosaic_cres_fcor_tt0'],
         'cont_weight_T0': ['weights_fcor_tt0', 'weights_cres_fcor_tt0'],
         'cont_restored_T1': ['mosaic_fcor_tt1', 'mosaic_cres_fcor_tt1'],
         'cont_weight_T1': ['weights_fcor_tt1', 'weights_cres_fcor_tt1'],
         'cont_noise_T0': ['mosaic_fcor_iqr'],
         'cont_components_T0': ['mosaic_components_tt0'],
         'cont_fitresidual_T0': ['mosaic_fitresidual_tt0']}
catalogue = {'continuum-component': 'selavy-components_cres_fcor',
             'continuum-island': 'selavy-islands_cres_fcor'}

im_art = """
# Images
images.artifactlist             = {}"""

ca_art = """
# Source catalogues
catalogues.artifactlist             = {}"""

ms_art = """
# Measurement sets
measurementsets.artifactlist             = {}"""

ev_art = """
# Evaluation reports
evaluation.artifactlist             = {}"""

ke_fil = {'im': "image{:d}.filename = {}",
          'ca': "cat{:d}.filename = {}",
          'ms': "ms{:d}.filename = {}",
          'ev': "eval{:d}.filename = {}"}

ke_typ = {'im': "image{:d}.type = {}",
          'ca': "cat{:d}.type = {}"}

ke_pro = {'im': "image{:d}.project = {}",
          'ca': "cat{:d}.project = {}",
          'ms': "ms{:d}.project = {}",
          'ev': "eval{:d}.project = {}"}

ke_fmt = {'ev': "eval{:d}.format = {}"}

ke_art = {'im': im_art, 'ca': ca_art, 'ms': ms_art, 'ev': ev_art}

"""
# The following uses an original code by Matthew Whiting <Matthew.Whiting@csiro.au>
# As described below.  Here the essentials are extracted as a subroutine to be called by the main racs_to_casda
#
# A python script to update the header keywords of FITS files. The
# headers able to be updated are a small defined set: PROJECT, SBID,
# DATE-OBS, DURATION.
#
# It also allows the specification of HISTORY statments, by giving a
# list of strings following the arguments for the above
#
# Example Usage:
#   updateFITSheaders.py --project=AS034 --SBID=1234 --DATE-OBS="2017-01-20T12:34:45" --DURATION=12345.6 "Made by me" "Not by you"
#
#
# @copyright (c) 2017 CSIRO
# Australia Telescope National Facility (ATNF)
# Commonwealth Scientific and Industrial Research Organisation (CSIRO)
# PO Box 76, Epping NSW 1710, Australia
# atnf-enquiries@csiro.au
#
# This file is part of the ASKAP software distribution.
#
# The ASKAP software distribution is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the License,
# or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
#
# @author Matthew Whiting <Matthew.Whiting@csiro.au>
#

import argparse
import astropy.io.fits as fits

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--fitsfile', type=str, help='FITS file to update')
parser.add_argument('--telescope', type=str, default="", help='TELESCOP keyword')
parser.add_argument('--project', type=str, default="", help='OPAL project ID for this observation')
parser.add_argument('--sbid', type=str, default="", help='Scheduling block ID for this observation')
parser.add_argument('--dateobs', type=str, default="", help='DATE-OBS string (YYYY-MM-DDTHH:MM:SS) for this observation')
parser.add_argument('--duration', type=str, default="", help='Length of this observation in sec')
parser.add_argument('history', metavar='hist', type=str, default="", nargs='*', help='A HISTORY statement')
options = parser.parse_args()
"""

required_fits_keys = ['NAXIS{:d}', 'CTYPE{:d}', 'CRVAL{:d}', 'CDELT{:d}', 'CRPIX{:d}']


def update_FITS_header(options):
    if options.fitsfile == "":
        exit(1)

    hdulist = fits.open(options.fitsfile, 'update', ignore_missing_end=True)
    hdr1 = hdulist[0].header

    headerChanged = False

    def addHeader(header, keyword, value):
        addIt = True
        addIt = addIt and value != ''
        if header.__contains__(keyword):
            addIt = addIt and header[keyword] != value
        if addIt:
            print("updateFITSheaders: Setting %s to %s" % (keyword, value))
            header[keyword] = value
        return addIt

    headerChanged = addHeader(hdr1, 'TELESCOP', options.telescope) or headerChanged
    headerChanged = addHeader(hdr1, 'PROJECT', options.project) or headerChanged
    headerChanged = addHeader(hdr1, 'SBID', options.sbid) or headerChanged
    headerChanged = addHeader(hdr1, 'DATE-OBS', options.dateobs) or headerChanged
    headerChanged = addHeader(hdr1, 'DURATION', options.duration) or headerChanged

    if headerChanged:
        for history in options.history:
            match = False
            # print(hdr1.keys())
            if hdr1.__contains__('HISTORY'):
                for line in hdr1['HISTORY']:
                    match = match or (line == history)
            if not match:
                print("updateFITSheaders: New HISTORY line: %s" % history)
                hdr1.add_history(history)

        while len(hdulist) > 1:
            hdulist.pop()

        print("updateFITSheaders: Updating file %s" % options.fitsfile)
        hdulist.flush()


def fits_header_check(file_name):
    # Check that all key words for all axes are present.
    fits_file = fits.open(file_name)
    fits_header = fits_file[0].header

    keys = [a for a in fits_header.keys()]

    nax = fits_header['NAXIS']
    ax_nums = range(1, nax+1)
    header_good = True
    err_messages = []
    for a in ax_nums:
        for ki in required_fits_keys:
            kia = ki.format(a)
            if kia not in keys:
                header_good = False
                err_messages.append("{} not found".format(kia))
    return header_good, err_messages


class Options(object):
    def __init__(self, fitsfile, sbid, dateobs, duration, telescope='ASKAP', project='AS110'):
        self.fitsfile = fitsfile
        self.telescope = telescope
        self.project = project
        self.sbid = sbid
        self.dateobs = dateobs
        self.duration = duration


def update_FITS_headers(files, row, history):
    sbid = str(row['SBID'])
    dateobs = t_string(row['SCAN_START']).replace(' ', 'T')
    duration = row['SCAN_LEN']
    for file in files:
        if 'test' not in file:
            file = file.replace('RACS_', 'RACS_test4_1.05_')
        if file.endswith('.fits'):
            options = Options(file, sbid, dateobs, duration)
            options.history = history
            update_FITS_header(options)


def arg_init():
    # code_path = os.path.dirname(os.path.abspath(survey.__file__))

    parser = ap.ArgumentParser(prog='survey_to_casda.py', formatter_class=ap.RawDescriptionHelpFormatter,
                               description=__doc__,
                               epilog='See -x for more explanation')
    # noinspection PyTypeChecker
    parser.add_argument('sbid', type=int, help='RACS SBID; no default.')
    parser.add_argument('-t', '--test', action='store_true', help="Upload to the CASDA test environment")
    parser.add_argument('-f', '--field', default=None, help="Field to select")
    parser.add_argument('-e', '--epoch', default=0, type=int, help="Survey observation epoch")
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-x', '--explain', action='store_true', help="give an expanded explanation")
    return parser


def t_string(db_time):
    time_val = Time(db_time / 3600.0 / 24.0, format='mjd', scale='utc')
    time_val.format = 'iso'
    return "{}".format(time_val)


def my_grep(file_name, txt):
    lines = open(file_name, 'r').readlines()
    p = False
    for li in lines:
        q = True
        for t in txt:
            q = q and bool(re.search(t, li))
        p = p or q
    return p


def get_input(file_name, key):
    lines = open(file_name, 'r').readlines()
    lines = [li.strip() for li in lines]
    p = None
    for li in lines:
        if li.startswith(key):
            p = li.split('=')[1]
    return p


def find_parset(root, row):
    r = row
    mos_time = r['MOSAIC_TIME']
    field = r['FIELD_NAME']
    if 'test4' not in field:
        field = field.replace('RACS_', 'RACS_test4_1.05_')

    sbid, csb = r['SBID', 'CAL_SBID']

    mos_before = mos_time - 86400.0
    mos_after = mos_time + 86400.0
    day0 = t_string(mos_before).split(' ')[0]
    day1 = t_string(mos_time).split(' ')[0]
    day2 = t_string(mos_after).split(' ')[0]
    # print('   ', day0, day1)

    gtmp0 = "{}/{:d}/slurmOutput/racs_pipeline*{:d}*{}*.sh".format(root, csb, sbid, day0)
    gtmp1 = "{}/{:d}/slurmOutput/racs_pipeline*{:d}*{}*.sh".format(root, csb, sbid, day1)
    gtmp2 = "{}/{:d}/slurmOutput/racs_pipeline*{:d}*{}*.sh".format(root, csb, sbid, day2)
    parfiles = glob.glob(gtmp0) + glob.glob(gtmp1) + glob.glob(gtmp2)
    key = 'FIELD_SELECTION_SCIENCE'
    # print("Found {:d} possible .sh files".format(len(parfiles)))
    # print(parfiles)
    parfile = None
    if len(parfiles) == 0:
        print("G0 {}".format(gtmp0))
        print("G1 {}".format(gtmp1))
    elif len(parfiles) == 1:
        parfile = parfiles[0]
    else:
        flags = []
        for pf in parfiles:
            val = get_input(pf, key)
            if val is None:
                sp = (False, False)
            else:
                val = get_input(pf, key).replace('"', '')
                # print("({}) ({})".format(val, field))
                if val == field:
                    sp = (True, True)
                else:
                    sp = (True, False)
            flags.append(sp)
        for pf, sp in zip(parfiles[::-1], flags[::-1]):
            if (sp == (True, True)) or (sp == (False, False)):
                parfile = pf
        if parfile is None:
            for pf in parfiles:
                print("field {}  -- {}".format(field, pf))
    return parfile


def get_history(parfile):
    lines = open(parfile, 'r').readlines()
    lines = [li.strip() for li in lines]
    history = []
    for li in lines:
        if li.startswith('# Processed'):
            history.append(li[2:])
    return history


def check_files_exist(files):
    ret = True
    for f in files:
        if not Path(f).exists():
            ret = False
            print("missing {}".format(f))
    return ret


def pack_flag_cal(root, row):
    # Find and pack into a tar file certain flag summaries and cal tables.
    """
    BPCAL/calparameters_1934_bp_SB{cal_sbid}.tab/
    {fld}/cont_gains_cal_SB{sbid}_{fld}.beam??.tab/
    diagnostics/Flagging_Summaries/scienceData_SB{sbid}_{fld}.beam??_averaged.ms.flagSummary
    """
    csb, sb, fld = row['CAL_SBID', 'SBID', 'FIELD_NAME']
    fld_test4 = fld.replace('RACS_', 'RACS_test4_1.05_')
    da = root.joinpath("{:d}".format(csb))
    bp = da.joinpath('BPCAL')

    g_bpcal = str(bp.joinpath("calparameters_1934_bp_SB{:d}.tab".format(csb)))
    g_gains = str(da.joinpath("{}".format(fld))) + "/cont_gains_cal_SB{:d}_{}.beam??.tab".format(sb, fld)
    g_flags = str(da.joinpath('diagnostics').joinpath('Flagging_Summaries')) + \
              "/scienceData_SB{:d}_{}.beam??_averaged.ms.flagSummary".format(sb, fld)
    g_flagt = str(da.joinpath('diagnostics').joinpath('Flagging_Summaries')) + \
              "/scienceData_SB{:d}_{}.beam??_averaged.ms.flagSummary".format(sb, fld_test4)

    bpc = glob.glob(g_bpcal)
    gai = glob.glob(g_gains)
    fla = glob.glob(g_flags) + glob.glob(g_flagt)
    tfile = da.joinpath("calibration-flags_SB{:d}_{}.tar".format(sb, fld))

    tar = tarfile.TarFile(name=str(tfile), mode='w', dereference=True)
    # tar = tarfile.open(str(tfile), "w")
    for name in bpc + gai + fla:
        tar.add(name)
    tar.close()

    return tfile


def main():
    args = arg_init().parse_args()
    run_date = time.strftime("%Y%m%d-%H%M%S")

    if args.explain:
        print(explanation)
        sys.exit()

    print("")
    print("Running survey_to_casda.py with the following input:")
    print("ARGS = ", args)
    print("")
    print(run_date)
    print("")

    os.system("module load askaputils")
    print("Loading RACS database ...")
    sbid = args.sbid
    epoch = args.epoch
    aks = ASKAP_Survey_factory(epoch=epoch)

    if args.field is None:
        print("Determining field names")
        tab = aks.f_table
        msk = tab['CAL_SBID'] == sbid
        fields = list(tab[msk]['FIELD_NAME'])
    else:
        fields = [args.field]

    casda_env = casda_production
    if args.test:
        casda_env = casda_test

    projId = 'AS110'
    images = ['cont_restored_T0', 'cont_weight_T0', 'cont_noise_T0',
              'cont_components_T0', 'cont_fitresidual_T0',
              'cont_restored_T1', 'cont_weight_T1']
    catalogues = ['continuum-component', 'continuum-island']

    ta = aks.f_table
    root = aks.get_data_root()
    mk = (ta['SBID'] == sbid) & (ta['SELECT'] == 1)
    tab = ta[mk]
    cal_sbid = tab[0]['CAL_SBID']
    csb_dir = root.joinpath("{:d}".format(cal_sbid))
    print(str(csb_dir))
    os.chdir(csb_dir)

    print("len(tab) = ", len(tab))
    image_lines = []
    cat_lines = []
    ms_lines = []
    ev_lines = []

    im_arti = []
    ca_arti = []
    ms_arti = []
    ev_arti = []

    all_files = []
    fits_files = []
    all_history = []

    # Collect the eval files first so that the history can be recovered.
    j = 0
    k = 'ev'
    # Ensure that no parfiles are entered moree than once.
    parfile_list = []
    for r in tab:
        # Now find the pipeline parset:
        parfile = find_parset(root, r)
        if parfile == None:
            print("No param file found - FATAL")
            exit(1)
        else:
            all_history.append(get_history(parfile))
            if parfile not in parfile_list:
                parfile_list.append(parfile)
                fn = csb_dir.joinpath(parfile)
                fnn = str(fn).replace('test4_1.05_', '')
                ev_arti.append('eval{:d}'.format(j))
                ev_lines.append(ke_fil[k].format(j, fnn))
                ev_lines.append(ke_fmt[k].format(j, 'txt'))
                ev_lines.append(ke_pro[k].format(j, projId))
                j += 1
                all_files.append(fnn)

        # now the validation tar
        fn = str(csb_dir.joinpath("validation_SB{:d}_{}.tar".format(sbid, r['FIELD_NAME'])))
        fnn = str(fn).replace('test4_1.05_', '')
        ev_arti.append('eval{:d}'.format(j))
        ev_lines.append(ke_fil[k].format(j, fnn))
        ev_lines.append(ke_fmt[k].format(j, 'validation-report'))
        ev_lines.append(ke_pro[k].format(j, projId))
        j += 1
        all_files.append(fnn)

        tfile = str(pack_flag_cal(root, r))
        ev_arti.append('eval{:d}'.format(j))
        ev_lines.append(ke_fil[k].format(j, tfile))
        ev_lines.append(ke_fmt[k].format(j, 'calibration'))
        ev_lines.append(ke_pro[k].format(j, projId))
        j += 1
        all_files.append(tfile)

    j = 0
    k = 'im'
    for r, history in zip(tab, all_history):
        r_inx = r['INDEX']

        for im in images:
            for which in image[im]:
                fn = sut.get_product_name(aks, r_inx, which)
                if fn is not None:
                    fnn = str(fn).replace('test4_1.05_', '')
                    im_arti.append('image{:d}'.format(j))
                    image_lines.append(ke_fil[k].format(j, fnn))
                    image_lines.append(ke_typ[k].format(j, im))
                    image_lines.append(ke_pro[k].format(j, projId))
                    j += 1
                    all_files.append(fnn)
                    fits_files.append(fnn)
                else:
                    print(im, 'absent')

        update_FITS_headers(fits_files, r, history)
        print('Checking FITS file headers ...')
        all_good = True
        for f_file in fits_files:
            h_good, err_mess = fits_header_check(f_file)
            if not h_good:
                all_good = False
                print("{} has bad header".format(f_file))
                for e in err_mess:
                    print("   {}".format(e))
        if all_good:
            print("   all OK\n")
        else:
            return 1

    # catalogues
    j = 0
    k = 'ca'
    for r in tab:
        r_inx = r['INDEX']
        for ca in catalogues:
            which = catalogue[ca]
            fn = sut.get_product_name(aks, r_inx, which)
            if fn is not None:
                fnn = str(fn).replace('test4_1.05_', '')
                ca_arti.append('cat{:d}'.format(j))
                cat_lines.append(ke_fil[k].format(j, fnn))
                cat_lines.append(ke_typ[k].format(j, ca))
                cat_lines.append(ke_pro[k].format(j, projId))
                j += 1
                all_files.append(fnn)
            else:
                print(ca, 'absent')
    j = 0
    k = 'ms'
    for r in tab:
        r_inx = r['INDEX']
        if got_leakage:
            which = 'ms_av_cal_lk'
        else:
            which = 'ms_av_cal'
        fns = sut.get_product_name(aks, r_inx, which)
        for fn in fns:
            if fn is not None:
                fnn = str(fn).replace('test4_1.05_', '')
                ms_arti.append('ms{:d}'.format(j))
                ms_lines.append(ke_fil[k].format(j, fnn))
                ms_lines.append(ke_pro[k].format(j, projId))
                j += 1
                all_files.append(fnn)

    if args.verbose:
        print('---------\n')
        print('[{}]'.format(','.join(im_arti)))
        for li in image_lines:
            print(li)
        print('\n')

        print('[{}]'.format(','.join(ca_arti)))
        for li in cat_lines:
            print(li)

        print('[{}]'.format(','.join(ms_arti)))
        for li in ms_lines:
            print(li)

    in_prov = 'casda_upload_{:d}.in_provisional'.format(sbid)
    in_final = 'casda_upload_{:d}.in'.format(sbid)
    fout = open(in_prov, 'w')
    fout.write(general.format(casda_env, sbid) + '\n')
    fout.write(im_art.format('[{}]'.format(','.join(im_arti)) + '\n'))
    for li in image_lines:
        fout.write(li + '\n')

    fout.write(ca_art.format('[{}]'.format(','.join(ca_arti)) + '\n'))
    for li in cat_lines:
        fout.write(li + '\n')

    fout.write(ms_art.format('[{}]'.format(','.join(ms_arti)) + '\n'))
    for li in ms_lines:
        fout.write(li + '\n')

    fout.write(ev_art.format('[{}]'.format(','.join(ev_arti)) + '\n'))
    for li in ev_lines:
        fout.write(li + '\n')
    fout.close()

    all_present = check_files_exist(all_files)
    if all_present:
        os.rename(in_prov, in_final)
        print("casdaupload input file {}".format(in_final))
    else:
        print("There are missing files.\n  casdaupload input file {}".format(in_prov))


if __name__ == "__main__":
    sys.exit(main())
