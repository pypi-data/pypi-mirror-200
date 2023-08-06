#!/usr/bin/env python
"""
Defines the ModelSet subclass of BeamSet

Copyright (C) CSIRO 2017
"""

from aces.beamset import beamset

beamset.KnownBeamSetTypes.append("SEFDSet")


class SEFDSet(beamset.BeamSet):
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

    def get_spectrum(self, selection):
        # return the entire SEFD spectrum for the selector given; final index in selector is ignored.
        i, j, k, l, m = selection
        return self.data[i, j, k, l, 0:]
