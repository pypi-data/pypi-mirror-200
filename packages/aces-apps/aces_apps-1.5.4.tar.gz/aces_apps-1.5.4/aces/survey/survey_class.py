#!/usr/bin/env python
import os
import numpy as np
import re
import time
import fcntl
from astropy.table import Table
# from astropy.io import ascii
from astropy.time import Time
import casacore.images as cim

from pathlib import Path
from askap.footprint import Skypos

# Make RACS-independent:
#   in class name
#   in input csv file, but with option to pass in
# Extend to completely encapsulate the .csv database.

field_name = "field_data.csv"
image_stats_name = "image_statistics.csv"


def t_string(db_time):
    time_val = Time(db_time / 3600.0 / 24.0, format='mjd', scale='utc')
    time_val.format = 'iso'
    return "{}".format(time_val)


def no_translate(a):
    return a


def make_beam_csv_name(sbid, field):
    return "beam_inf_{:d}-{}.csv".format(sbid, field)


def make_brt_err_csv_name(sbid, field):
    return "bright_err_{:d}-{}.csv".format(sbid, field)


def make_astrom_bb_csv_name(sbid, field):
    return "astrom_bb_{:d}-{}.csv".format(sbid, field)


def make_cat_match_csv_name(sbid, field, tag):
    return "cat_match_{}_{:d}-{}.csv".format(tag, sbid, field)

def make_leakage_csv_name(sbid, field, pol):
    return "stokes_{}_leakage_{:d}-{}.csv".format(
        pol, sbid, field
    )

def make_statistics_name(sbid, field):
    return "statistics_{:d}-{}.csv".format(sbid, field)


def make_fits_name(sbid, field):
    return "psf.{}.SB{:d}.{}.fits".format('{}', sbid, field)


def parse_filename(file_name):
    # assume name of the form image.i.SB8576.cont.SURV_1335-25A.linmos.taylor.0.restored.fits
    q = re.findall("\.SB[0-9]+\.", file_name)
    r = re.findall("cont\.[\S]*\.li", file_name)
    p = re.findall("\.[iquv]\.SB", file_name)

    sb = int(q[0][3:-1])
    field = r[0][5:-3]
    pol = p[0][1]

    return sb, field, pol


def access_db(t=0, wd=Path('.'), tmax=10):
    free = wd.joinpath('free')
    lock = open(free, 'w+')

    n = 0
    access = False

    while n < tmax:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            access = True
            lock.write("Lock file : {}\n".format(str(free)))
            lock.write("Wait time : {:d}\n".format(n))
            print("Lock file : {}\n".format(str(free)))
            print("Wait time : {:d}\n".format(n))
            break
        except IOError as e:
            n += 1
            print("waiting ", n)
            time.sleep(1.0)
    return lock, access, n


def release_db(wd=Path('.'), content=' '):
    free = wd.joinpath('free')
    f = open(free, 'w')
    f.write(content)
    f.close()


