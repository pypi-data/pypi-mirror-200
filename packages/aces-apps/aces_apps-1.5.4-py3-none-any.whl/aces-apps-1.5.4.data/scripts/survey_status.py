#!/group/askap/mcc381/miniconda3/envs/aces/bin/python
"""
#!/usr/bin/env python
"""

import argparse as ap
import sys
import os

import aces.sefd.ASKAP_msdata__cc as akms
import askap.parset.parset as ps
import aces.survey.survey_utils as asu
from aces.survey.survey_class import ASKAP_Survey_factory

import numpy as np
from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.io import ascii
from astropy.table import Table, Column

from pathlib import Path

# done : Write utility functions into a separate .py
# done : Make csv file names more meaningful - specifically the beam image files.
# done : Expect to run this from a directory with subdirectory db.
# done : change number of files below generic.
# todo : create db if not present
# done : MB together should work

explanation = """
survey_status.py is the script to keep track of the bookkeeping for ASKAP surveys.
It is a prototype, derived from the equivalent software written for RACS.
----------------------------------------------------------------------
This script initiates the database for an epoch of observations for an ASKAP survey.
It also allows updates to be made with each new observing session.

The life cycle of this database is as follows.
1. Creation from observing parset. This can be done before the observation. The given parset must hold the
full specification of this epoch survey; that is all fields are defined even if only a subset are observed in any
given scheduling block.

2. Add observing information; from the field to SBID mapping provided, the MeasurementSets are read for information
that is added to the database.

3. Add image information. 

The database consists of a description table and a set of directories containing other tables. For each survey epoch
there is a row in the description file, and a directory of tables.

In each epoch directory are tables, including:
 - field_table : with a row for each field observation (within a single epoch a field observation maybe repeated).
 - beam_table : one table for each row in the field_table, each with a row for each beam.
 - other tables as needed.


(1) To create a database and initialise the field_table
        survey_status.py -s <survey name> -e <epoch> -p <observing parset>

(2) To update the database with observation information
        survey_status.py -s <survey name> -e <epoch> -s <observation record>
        
    Steps 1 and 2 can be performed with a single execution as 
        survey_status.py -s <survey name> -e <epoch> -p <observing parset> -s <observation record>

(3) To update the database with image-specific information, selected according to the image_info argument:
    M - mosaic image
    B - beam images
    S - image statistics
    A - astrometry (beam-beam)
    C - catalogue compare
    P - polarization leakage

first csv file to keep track of the observations. This 
is run by calling:

survey_status.py -s <survey name> -e <epoch> -p <observing parset> -s <observation record>

- <observing>.parset is the parset used to create the observations. 
- <observation_record>.csv is the observing record (original from Aidan). However,
    easy to re-create. The file needs to be in CSV format and contain the columns:

    id,field,selected,scheduled,sbid,observed,processed,quality,casda

    For example:
    10,RACS_test4_1.05_0805-71A,,,,,,,
    100,RACS_test4_1.05_2131-56A,1,1,8676,1,,,

The files created are:
  descriptor - created if necessary, appended otherwise; has columns:
    EPOCH, OBS_FREQ, FOOTPRINT, PITCH, ROTATION, DURATION, POL_MODE, DB_FILE
  data_base directory that contains:
    field_data -  the master csv file for the bookkeeping with columns:
      INDEX, SRC,	FIELD_NAME, SBID, SCAN, CAL_SBID, STATE, RA_HMS, DEC_DMS, RA_DEG, DEC_DEG,
      GAL_LONG, GAL_LAT, POL_AXIS, SCAN_START, SCAN_LEN, MED_RMS_uJy,
      MODE_RMS_uJy, STD_RMS_uJy, MIN_RMS_uJy, MAX_RMS_uJy,
      PSF_MAJOR, PSF_MINOR, PSF_ANGLE
    beam_data - for each field observation (row in field_data):
      BEAM_NUM, DATE, RA_HMS, DEC_DMS, RA_DEG, DEC_DEG, GAL_LONG, GAL_LAT,
      PSF_MAJOR, PSF_MINOR, PSF_ANGLE

The last 8 columns will be empty as these fill up after calibration and imaging.

"""
"""
Other columns of data that would be useful:
1. Information about data products:
 - date produced
 - software version
 - how many beam (valid) images for each Stokes parameter (MFS)
 - how many (valid) mosaic images for each Stokes parameter (MFS)
 - how many cubes for each Stokes parameter, and whether reduced to cubelets.
 
survey_status.py -p  survey_epoch_<#>.parset -s survey_record_epoch_<#>.csv -g <new_csv_file>.csv -u

- survey_epoch_<#>.parset is the parset used to create the observations. 
- survey_record_epoch_<#>.csv is the observing record (original from Aidan). However,
    easy to re-create. The file needs to be in CSV format and contain the columns:

    id,field,selected,scheduled,sbid,observed,processed,quality,casda

    For example:
    10,RACS_test4_1.05_0805-71A,,,,,,,
    100,RACS_test4_1.05_2131-56A,1,1,8676,1,,,
    
- <new_csv_file>.csv is the updated bookkeeping csv file. Originally this file would be 
    downloaded from google sheets as this is where the modifying is done as the processing
    of the fields commences. This will have the columns:
    
    SRC	FIELD_NAME, SBID, STATE, RA_HMS, DEC_DMS, RA_DEG, DEC_DEG, GAL_LONG, GAL_LAT,
    OBS_FREQ, FOOTPRINT, PITCH, ROTATION, DURATION, POL_MODE, POL_AXIS, SB_TIME, 
    SB_START_DATE, SB_START_TIME, SB_END_DATE, SB_END_TIME, CAL_SBID, MED_RMS_uJy,
    MODE_RMS_uJy, STD_RMS_uJy, MIN_RMS_uJy, MAX_RMS_uJy, PSF_MAJOR, PSF_MINOR, PSF_ANGLE

Using the -u (--update) lets you update the csv file with the new fields that have been observed.
Will created a new csv file with the same information as before, just with new SBIDs if required.

    
The required input are:

- survey_epoch_<#>.parset is the parset used to create the observations. 
- survey_record_epoch_<#>.csv is the observing record (original from Aidan). However,
    easy to re-create. The file needs to be in CSV format and contain the columns:

    id,field,selected,scheduled,sbid,observed,processed,quality,casda

    For example:
    10,RACS_test4_1.05_0805-71A,,,,,,,
    100,RACS_test4_1.05_2131-56A,1,1,8676,1,,,
    
- <new_csv_file>.csv is the updated bookkeeping csv file. Originally this file would be 
    downloaded from google sheets as this is where the modifying is done as the processing
    of the fields commences. This will have the columns:
    
    SRC	FIELD_NAME, SBID, STATE, RA_HMS, DEC_DMS, RA_DEG, DEC_DEG, GAL_LONG, GAL_LAT,
    OBS_FREQ, FOOTPRINT, PITCH, ROTATION, DURATION, POL_MODE, POL_AXIS, SB_TIME, 
    SB_START_DATE, SB_START_TIME, SB_END_DATE, SB_END_TIME, CAL_SBID, MED_RMS_uJy,
    MODE_RMS_uJy, STD_RMS_uJy, MIN_RMS_uJy, MAX_RMS_uJy, PSF_MAJOR, PSF_MINOR, PSF_ANGLE

Using the -u (--update) lets you update the csv file with the new fields that have been observed.
Using the -a (--analysis) lets you update the csv file with the new fields that have been observed.

- survey_stats_<date>.csv is the output file from survey_analysis.py which returns the image
    statistics. The file has columns:
    
    FLD_NAME,MED_RMS_uJy,MODE_RMS_uJy,STD_RMS_uJy,MIN_RMS_uJy,MAX_RMS_uJy,PSF_MAJ,PSF_MIN,PSF_PA


 
"""
survey_colnames = ['SURVEY_NAME']
survey_coltypes = ['S12']

