#!/usr/bin/env python
"""
Defines the ModelSet subclass of BeamSet

Copyright (C) CSIRO 2017
"""

from aces.beamset import beamset
from aces.beamset import model as bm
import aces.beamset.surfacegaussian
import numpy as np

beamset.KnownBeamSetTypes.append("ModelSet")


def get_model_class(name):
    base = bm.Model([])
    cls_base = base.__class__
    for cls in cls_base.__subclasses__():
        if name == cls.__name__:
            return cls

    # print([a.__name__ for a in models]
    # if name in globals().keys():
    #     cls = globals()[name]
    #     return cls
    # else:
    raise NameError(name)


class ModelSet(beamset.BeamSet):
    """
     ModelSet is based on BeamSet.
     - additional metadata items:
    """
    payloadtype = 'float'

    def __init__(self, metadata=None, data=None, flags=None, filename=None):
        beamset.BeamSet.__init__(self, metadata, data, flags, filename)
        # Thefollowing now done in the baseclass.

    def print_summary(self):
        """
        Prints to standard output a summary
        """
        beamset.BeamSet.print_summary(self)
        model_name = self.metadata['model']
        num_params = self.metadata['payloadshape'][0]
        param_names = self.metadata['modelParams']
        print("")
        print("Model name: {} with {:d} parameters".format(model_name, num_params))
        for i, name in enumerate(param_names):
            print("            {:d}  {}".format(i, name))

    def get_model(self, selection):
        """Here's where we can find the required class, and call the appropriate __init__
        """

        model = self.metadata['model']
        model_cls = get_model_class(model)
        ret = model_cls(self.data[selection])
        return ret

    def get_beam_centres(self, ant, pol, chan):
        """ Retrieve the centres of all beams in a footprint(for the
        given antenna, polarization and channel.
        Also returned are the expected beam positions according to footprint.py, or
        in the case of single port beams, the position computed from PAF port positions.
        """
        beams = self.metadata['beams']
        seli = {'times': 0, 'channels': chan}
        selv = {'antennas': ant, 'polarization': pol, 'beams': beams}
        selector, sub_shape = self.get_selector_subshape(seli, selv)
        selret = self.make_gen(sub_shape)
        ret_o = np.zeros(sub_shape+[2])
        for s, sr in zip(selector, selret):
            mod = self.get_model(s)
            mod.set_ang_unit('degree')
            cent = mod.get_centre()
            ret_o[sr] = cent

        nbeams = len(beams)
        ret_e = np.zeros((nbeams, 2))
        for i in range(nbeams):
            ret_e[i] = self.get_beam_offset(i) * [-1, 1]
        return np.squeeze(ret_o), ret_e
