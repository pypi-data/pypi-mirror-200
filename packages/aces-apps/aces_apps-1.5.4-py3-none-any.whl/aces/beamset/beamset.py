#!/usr/bin/env python
"""
Defines classes for holding beam maps and models for ASKAP
Copyright (C) CSIRO 2017

"""
import copy
import datetime
import logging
import os
import time

import h5py
import numpy as np

from aces.beamset import beambase

logger = logging.getLogger(__name__)

"""
The current initialising of this class and its subclasses is awkward
because of giving the option to  open an empty object and populate is in
subsquent steps, perhaps several times. There seems to be no good case for
providing this flexibility.

Requirements:
1. to be able to create an object directly from stored data in an hdf5 file;
2. to be able to start from nothing, and populate data and flags progressively
   through the process.

So propose the following:
- allow only two kinds of init with __init__(self,filename=None,metadata=None,data=None,flags=None)
- __init__ insists on valid values for either filename or metadata, but not both.
- valid values for data and flags is optional.

"""

"""
2017Oct18
Because of long frequencies axis in sefd data (>8000), the old metadata['frquencies'] must be
supplemented with a possible metadata['freq_range'] that holds start, stop, nf.
As a consequence, it is convenient to have an object variable self.axes that is loaded from metadata
and holds the values along each axis of the container.
TODO: improve the abstraction, making this availavle only through a method call.

"""
#: List of everything that inherits the base class
KnownBeamSetTypes = ['BeamSet']

MJD0 = datetime.datetime(1858, 11, 17)


def mjd_to_dt(mjd):
    """
    Convert modified julian date to python datetime object
    
    :param float mjd: modified julian date
    :return: :class:`datetime.datetime` object rendered as a string
    :rtype: str
    
    """
    if mjd == 0.0 or mjd is None:
        return "** Date not recorded **"
    else:
        delta = datetime.timedelta(days=mjd)
        dt = MJD0 + delta
        return dt.__str__()


def list_items(items):
    ret = "unrecognised type {}".format(type(items[0]))
    if isinstance(items[0], int) or isinstance(items[0], np.int64):
        ret = ','.join(["{:d}".format(a) for a in items])
    elif isinstance(items[0], float):
        ret = ','.join(["{:.1f}".format(a) for a in items])
    elif isinstance(items[0], str):
        ret = ','.join(["{}".format(a) for a in items])
    return ret


