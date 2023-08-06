#!/usr/bin/env python
import re

from astropy.io import ascii
from astropy.io import fits
from astropy.table import Table
import aces.survey.db_methods as meths


def data_source_factory(file_name, file_type=None):
    if file_type:
        sub_cl = file_type
    else:
        sub_cl = file_name.suffix[1:]
    for cls in DataSource.__subclasses__():
        if cls.__name__.endswith(sub_cl.upper()):
            return cls(file_name)
    print("No subclass to suit {}", format(file_type))


class DataSource(object):
    # base class for data retrieval subclasses
    def __init__(self, file_path, ref_time=None):
        self.ref_time = ref_time
        self.data = None
        self.result = None
        self.file_path_exists = False
        self.keys = None
        self.file = self.open(file_path)

    def check(self, file_path):
        # for all subclasses, check file existence and currency - but against what reference time?
        # store these quantities in object for later retrieval

        self.file_path_exists = file_path.exists()

    def open(self, file_path):
        pass

    def exists(self):
        return self.file_path_exists

    def get(self, desc, index=0):
        self.result = Table(names=desc['CNAME'], dtype=desc['CTYPE'], masked=True)
        if self.file_path_exists:
            self.keys = [a.split('@')[1] for a in desc['ARGS']]
            #             self.keys = [d%index if '%' in d else d for d in desc['ARGS']]
            self._get(desc, index)
            self.translate(desc)
        else:
            flags = [True] * len(desc)
            self.result.add_row(desc['CFILL'], flags)
        return self.result

    def translate(self, desc):
        methods = desc['METHOD']
        data, flags = [], []
        for i, (d, m, fi) in enumerate(zip(self.data, methods, desc['CFILL'])):
            flags.append(False)
            if d is None:
                data.append(fi)
                flags[-1] = True
            elif m == "nil":
                data.append(d)
            else:
                meth = getattr(meths, m, None)
                data.append(meth(d))
        self.result.add_row(data, flags)


class DataSourceFITS(DataSource):
    def __init__(self, file, ref_time=None):
        super().__init__(file, ref_time)

    def open(self, file_path):
        super().check(file_path)
        if self.file_path_exists:
            return fits.open(file_path)
        else:
            return None

    def _get(self, desc, index=0):
        self.data = []
        for i in self.keys:
            self.data.append(self.file[0].header[i])


class DataSourcePARSET(DataSource):
    def __init__(self, file, ref_time=None):
        self.lines = []
        super().__init__(file, ref_time)

    def open(self, file_path):
        super().check(file_path)
        if self.file_path_exists:
            file = open(file_path, 'r')
            self.lines = [li.strip() for li in file.readlines()]
        else:
            return None

    def _get(self, desc, index=0):
        self.data = [None] * len(desc)
        for i, item in enumerate(self.keys):
            for li in self.lines:
                if li.startswith(item):
                    self.data[i] = li.split('=')[1]


class DataSourceCSV(DataSource):
    def __init__(self, file, ref_time=None):
        super().__init__(file, ref_time)

    def open(self, file_path):
        super().check(file_path)
        if self.file_path_exists:
            file = ascii.read(file_path)
            return file
        else:
            return None

    def _get(self, desc, index=0):
        self.data = self.file[self.keys][index]


class DataSourceTABLE(DataSource):
    def __init__(self, file, ref_time=None):
        super().__init__(file, ref_time)

    def open(self, file_path):
        return file_path

    def _get(self, desc, index=0):
        self.data = self.file[self.keys][index]


class DataSourceFLAGSUMMARY(DataSource):
    # The need for this very specialised class arises from an inadequate
    # way of recording the data needed.
    def __init__(self, file, ref_time=None):
        self.lines = []
        super().__init__(file, ref_time)

    def open(self, file_path):
        super().check(file_path)
        if self.file_path_exists:
            file = open(file_path, 'r')
            self.lines = [li.strip() for li in file.readlines() if li.startswith('Flagged')]
        else:
            return None

    def _get(self, desc, index=0):
        self.data = [0, 0]
        li = self.lines[0]
        nums = re.findall('[0-9]+', li)
        self.data[0] = int(nums[0])
        self.data[1] = int(nums[1])


def func_cols(table, desc):
    """
    Adds table columns that are specified as functions of two or more other columns.
    """
    arguments = [a.split(';') for a in desc['ARGS']]

    mk = [a[0].startswith('@') for a in arguments]
    tt = desc[mk]
    for ti in tt:
        args = ti['ARGS'].split(';')
        cols = []
        for arg in args:
            cols.append(table[arg[1:]])
        fnc = getattr(meths, ti['METHOD'])
        q = fnc(*cols)
        table[ti['CNAME']] = q