desc_colnames = ['EPOCH', 'OBS_FREQ', 'FOOTPRINT', 'PITCH',
                 'ROTATION', 'DURATION', 'POL_MODE', 'DATABASE', 'PRODUCT_ROOT']
desc_coltypes = ['i4', 'f4', 'S20', 'f4', 'f4', 'f4', 'S12', 'S80', 'S80']

states = {'NULL': '--NULL--', 'OBSERVED': 'OBSERVED', 'IMAGING': 'IMAGING', 'IMAGED': 'IMAGED', 'ERROR': 'ERROR'}
not_observed = states['NULL']
observed = states['OBSERVED']
imaged = states['IMAGED']
global_verbose = False


def vprint(*args):
    if global_verbose:
        print(*args)


def arg_init():
    parser = ap.ArgumentParser(prog='survey_status', formatter_class=ap.RawDescriptionHelpFormatter,
                               description='Produce a csv file of the current status of survey',
                               epilog='See -x for more explanation')
    # noinspection PyTypeChecker
    parser.add_argument('-s', '--survey', default=None, type=str, help="Survey name")
    parser.add_argument('-e', '--epoch', default=0, type=int, help="Survey observation epoch")
    parser.add_argument('-p', '--parset', help="Name of the survey observing parset")
    parser.add_argument('-m', '--mapping_file', type=str, help="Name of the survey summary file")
    parser.add_argument('-c', '--cat_params', type=str, help="Name of catalogue compare param file")
    parser.add_argument('-r', '--product_root', type=str, help="Root directory for survey products")
    parser.add_argument('-n', '--numbers', type=int, nargs='*', help="Row numbers to process")
    parser.add_argument('-b', '--bounds', type=int, nargs='*', help="Row number bounds")
    parser.add_argument('-S', '--sbid', type=int, nargs=1, help="Select by SBID")
    parser.add_argument('-C', '--calsbid', type=int, nargs=1, help="Select by CAL SBID")
    parser.add_argument("-O", "--overwrite", dest="check_stale", action="store_false", 
        help="Re-do ALL cross-matching")
    parser.add_argument("-P", "--pols", type=str, nargs="*", default=["v"],
        help="Specify which polarizations [q, u, and/or v] to obtain leakage for")

    parser.add_argument('-i', '--image_info', nargs='*', type=str, help="Get image information [MBSAC]")
    parser.add_argument('-w', '--workdir', default=Path.cwd(), help="Current working directory")
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-x', '--explain', action='store_true', help="give an expanded explanation")
    return parser