class BeamSet:
    """
    This is the base class for subclasses that hold sets of beams in various
    formats - measurements and models.
    
    Classes of BeamSet share the basic structure for holding data and flags that are organised
    by antenna, beam, polarization, frequency channel, and time. The container for data and
    flags has these five dimensions. Subclasses may add extra dimensions, depending on the
    shape of their data "payloads". For example, a Map subclass would have a payload with
    shape (Nx,Ny) for an Nx by Ny grid.
    
    The data and flag structures are :class:`numpy.ndarray` objects (and
    their `h5py` equivalents), defined so that:
    containerShape = (Nt, Na, Nb, Np, Nf) where
    
    - t: time
    - a: antenna
    - b: beam
    - p: polarization
    - f: frequency.

    Iteration. The class provides facilties for iterating over subspaces of the 5-dimensional
    data volume. See comments for methods get_selector and get_selector_subshape.
    
    """
    # default payload type, can be overridden by defining this variable in local classes
    payloadtype = 'complex'

    metadataDefaults = {'class': 'BeamSet',
                        'times': [],
                        'antennas': [],
                        'beams': [],
                        'frequencies': [],
                        'polarizations': [],
                        'payloadshape': (1,),
                        'fp_name': 'None', 'fp_pitch': 0.0, 'fp_angle': 0.0,
                        'beamformingSBID': -1,
                        'beamformingPA': 0.0,
                        'beamformingEpoch': 0.0,
                        'holographySBID': -1,
                        'holographyEpoch': 0.0,
                        'beamType': 'formed',
                        'history': [time.asctime()+": First Created"]}

    lookup = {}
    select_all = {}
    axis_names = ['times', 'antennas', 'beams', 'polarizations', 'frequencies']
    for i, k in enumerate(axis_names):
        lookup[k] = i
        select_all[k] = 'all'
    lookup['channels'] = 4

    def __init__(self, metadata=None, data=None, flags=None, filename=None):
        """
        Initialise BeamSet object
        
        :param dict metadata: carries necessary ancillary quantities as defined below
        :param data: antenna/beam data payload
        :type data: :class:`numpy.ndarray`
        :param flags:
        :type flags: :class:`numpy.ndarray`
        :param filename: if present, read object data from it
        :type filename: str

        metadata carries necessary ancillary quantities as a python dictionary
        metadata['class'] - name of BeamSet sub-class
        metadata['times']         - list of times (float MJD)
        metadata['antennas']      - list of antennas, by number in the range [1-36] inclusive.
        metadata['beams']         - list of beam numbers
        metadata['polarizations'] - list of polarizations eg. ['xx','xy','yx','yy']
        metadata['frequencies']   - list of frequencies (in MHz)  OR the line below
        metadata['freq_range']    - list giving frequencies as [start, stop, nf].
        metadata['payloadshape']  - tuple giving the shape of the payload
        metadata['fp_name']       - Footprint(name
        metadata['fp_pitch']      - Footprint(pitch
        metadata['fp_angle']      - Footprint(position angle
        metadata['beamformingPA'] - antenna position angle used for beamforming
        metadata['beamformingEpoch'] - as float MJD
        metadata['holographyEpoch']   - as float MJD
        metadata['beamType']       - type of beam in ['formed','singleport']
        metadata['history']        - can be added to using BeamSet.add_to_history
        ***** "list" items should be np.array *********
        plus subclass-specific quantities
        
        """

        self.filename = None
        if filename is None and metadata is None:
            raise ValueError("Invalid input - must provide filename or metadata")
        if filename:
            self.read_from_hdf5(filename)
        else:
            self.metadata = copy.deepcopy(BeamSet.metadataDefaults)
            self.metadata.update(metadata)

        self._init()
        # if self.data exists, skip this
        # else copy inputs, or if none, create blank container and flags.
        if not hasattr(self, 'data'):
            # if data.all() is not None:
            if data is not None:
                self.data = data
                self.flags = flags
            else:
                self._create_blank_container()

    def _init(self):
        """
        Private method to be called by __init__ after metadata dictionary is established.
        Subclass invocation of __init__ will be after this.
        """
        # Set class name in metadata - this will pick up the subclass of calling object (self).
        # Do it here to overwrite any conflicting class name
        self.metadata['class'] = self.__class__.__name__
        # self.filename = None

        # Always recompute data structure shape values
        self.Nt = len(self.metadata['times'])
        self.Na = len(self.metadata['antennas'])
        self.Nb = len(self.metadata['beams'])
        self.Np = len(self.metadata['polarizations'])
        # self.Nf = len(self.metadata['frequencies'])
        self.Nf = self._get_frequencies()

        # For the container axes, define an internal structure to hold ais values
        self.axes = {'times': self.metadata['times'],
                     'antennas': self.metadata['antennas'],
                     'beams': self.metadata['beams'],
                     'polarizations': self.metadata['polarizations'],
                     'frequencies': self.frequencies}

        self.channels = range(self.Nf)
        self.containerShape = [self.Nt, self.Na, self.Nb, self.Np, self.Nf]
        self.payloadShape = self.metadata['payloadshape']
        try:
            self.payloadType = getattr(np, self.__class__.payloadtype)
        except:
            self.payloadType = self.__class__.payloadtype
            logger.debug(f"Beamset payload type: {self.payloadType}, {type(self.payloadType)}")
        
        # Ensure lists are held in numpy arrays.
        # Ugly code: if other str lists are introduced it will break.
        for k, v in self.metadata.items():
            if isinstance(v, list) and k != 'history':
                self.metadata[k] = np.array(v)

        # Update internal angular quantities:
        self.fpPitch = np.radians(self.metadata['fp_pitch'])
        self.fpAngle = np.radians(self.metadata['fp_angle'])
        self.beamformingPA = np.radians(self.metadata['beamformingPA'])

        if self.metadata['beamType'] == 'formed':
            fp_name = self.metadata['fp_name'].lower()
            if ':' not in fp_name:
                fp_name = 'ak:'+fp_name
            # noinspection PyTypeChecker
            # print('beamset:_init fp_name {}'.format(fp_name))
            self.beams = beambase.BeamFormed(fp_name, self.fpPitch, self.fpAngle, self.beamformingPA)
        elif self.metadata['beamType'] == 'singleport':
            self.beams = beambase.BeamSinglePorts(self.metadata['beams'])

    def _get_frequencies(self):
        if 'freq_range' in self.metadata:
            start, stop, nf = self.metadata['freq_range']
            # print(start, stop, nf)
            self.frequencies = np.linspace(start, stop, int(nf))
            # self.metadata['frequencies'] = self.frequencies
        else:
            self.frequencies = self.metadata['frequencies']
        return len(self.frequencies)

    def get_metadata(self, override=None):
        """
        Returns a copy of the metadata. If the optional filter is set
        to a dictionary with keys and values for 'times','antennas','beams',
        'polarizations' and/or 'frequencies', the returned dictionary will pass
        only values that exist in self.metadata.
        """
        if override:
            filt = self.filter(override)
        else:
            filt = {}
        ret = copy.deepcopy(self.metadata)
        for k in ret:
            if k in filt:
                ret[k] = filt[k]
        return ret

    def show_my_class(self):
        print(self.metadata['class'])

    def get_container_shape(self):
        """ Return the shape of the "Container", i.e. the first 5 dimensions of the data array
        """
        return self.containerShape

    def get_vector(self, selection):
        """
        Given a selection, return a list holding the corresponding positions along each
        container dimension.
        See comments for get_selector.
        """
        vec = [None]*5
        lu = BeamSet.lookup
        for ax, j in lu.items():
            if ax in self.axes.keys():
                vec[j] = self.axes[ax][selection[j]]
        return vec

    def get_selector_subshape(self, indices=select_all, values=None):
        """
        Returns (yields) a generator and the shape of the indexed subspace.
        
        The generator iterates through the selection
        specified in the arguments. For example:
        
        .. code-block:: python
        
          seli = {'times':0, 'channels':[55,65]}
          selv = {'ant':5,'beams':[14],'pol':['XX','YY']}
          sel,sub_sh = obj.get_selector_subshape(seli,selv)
          for s in sel:
            beamMap = obj.getMap(s,['power'])
            time,ant,beam,pol,freq = obj.getVector(s)


        Selections made in values override those made in indices.
        The selection for any axis without mention in either argument is [0].
        
        :param indices: A dictionary holding axis indices
        :param values: A dictionary holding axis values; corresponding indices are computed from metadata
        """
        ind = self.get_selection(indices, values)

        sub_shape = [len(i) for i in ind]
        self._check_generator_request(ind)
        gen = self._get_generator(ind)
        return gen, sub_shape

    def get_selector(self, indices=select_all, values=None):
        """
        Returns (yields) a generator that can iterate through the selection
        specified in the arguments. For example:
        
        .. code-block:: python
        
          seli = {'times':0, 'channels':[55,65]}
          selv = {'ant':5,'beams':[14],'pol':['XX','YY']}
          sel = obj.get_selector(seli,selv)
          
          for s in sel:
            beamMap = obj.getMap(s,['power'])
            time,ant,beam,pol,freq = obj.getVector(s)

        
        Selections made in values override those made in indices.
        
        The selection for any axis without mention in either argument is [0].
        :param indices: A dictionary holding axis indices
        :param values: A dictionary holding axis values; corresponding indices
        are computed from metadata
        """
        return self.get_selector_subshape(indices, values)[0]

    def get_selection(self, indices=select_all, values=None):
        """
        Returns a selection (slice) into the object data,
        specified in the arguments. For example:
        seli = {'times':0, 'channels':[55,65]}
        selv = {'ant':5,'beams':[14],'pol':['XX','YY']}
        selection = obj.get_selection(seli,selv)

        Selections made in values override those made in indices.
        The selection for any axis without mention in either argument is [0].
        
        :param indices: A dictionary holding axis indices, OR a list of indices for each axis (parameter values
                        will be ignored)
        :param values: A dictionary holding axis values; corresponding indices are computed from metadata
        
        """

        if type(indices) is list:
            ind = indices
        else:
            if indices is None:
                indices = {}
            if values is None:
                values = {}

            md = self.metadata
            lu = BeamSet.lookup
            ind = [[0]]*5
            for k, v in indices.items():
                for dim, j in lu.items():
                    if k in dim:
                        if type(v) == str and v == 'all':
                            vl = range(len(md[dim]))
                        elif type(v) != list and type(v) != tuple and type(v) != range:
                            vl = [v]
                        else:
                            vl = v
                        ind[j] = vl
            for k, v in values.items():
                for dim, j in lu.items():
                    if k in dim:
                        if type(v) != list and type(v) != np.ndarray:
                            vl = [v]
                        else:
                            vl = v
                        si = []
                        for vi in vl:
                            vwh = np.where(md[dim] == vi)
                            if vwh[0].shape[0] > 0:
                                si.append(vwh[0][0])
                            else:
                                raise ValueError("Invalid selection %s : %s" % (k, v))
                        ind[j] = si
        return ind

    @staticmethod
    def _get_generator(ind):
        for i in ind[0]:
            for j in ind[1]:
                for k in ind[2]:
                    for l in ind[3]:
                        for m in ind[4]:
                            yield np.s_[i, j, k, l, m]

    @staticmethod
    def make_gen(array_shape):
        """
        Given a the shape of a 5D array, yield a generator that
        iterates over the array.
        """
        ind = [range(a) for a in array_shape]
        for i in ind[0]:
            for j in ind[1]:
                for k in ind[2]:
                    for l in ind[3]:
                        for m in ind[4]:
                            yield np.s_[i, j, k, l, m]

    def filter(self, request):
        """
        Given a requested set of selections in a trial metadata dict,
        pass through to the returned dict only items that exist in self.
        """
        ret = {}
        for k, v in request.items():
            if k in BeamSet.lookup:
                if k == 'channels':
                    mdk = self.channels
                else:
                    mdk = self.metadata[k]
                vret = np.array([vi for vi in v if vi in mdk])
                if k == 'polarizations':
                    if 'I' in v:
                        if 'I' in mdk or ('XX' in mdk and 'YY' in mdk):
                            vret = np.concatenate((vret, ['I']))
            else:
                vret = v
            ret[k] = vret
        # Now add an item for frequencies if 'channels' is in the request
        if 'channels' in ret:
            ret['frequencies'] = self.metadata['frequencies'].take(ret['channels'])
        return ret

    def _create_blank_container(self):
        """
        Creates this instance's data and flag containers, data with payload of
        the given dimensions.
        """
        shape = self.containerShape + list(self.payloadShape)
        self.data = np.zeros(shape, self.payloadType)
        self.flags = np.zeros(self.containerShape, np.bool_)
        # print("** Container set to zero **"

    def _check_generator_request(self, ind):
        for i, j in zip(self.containerShape, ind):
            if isinstance(j[0], range):
                maxj = j[0].stop - 1
            else:
                maxj = max(j)
            if maxj >= i:
                print(maxj, i)
                raise ValueError("Request goes outside container bounds {}".format(self.containerShape))

    def get_beam_offset(self, beam):
        """
        Return beam offset in degrees
        """
        offset = self.beams.get_beam_offset(beam)
        return np.degrees(offset)

    def get_beam_offsets(self):
        """
        Return ndarray of beam offsets, in degrees
        """
        ret = np.array([])
        # for beam in self.metadata['beams']:
        for beam in range(self.Nb):
                ret = np.append(ret, self.get_beam_offset(beam))
        ret = np.reshape(ret, [self.Nb, 2])
        return ret

    def get_subset(self, selection):
        """
        Return a new object of the same class including data specified by selection
        :param selection: a slice into the object data
        :return: a new object of the same class
        """
        new_md = self.get_metadata()
        new_seli = {}
        for si, na in zip(selection, BeamSet.axis_names):
            new_md[na] = [self.metadata[na][i] for i in si]
            new_seli[na] = 'all'
        new_obj = self.__class__(new_md)
        out_sel = new_obj.get_selector(indices=new_seli)
        in_sel = self.get_selector(selection)
        for si, so in zip(in_sel, out_sel):
            new_obj.data[so] = self.data[si]
            new_obj.flags[so] = self.flags[si]

        new_obj.add_to_history("Subset created.")
        return new_obj

    def operation(self, axis, op_func, result_label):
        """
        Operate on payloads along the given axis using op_func.
        :param axis: The chosen axis in range 0-4
        :param op_func: A function expecting a stack of payloads, returning the result as a payload-shaped object.
        The function's doc-string is used in the new object's history
        :param result_label: used to label the single item remaining on the given axis.
        :returns an object of same class as self.

        """
        dim = BeamSet.axis_names[axis]
        ss0 = self.get_selection()
        ss1 = [i for i in ss0]
        ss1[axis] = [0]

        ret_obj = self.get_subset(ss1)
        ret_obj.metadata[dim] = np.array(result_label)
        sel = self.get_selector(ss1)
        osel = ret_obj.get_selector()
        for s, so in zip(sel, osel):
            si = list(s)
            inputs = []
            for i in ss0[axis]:
                si[axis] = i
                inputs.append(self.data[tuple(si)])
            inputs = np.array(inputs)
            ret_obj.data[so] = op_func(inputs)
        ret_obj.add_to_history("{} over {} axis ({:d}) ...".format(op_func.func_doc, dim, axis))
        ret_obj.add_to_history("{} combined: {}".format(dim, self.metadata[dim]))
        return ret_obj

    def add_to_history(self, item, timestamp='now'):
        """
        Add string item to history list, with timestamp
        """
        if timestamp == 'now':
            ts = time.asctime()
        else:
            ts = timestamp
        # noinspection PyTypeChecker
        self.metadata['history'].append(ts + ' : ' + item)

    def print_summary(self):
        """
        print(summary of quantities defined in this base class.
        Consider overloading this method in subclasses, calling BeamSet.print_summary(self)
        and adding subclass-specific quantities.
        """
        md = self.metadata
        antennas = list_items(md['antennas'])
        beams = list_items(md['beams'])
        pols = list_items(md['polarizations'])
        fs = self.frequencies
        if len(fs) < 5:
            s_freq = list_items(fs) + ' MHz'
        else:
            f1, f2, df = fs[0], fs[-1], fs[1]-fs[0]
            s_freq = '{:.1f} to {:.1f} step {:.3f} MHz'.format(f1, f2, df)
        nbeams = self.Nt * self.Na * self.Nb * self.Np * self.Nf
        nf = np.count_nonzero(self.flags)
        if self.filename:
            print("    Summarising {}\n".format(self.filename))
        else:
            print("    Summarising {}\n".format(self.__class__.__name__))

        print("File class                {:s}".format(md['class']))
        print("File contains data for    {:d} epoch".format(self.Nt))
        print("Antennas                  {}".format(antennas))
        if md['beamType'] == "formed":
            print("Footprint(               '{}'  pitch = {:.2f} deg   PA = {:.2f} deg".format(md['fp_name'],
                                                                                               md['fp_pitch'],
                                                                                               md['fp_angle']))
            print("File contains beams       {}".format(beams))
            print("Polarizations             {}".format(pols))
            print("SBID (beamforming)        {:d}".format(md['beamformingSBID']))
            print("Beams formed on           {} UTC".format(mjd_to_dt(md['beamformingEpoch'])))
            print("at antenna position angle {:.1f} deg".format(md['beamformingPA']))
        elif md['beamType'] == 'singleport':
            print("Single port beams")
            print("File contains ports       {}".format(beams))
        print('channel frequencies       {}'.format(s_freq))
        print('Number of channels        {:d}'.format(self.Nf))
        print("SBID (holography)         {:d}".format(md['holographySBID']))
        print("Holography measurements   {} UTC".format(mjd_to_dt(md['holographyEpoch'])))
        print("History : ")
        for h in md['history']:
            print("    {:s}".format(str(h)))
        print("In total {:d} payloads; {:d} flagged ({:.2f}%)".format(nbeams, nf, nf*100.0/nbeams))

    def write_to_hdf5(self, filename):
        # todo: handle None as value (in write and read)
        if os.path.exists(filename):
            os.remove(filename)

        f = h5py.File(filename, "w")
        data = f.create_dataset('data', data=self.data)
        f.create_dataset('flags', data=self.flags)
        self.add_to_history("Written to disk as %s" % filename)
        temp = self.metadata
        for k, v in temp.items():
            if isinstance(v, np.ndarray):
                if len(v) > 0:
                    if isinstance(v[0], np.str_):
                        v = np.array([a.encode() for a in v])
            elif isinstance(v, str):
                v = v.encode()
            temp[k] = v

        data.attrs.update(temp)
        f.close()

    def read_from_hdf5(self, filename):
        f = h5py.File(filename, "r")
        self.filename = filename
        self.data = np.array(f['data'])
        # self.data = f['data']
        self.flags = f['flags']
        metadata = {}
        for a in f['data'].attrs.keys():
            v = f['data'].attrs[a]

            if isinstance(v, np.ndarray):
                if len(v) > 0:
                    if isinstance(v[0], np.bytes_):
                        v = np.array([a.decode() for a in v])
            elif isinstance(v, bytes):
                v = v.decode()

            metadata[a] = v
        temp = metadata['history'].tolist()
        metadata['history'] = temp

        # Catch files formed before the need for various new
        # metadata items:
        # new_items = {
        #             'payloadshape': self.data.shape[5:],
        #             }
        new_items = {}
        metadata.update(new_items)

        self.metadata = metadata
        self.add_to_history("Read from disk as %s" % filename)