def ASKAP_Survey_factory(epoch=0, read_write=False, verbose=False):
    """

    :param epoch: Integer epoch number. An exception is raised if the description table lack a row for this epoch.

    """
    survey_file = 'survey.csv'
    desc_file = 'description.csv'
    if 'SURVEY' in os.environ:
        survey_base = Path(os.environ['SURVEY'])
    else:
        survey_base = Path('.')
    if verbose:
        print("Survey_base = {}".format(survey_base))

    survey_db = survey_base.resolve().joinpath('db')
    survey_db_inputs = survey_base.resolve().joinpath('db-inputs')
    survey = survey_db.joinpath(survey_file)
    if survey.exists():
        survey_table = Table.read(survey, format='ascii')
        if verbose:
            print(survey_table)
    else:
        raise IOError((0, 0, survey))

    desc = survey_db.joinpath(desc_file)
    if desc.exists():
        desc_table = Table.read(desc, format='ascii')
        if verbose:
            print(desc_table)
    else:
        raise IOError((0, 0, desc))

    if epoch in desc_table['EPOCH']:
        ie = np.where(epoch == desc_table['EPOCH'])[0][0]
    else:
        print(epoch, desc_table['EPOCH'])
        raise Exception('Epoch {:d} not found'.format(epoch))

    desc_row = desc_table[ie]

    db_dir = survey_db.joinpath(str(desc_row['DATABASE']))
    db_inputs_dir = survey_db_inputs.joinpath(str(desc_row['DATABASE']))

    product_root = survey_db.joinpath(str(desc_row['PRODUCT_ROOT']))
    field_file = db_dir.joinpath(field_name)
    # get access here ...
    print(str(field_file))
    lock = None
    if read_write:
        print("db_dir = {}".format(str(db_dir)))
        lock, success, nt = access_db(t=0, wd=db_dir, tmax=60)
        print("access : ", success, nt)
        if not success:
            raise RuntimeError("\n\nAccess timed out after {:d} seconds.\n".format(nt))

    f_table = Table.read(str(field_file), format='ascii')
    aks = ASKAP_Survey(f_table, desc_row)
    aks.lock = lock
    if verbose:
        print('Populating beam tables')
    beam_missing = []
    # bright_missing = []
    for sb, f in zip(aks.sbids, aks.field_names):
        if sb >= 0:
            key = make_beam_csv_name(sb, f)
            b_name = db_dir.joinpath(key)
            if b_name.exists():
                aks.beam_tables[key] = Table.read(str(b_name), format='ascii')
            else:
                beam_missing.append(b_name)
    # if len(beam_missing) > 0:
    #     print("{:d} beam tables not found".format(len(beam_missing)))
    # if verbose:
    #     for b in beam_missing:
    #         print(b)

    # print("{:d} bright_err tables not found".format(len(bright_missing)))
    # if verbose:
    #     for b in bright_missing:
    #         print(b)

    aks.survey_name = survey_table['SURVEY_NAME'][0]
    aks.db_dir = db_dir
    aks.db_inputs = db_inputs_dir
    aks.product_root = product_root
    aks.field_file = field_file
    aks.read_write = read_write

    file_templates = db_inputs_dir.joinpath("filenames.csv")
    aks.survey_files = SurveyFiles(aks, file_templates)
    return aks