# -------------------------------------------------------------------------------
def dec2deg(ra_hms, dec_dms):
    """
    DEC2DEG - convert coordinates to decimal degrees and galactic coordinates
    :param ra_hms: RA in hh:mm:ss.sssss
    :param dec_dms: DEC in dd:mm.ss.ssss
    :return: [RA in degrees, DEC in degrees, Long in degrees, Lat in degrees]
    """
    sc = SkyCoord(ra_hms, dec_dms, frame='icrs', unit=(u.hour, u.deg))
    rastr = sc.ra.to_string(unit='hour', sep=' ', pad=True)
    decstr = sc.dec.to_string(unit='deg', sep=' ', pad=True, alwayssign=True)
    return [sc.icrs.ra.degree, sc.icrs.dec.degree, sc.galactic.l.degree, sc.galactic.b.degree,
            rastr, decstr]


def from_ra_dec_deg(ra, dec):
    sc = SkyCoord(ra, dec, frame='icrs', unit="deg")
    return [sc.icrs.ra.degree, sc.icrs.dec.degree, sc.galactic.l.degree, sc.galactic.b.degree]


# -------------------------------------------------------------------------------
def get_scan_info_from_ms(sb):
    # Get information about scans from a measurementset for this SBID.
    try:
        ms_file = akms.get_msname(sb)
        ms_obj = akms.MSData(ms_file)
        info = ms_obj.get_scan_info()

    except IOError:
        print('MS file for {:d} inaccessible. Continue without scan information.'.format(sb))
        info = None

    return info


