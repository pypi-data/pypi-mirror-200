#!/usr/bin/env python
"""
Defines the BeamMeasure subclass of BeamSet
Defines the BeamModel subclass of BeamSet (or BeamMeasure?)
Copyright (C) CSIRO 2017

"""


#import beamset
from aces.beamset import beamset

beamset.KnownBeamSetTypes.append("BeamMeasure")
beamset.KnownBeamSetTypes.append("BeamModel")


class BeamMeasure(beamset.BeamSet):
    # BeamMeasure is based on BeamSet.
    # - additional metadata items:

    def __init__(self, metadata=None, data=None, flags=None):

        beamset.BeamSet.__init__(self, metadata, data, flags)


class BeamModel(beamset.BeamSet):
    # BeamModel is based on BeamSet.
    # - additional metadata items:

    def __init__(self, metadata=None, data=None, flags=None):
        beamset.BeamSet.__init__(self, metadata, data, flags)