class ASKAP_Survey(object):

    def __init__(self, field_table, description):
        """
        Initialises ASKAP_Survey instance, based on an input descriptor file in csv format.
        This file is expected in the working directory unless the environment variable $SURVEY exists.
        The descriptor file has default name survey_status.csv. This default can be
        overriden in the __init__ call.
        """
        self.starting = time.time()
        self.desc_row = description
        self.f_table = field_table
        self.epoch = self.desc_row['EPOCH']
        self.freq_ref = self.desc_row['OBS_FREQ']

        self.cal_sbids = np.array(self.f_table['CAL_SBID'])
        self.sbids = np.array(self.f_table['SBID'])
        self.field_names = np.array(self.f_table['FIELD_NAME'])

        self.sbids_cal = sorted([a for a in set(self.cal_sbids) if a > 0])
        self.calsb_sb = {}
        self.sbids_fld = {}
        for ca in self.sbids_cal:
            inx = np.where(self.cal_sbids == ca)[0]
            self.calsb_sb[ca] = sorted(list(set(self.sbids[inx])))
        for sb in set(self.sbids):
            inx = np.where(self.sbids == sb)[0]
            self.sbids_fld[sb] = sorted(self.field_names[inx])
        self.beam_tables = {}
        self.bright_err_tables = {}
        self.survey_name = ""
        self.db_dir = ""
        self.db_inputs = ""
        self.product_root = ""
        self.field_file = None
        self.file_obj = None
        self.lock = None
        self.read_write = False

    def __len__(self):
        return len(self.f_table)

    def _select(self, criteria):
        """
        Return a table selected by the criteria
        :param criteria: List of three-element criteria. Items of the list combined with AND

        eg: critera = [['COL1', '==', 21], ['COL2', '>', 1.4]]
        """
        rel_choices = ['==', '!=', '>', '<', '>=', '<=']

        maska = [True] * len(self.f_table)
        for c in criteria:
            thing, rel, val = c
            if thing not in self.f_table.colnames:
                raise Exception("No such thing {}".format(thing))
            if rel not in rel_choices:
                raise Exception("No such relation recognised {}".format(rel))
            if rel == "==":
                maskb = self.f_table[thing] == val
            elif rel == "!=":
                maskb = self.f_table[thing] != val
            elif rel == "<":
                maskb = self.f_table[thing] < val
            elif rel == "<=":
                maskb = self.f_table[thing] <= val
            elif rel == ">":
                maskb = self.f_table[thing] > val
            elif rel == ">=":
                maskb = self.f_table[thing] >= val
            if type(maskb) != bool:
                maska = [a and b for a, b in zip(maska, maskb)]
            else:
                maska = maska and maskb
        return maska

    def select_indices(self, criteria):
        """
        Return a table selected by the criteria
        :param criteria: List of three-element criteria. Items of the list combined with AND
        """
        msk = np.array(self._select(criteria))
        ind = np.where(msk == True)[0]
        return ind

    def select(self, criteria):
        """
        Return a table selected by the criteria
        :param criteria: List of three-element criteria. Items of the list combined with AND
        """
        # rel_choices = ['==', '!=', '>', '<', '>=', '<=']

        mask = self._select(criteria)
        ret = ASKAP_Survey(self.f_table[mask], self.desc_row)
        ret.db_dir = self.db_dir
        ret.product_root = self.product_root
        ret.field_file = self.field_file
        return ret

    def set_select(self):
        select = [0] * len(self.f_table['SELECT'])
        msk_state = self.f_table['STATE'] == "IMAGED"
        tab = self.f_table[msk_state]
        flds = sorted(list(set(tab['FIELD_NAME'])))

        for fld in flds:
            msk = tab['FIELD_NAME'] == fld
            msk_def = tab['DEFECT'] == 0
            msk_ano = tab['ANOMALY'] == 0
            tabf = tab[msk & msk_def & msk_ano]
            badness = tabf['MED_RMS_uJy'] * tabf['PSF_MAJOR'] * tabf['PSF_MINOR']

            if len(tabf) > 1:
                igood = np.where(badness == badness.min())[0][0]
                inx = tabf['INDEX'][igood]
                select[inx] = 1
            elif len(tabf) == 1:
                inx = int(tabf['INDEX'])
                select[inx] = 1
        self.f_table['SELECT'] = select
        self.write_field_table()

    def get_sbs_cal(self):
        return self.sbids_cal

    def get_sbs_sci(self, calsb):
        return self.calsb_sb[calsb]

    def get_sbids(self):
        return self.sbids

    def get_fields(self, sbid):
        return self.sbids_fld[sbid]

    def get_nfields(self, sbid):
        return len(self.sbids_fld[sbid])

    def find_field(self, field_name, translate=no_translate):
        """
        Return the indices of rows with FIELD_NAME match with input. Several may be returned
        if the one field were observed more than once.
        :param field_name:
        :return: list of indices.
        """
        fld = translate(field_name)
        ret = []
        for j, f in enumerate(self.field_names):
            if field_name in f:
                ret.append(j)
        return ret

    def find_position(self, ra, dec):
        c = Skypos(ra, dec)
        flds = self.field_names
        tra = np.array(self.get_column(['RA_DEG']))
        tdec = np.array(self.get_column(['DEC_DEG']))
        seps = []
        inxs = []
        for f, r, d in zip(flds, tra, tdec):
            t = Skypos(r[0] * np.pi / 180., d[0] * np.pi / 180.)
            sep = c.d_pa(t)[0]
            if sep < 5. * np.pi / 180.0:
                seps.append(sep)
                inxs.append(np.where(flds == f)[0][0])
        seps = np.array(seps)
        inx = inxs[np.where(seps.min() == seps)[0][0]]
        return inx

    def get_column(self, col):
        ret = np.array(self.f_table[col])
        return ret

    def get_row(self, inx):
        mk = self.f_table['INDEX'] == inx
        ta = self.f_table[mk]
        return ta[0]

    def get_field_data(self, inx, cols):
        ret = []
        for col in cols:
            ret.append(self.f_table[col][inx])
        return ret

    def put_field_data(self, inx, cols, data):
        """
        Over-write values in the field data table
        :param inx: row number of table
        :param cols: Names of columns to receive new values
        :param data: List of values. Length must match length of cols list.
        """
        for c, d in zip(cols, data):
            self.f_table[c][inx] = d

    def get_field_table(self):
        """
        Return the field table as an astropy Table
        :return: (Table) field_table
        """
        return self.f_table

    def get_sub_table(self, fld, sbid, which, **kw):
        """

        :param fld:
        :param sbid:
        :param which: Select which table from 'beam', 'cat', 'ast_bb', 'statistics'
        :returns astropy Table
        """
        db = self.db_dir

        if which == 'beam':
            b_name = make_beam_csv_name(sbid, fld)
        elif which == 'cat':
            tag = kw['C_SURVEY']
            b_name = make_cat_match_csv_name(sbid, fld, tag)
        elif which == 'ast_bb':
            b_name = make_astrom_bb_csv_name(sbid, fld)
        elif which == 'statistics':
            print("sbid = {:d}, fld = {}".format(sbid, fld))
            b_name = make_statistics_name(sbid, fld)

        b_path = db.joinpath(b_name)
        sub_table = None
        # print('b_path = ', str(b_path))
        if b_path.exists():
            sub_table = Table.read(str(b_path), format='csv')
        else:
            pass
            # print(kw, tag)
            # print("No table found {}".format(b_path))
        return sub_table

    def get_sub_fitsdata(self, fld, sbid, which):
        """

        :param fld:
        :param sbid:
        :param which: Select which file from 'bpa', 'bmi', 'bpa'
        :returns ndarray image
        """
        db = self.db_dir
        b_name = make_fits_name(sbid, fld).format(which)

        b_path = db.joinpath(b_name)
        data = None
        if b_path.exists():
            im = cim.image(str(b_path))
            data = np.squeeze(im.getdata())
            data = np.ma.masked_invalid(data)

        else:
            print("No table found {}".format(b_path))
        return data

    def get_inx_from_fld_sbid(self, fld, sbid):
        inxs = self.find_field(fld)
        i = np.where(self.f_table['SBID'][inxs] == sbid)
        inx = inxs[i[0][0]]
        return inx

    def get_row_from_prod_name(self, pname):
        # assume name of the form image.i.SB8576.cont.SURV_1335-25A.linmos.taylor.0.restored.fits
        sb, field, pol = parse_filename(pname)

        inxs = self.find_field(field)
        for i in inxs:
            if self.f_table['SBID'][i] == sb:
                ret = i
        return ret

    def sort_field_data(self, cols):
        """

        :param cols: List of column names
        """
        self.f_table.sort(cols)

    def get_data_root(self):
        return self.product_root

    def get_freq_ref(self):
        return self.freq_ref

    # def get_data_variant(self):
    #     if 'VARIANT' in self.desc_row.colnames:
    #         var = int(self.desc_row['VARIANT'])
    #     else:
    #         var = 0
    #     return var

    def show_one(self, inx):
        row = self.f_table[inx]
        for c, a in zip(row.colnames, row):
            print("{:23s} {}".format(c, a))

    def write_field_table(self):
        if self.read_write:
            self.f_table.write(str(self.field_file), format='ascii', delimiter=',', overwrite=True)
        else:
            print("No write permitted - opened READ_ONLY")

    def release(self):

        wd = self.db_dir
        release_db(wd = wd, content="dt = {:f}".format(time.time() - self.starting))
        self.read_write = False


class SurveyFiles(object):
    def __init__(self, survey, file_templates):
        print("file_templates : {}".format(file_templates))
        tab = Table.read(file_templates, format='ascii')
        print(tab.colnames)
        ftypes = tab['file_types']
        name_templates = tab['name_templates']
        self.survey = survey
        self.lookup = dict(zip(ftypes, name_templates))
        self.root = self.survey.get_data_root()

    def file_name(self, ftype, inx, taylor=0, stokes='i', beam=0):
        tmpl = self.lookup[ftype]
        db_row = self.survey.get_row(inx)
        cal_sbid, sbid, fld = db_row['CAL_SBID', 'SBID', 'FIELD_NAME']
        name = tmpl.format(cal_sbid, sbid, fld, taylor, stokes, beam)
        return self.root.joinpath(name)

    def cal_table_name(self, ftype, cal_sbid):
        """Name of bandpass calibration tables.

        :param ftype: str, bp_table or bp_leakage_table.
        :param cal_sbid: int, SB ID of calibrator scan.
        :return: PosixPath to calibration table of choice.
        """

        tmpl = self.lookup[ftype]
        name = tmpl.format(cal_sbid)
        return self.root.joinpath(name)