def parset_to_field_table(parset_file):
    # This is part (i) of the table building task:
    #
    #   i) extract all data from parset, and fill spare columns with FILL (whatever is chosen)
    #  ii) For rows in the input table that need it, extract scan info from ms.
    # iii) Other columns can be supploed with data from other sources.
    #
    # open the survey_record.csv file that one gets from Aidan on a semi regular basis
    # ------------------

    parset = ps.ParameterSet(parset_file)  # open the parset file
    duration = parset['common.target.src%d.duration']  # integration time for each science field
    footprint = parset['common.target.src%d.footprint.name']  # name of footprint used for observations
    pitch = parset['common.target.src%d.footprint.pitch']  # pitch used for the observations
    rotation = parset['common.target.src%d.footprint.rotation']  # rotation used for the observations
    obsfreq = parset['common.target.src%d.sky_frequency']  # observing frequency

    # Before composing the descriptor row, we need some information from the parset field keys
    keys = parset.keys()
    field_keys = [a for a in keys if 'field_name' in a and "%d" not in a]
    n_fields = len(field_keys)
    src_numbers = sorted([int(a.split('.')[2][3:]) for a in field_keys])

    # We assume that the pol_axis mode is the same for every field - good assumption for RACS, VAST
    key = "common.target.src{:d}.pol_axis".format(src_numbers[0])
    pol_mode = parset[key][0]  # polar axis = [mode, angle]

    # Now complete the desc_table:
    # EPOCH, OBS_FREQ, FOOTPRINT, PITCH, ROTATION, DURATION, POL_MODE, DATABASE, PRODUCT_ROOT, VARIANT
    row = [-1, obsfreq, footprint, pitch, rotation, duration, pol_mode, '', '']

    fld, fld_direction, fld_pol, r_deg, d_deg, l_deg, b_deg, ra_hms, dec_dms = [], [], [], [], [], [], [], [], []
    for ii in src_numbers:
        # extract information from the parset file
        fld.append(parset['common.target.src{}.field_name'.format(ii)])  # survey field name
        fld_direction = parset['common.target.src{}.field_direction'.format(ii)]  # survey field coordinates
        fld_pol.append(parset['common.target.src{}.pol_axis'.format(ii)][1])  # survey field axis angle

        # convert position to degrees and galactic coords

        fld_dir = dec2deg(fld_direction[0], fld_direction[1])
        r_deg.append(fld_dir[0])
        d_deg.append(fld_dir[1])
        l_deg.append(fld_dir[2])
        b_deg.append(fld_dir[3])
        ra_hms.append(fld_dir[4])
        dec_dms.append(fld_dir[5])

    field_table = Table()
    field_table['INDEX'] = range(n_fields)
    field_table['SRC'] = src_numbers
    field_table['FIELD_NAME'] = fld
    field_table['SBID'] = -1
    field_table['SCAN'] = -1
    field_table['CAL_SBID'] = -1
    statecol = Column([not_observed] * n_fields, name='STATE', dtype='S10')
    field_table.add_column(statecol)

    field_table['RA_HMS'] = ra_hms
    field_table['DEC_DMS'] = dec_dms
    field_table['RA_DEG'] = r_deg
    field_table['DEC_DEG'] = d_deg
    field_table['GAL_LONG'] = l_deg
    field_table['GAL_LAT'] = b_deg

    field_table['POL_AXIS'] = fld_pol
    field_table['SCAN_START'] = -1.0
    field_table['SCAN_LEN'] = -1.0
    field_table['SCAN_TINT'] = -1.0

    field_table['NBEAMS_I'] = -1
    field_table['MOSAIC_TIME'] = -1.0
    field_table['NPIXELS_V'] = -1
    field_table['PSF_MAJOR'] = -1.0
    field_table['PSF_MINOR'] = -1.0
    field_table['PSF_ANGLE'] = -1.0
    field_table['MINIMUM'] = -1.0
    field_table['MAXIMUM'] = -1.0

    field_table['MED_RMS_uJy'] = -1.0
    field_table['MODE_RMS_uJy'] = -1.0
    field_table['STD_RMS_uJy'] = -1.0
    field_table['MIN_RMS_uJy'] = -1.0
    field_table['MAX_RMS_uJy'] = -1.0

    field_table['SELAVY_TIME'] = -1.0
    field_table['NUM_SELAVY'] = -1

    field_table['SELECT'] = 0
    field_table['DEFECT'] = 0
    field_table['ANOMALY'] = 0
    field_table['COMMENT'] = ''
    field_table['MinUV'] = 0

    return field_table, row


def obs_to_field_table(field_table, mapping_file):
    # Split this into two parts:
    #   i) extract all data from parset, and fill spare columns with FILL (whatever is chosen)
    #  ii) For rows in the input table that need it, extract scan info from ms.
    # iii) Other columns can be supplied with data from other sources.
    #
    # open the survey_record.csv file that one gets from Aidan on a semi regular basis

    field_table_out = field_table.copy()

    r_data = ascii.read(mapping_file, format='csv')
    r_field_name = r_data['field']  # survey field name
    r_sbid = r_data['sbid']  # survey SBID
    r_cal_sbid = r_data['cal_sbid']  # survey SBID
    mapping = {}
    for f, s, c in zip(r_field_name, r_sbid, r_cal_sbid):
        k = "{}_{:d}".format(f, s)
        mapping[k] = [f, s, c]

    # Here go get scan info.
    set_sbids = sorted(list(set(r_sbid)))
    scan_info = {}
    for sb in set_sbids:
        scan_info[sb] = get_scan_info_from_ms(sb)

    # deli = []
    for km in mapping.keys():
        f, ssb, csb = mapping[km]
        wh = np.where(field_table_out['FIELD_NAME'] == f)[0]
        if len(wh) == 0:
            print('Not found in field table : ', f, ssb, csb, wh)
        else:
            got = False
            irow = -1
            # sbids = []
            vprint("field {}  {:d}".format(f, ssb))
            for wi in wh:
                r = field_table_out[wi]
                if r['SBID'] == -1:
                    irow = wi
                    got = True
                    vprint('  ', wi, '-1 using')
                elif r['SBID'] == ssb:
                    irow = wi
                    got = True
                    vprint('  ', wi, 'ssb using')

            if not got:
                # initialise a new row and append it
                row = field_table_out[wh[0]]
                row['NBEAMS_I'] = -1
                row['MOSAIC_TIME'] = -1.0
                row['NPIXELS_V'] = -1
                row['PSF_MAJOR'] = -1.0
                row['PSF_MINOR'] = -1.0
                row['PSF_ANGLE'] = -1.0
                row['MINIMUM'] = -1.0
                row['MAXIMUM'] = -1.0

                row['MED_RMS_uJy'] = -1.0
                row['MODE_RMS_uJy'] = -1.0
                row['STD_RMS_uJy'] = -1.0
                row['MIN_RMS_uJy'] = -1.0
                row['MAX_RMS_uJy'] = -1.0

                row['SELAVY_TIME'] = -1.0
                row['NUM_SELAVY'] = -1
                vprint('  adding new r["SBID"] = ', ssb)
                field_table_out.add_row(row)

            # print("{} {:d}".format(f, irow))
            field_table_out[irow]['SBID'] = ssb
            field_table_out[irow]['CAL_SBID'] = csb
            scan_data = scan_info[ssb]
            field_scan_found = False
            iscan = -1
            scan_times = []
            if scan_data:
                for k, v in scan_data.items():
                    print(k, v)
                    if f == v[3]:
                        field_scan_found = True
                        iscan = k
                        scan_times = v
                        break
            if field_scan_found:
                field_table_out[irow]['SCAN'] = iscan
                field_table_out[irow]['STATE'] = observed

                field_table_out[irow]['SCAN_START'] = scan_times[0]
                field_table_out[irow]['SCAN_LEN'] = scan_times[1]
                field_table_out[irow]['SCAN_TINT'] = scan_times[2]
            else:
                vprint("Scan information not found for {}".format(f))

    # field_table_out.remove_rows(deli)
    return field_table_out


def save_db(survey_tab, survey_file, desc_tab, desc_file, field_tab, field_file):
    survey_tab.write(str(survey_file), format='ascii.csv', delimiter=',', overwrite=True)
    desc_tab.write(str(desc_file), format='ascii.csv', delimiter=',', overwrite=True)
    field_tab.write(str(field_file), format='ascii.csv', delimiter=',', overwrite=True)


def get_desc_for_epoch(table, epoch):
    wh_epoch = np.where(table['EPOCH'] == epoch)[0]
    if len(wh_epoch) == 1:
        inx = wh_epoch[0]
        return inx, table[inx]
    else:
        return None


# -------------------------------------------------------------------------------
def main():
    # This expects an environment variable "SURVEY" that holds the full path of the particular survey's database root.
    # eg. export SURVEY=/group/askap/mcc381/ASKAP_surveys/RACS

    # At present, the user must launch the task from a directory one level below the main survey directory.
    # For example, xx/RACS/db
    # Then survey product files will be sought in x/RACS/ for example xx/RACS/calsbid/field/*.fits
    # Database files will be written into the current working directory.
    # This scheme will be generalised in future. Somehow.

    args = arg_init().parse_args()
    new_survey_name = args.survey
    survey_name = None
    epoch = args.epoch
    verbose = args.verbose
    if verbose:
        print(args)

    if 'SURVEY' not in os.environ:
        raise RuntimeError("Symbol 'SURVEY' not found in environment")

    base = Path(os.environ['SURVEY']).resolve()
    dbinputs = base.joinpath('db-inputs/epoch_{:d}'.format(epoch))
    db_root = base.joinpath('db')
    if verbose:
        print("base    = {}".format(str(base)))
        print('db_root = {}'.format(str(db_root)))

    if not db_root.exists():
        print("{} not found".format(db_root))
        print("If this is the initialisation of this db, execute the following:")
        print("mkdir {}".format(new_survey_name))
        print("export SURVEY={}".format(base.joinpath(new_survey_name)))
        print("mkdir $SURVEY/db")
        return 0

    vprint(db_root, new_survey_name)

    do_step1, do_step2 = False, False
    if args.parset:
        parset = Path(args.parset)
        do_step1 = parset.exists()
        # if not do_step1:
        #     print("Warning: {} not found".format(str(parset)))
    else:
        parset = None
    if args.mapping_file:
        mapping_file = Path(args.mapping_file)
        print("mapping file ", str(mapping_file), mapping_file.exists())
        do_step2 = mapping_file.exists()
    else:
        mapping_file = None

    survey_file = db_root.joinpath("survey.csv")
    desc_file = db_root.joinpath("description.csv")
    epoch_d = "epoch_{:d}".format(epoch)
    db_dir = db_root.joinpath(epoch_d)
    field_name = "field_data.csv"
    field_table_file = db_dir.joinpath(field_name)

    do_step3 = args.image_info is not None

    if verbose:
        print("Parset       {}".format(parset))
        print("Mapping file {}".format(mapping_file))
        print("DB directory {}".format(db_dir))

    if not (do_step1 or do_step2 or do_step3):
        print("Nothing to do {}".format([do_step1, do_step2, do_step3]))
        sys.exit()

    # Locate or create survey and description tables.
    if survey_file.exists():
        survey_table = ascii.read(survey_file, format='csv')
        if len(survey_table) == 0:
            print("Error: survey table file {} is empty.".format(survey_file))
            sys.exit()
        survey_name = survey_table['SURVEY_NAME'][0]
        if new_survey_name and (survey_name != new_survey_name):
            print("{} survey database already created so -s argument ignored".format(survey_name))
    else:
        survey_table = Table(names=survey_colnames, dtype=survey_coltypes)

    if desc_file.exists():
        desc_table = ascii.read(desc_file, format='csv')
        vprint(desc_table)
    else:
        desc_table = Table(names=desc_colnames, dtype=desc_coltypes)
        vprint(desc_table)

    if do_step1:
        # variant = args.variant
        if args.product_root is None:
            print("Error: product_root must be given. Use option -r")
            sys.exit()
        else:
            product_root = Path(args.product_root)
        product_root = product_root.resolve()

        assert db_root.exists(), ("{} not found".format(db_root))
        vprint('product_root = ', product_root)

        inx_row = get_desc_for_epoch(desc_table, epoch)
        if inx_row:
            if db_dir.exists():
                print("\n")
                print("    Database already built for this {} epoch {:d}".format(survey_name, epoch))
                print("    Delete whole database and restart if necessary.\n")
                sys.exit()
            else:
                desc_table.remove_row(inx_row[0])

        print("   Step 1  Creating database from parset ...")
        if len(survey_table) == 0:
            survey_name = new_survey_name
            survey_row = [survey_name]
            survey_table.add_row(survey_row)
        field_table, desc_row = parset_to_field_table(str(parset))
        desc_row[0] = epoch
        desc_row[desc_table.index_column('DATABASE')] = epoch_d
        desc_row[desc_table.index_column('PRODUCT_ROOT')] = str(product_root)

        desc_table.add_row(desc_row)
        print("epoch_d = ", epoch_d)
        Path.mkdir(db_dir)
        save_db(survey_table, survey_file, desc_table, desc_file, field_table, field_table_file)
        print("n nulls: ", len(field_table[field_table['STATE'] == '--NULL--']))

    if do_step2:
        print("   Step 2  Fetching observing information for {}".format(survey_name))
        field_table_0 = ascii.read(str(field_table_file), format='csv')
        # find_duplicates(field_table_0)
        # sys.exit()
        field_table = obs_to_field_table(field_table_0, args.mapping_file)
        field_table.sort(['SRC', 'SBID'])
        field_table['INDEX'] = range(len(field_table))
        save_db(survey_table, survey_file, desc_table, desc_file, field_table, field_table_file)
        print("Number of rows in 'NULL' state : ", len(field_table[field_table['STATE'] == '--NULL--']))

    if do_step3:
        vprint("   Step 3  Fetching image information for {}".format(survey_name))
        survey = ASKAP_Survey_factory(epoch=epoch, read_write=True, verbose=args.verbose)
        # print("survey.lock ", survey.lock)

        # First, select on valid state, and possibly on given CAL_SBID or SBID
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

        stats_kw = {'db_update': True, 'do_replace': False}
        match_kw = {'match_params': "", 'comparison_survey': ""}
        image_info = 'MB'
        if len(args.image_info) > 0:
            image_info = ''.join(args.image_info)
        if 'C' in image_info:
            cat_params = dbinputs.joinpath('match_params.csv')
            if args.cat_params:
                cat_params = Path(args.cat_params)
            if cat_params.exists():
                match_kw = {'match_params': str(cat_params), 'comparison_survey': ""}
            else:
                print("No file {} found. Provide it with -c or in {}".format(cat_params, dbinputs))
                # survey.release()
                return 0
        print("  with codes {}".format(image_info))
        for i in rows:
            sbid, fld = survey.get_field_data(i, ['SBID', 'FIELD_NAME'])
            print("i = {:d}  SBID = {:d}   {}".format(i, sbid, fld), end="\r", flush=True)
            if 'M' in image_info:
                asu.func_mosaic_info(survey, row_num=i)
            if 'B' in image_info:
                asu.func_beam_info(survey, row_num=i)
            if 'S' in image_info:
                if 'r' in image_info:
                    stats_kw['do_replace'] = True
                asu.func_stats_info(survey, row_num=i, **stats_kw)
            if 'A' in image_info:
                asu.func_astrom_bb_info(survey, row_num=i)
            if 'C' in image_info:
                settings_file = match_kw['match_params']
                settings = ascii.read(settings_file, format='csv')
                comparisons = list(settings['cat'])
                comparisons.remove('THIS')
                dec = survey.get_field_data(i, ['DEC_DEG'])[0]
                # ss = ['TGSS', 'SUMSS', 'NVSS', 'ICRF']
                ss = comparisons
                if dec < -51.:
                    ss.remove('TGSS')
                if dec > -30.:
                    ss.remove('SUMSS')
                if dec < -40.:
                    ss.remove('NVSS')
                for s in ss:
                    match_kw['comparison_survey'] = s
                    asu.func_cat_match_info(survey, 
                        row_num=i, 
                        check_stale=args.check_stale,
                        **match_kw)
            if 'P' in image_info:
                asu.func_leakage_info(survey, row_num=i, pols=args.pols)

        print("\nImage data is up to date")
        survey.write_field_table()
        # survey.release()


if __name__ == "__main__":
    sys.exit(main())
