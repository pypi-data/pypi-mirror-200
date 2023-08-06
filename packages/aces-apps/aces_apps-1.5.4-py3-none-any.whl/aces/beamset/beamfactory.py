#!/usr/bin/env python
"""
Defines a loader of any derived BeamSet based on class ID

Copyright (C) CSIRO 2017
"""
import logging
import os

import h5py

from aces.beamset.beamset import BeamSet, KnownBeamSetTypes
from aces.beamset.mapset import MapSet
from aces.beamset.modelset import ModelSet
from aces.beamset.sefdset import SEFDSet

logger = logging.getLogger(__name__)

def load_beamset_class(filename):
    if os.path.exists(filename):
        try:
            f = h5py.File(filename, "r")
            data = f['data']
            stored_class_b = data.attrs['class']
            if isinstance(stored_class_b, bytes):
                stored_class = stored_class_b.decode("utf-8", errors="ignore")
            else:
                stored_class = stored_class_b
        except:
            logger.info(f"Available {filename} attributes: {data.attrs}")
            raise RuntimeError("Could not determine class type from file metadata")

        if stored_class not in KnownBeamSetTypes:
            raise RuntimeError("Unknown class found in file metadata: %s" % stored_class)

        if stored_class == 'BeamSet':
            my_container = BeamSet(filename=filename)
            return my_container

        if stored_class == 'MapSet':
            my_container = MapSet(filename=filename)
            return my_container

        if stored_class == 'ModelSet':
            my_container = ModelSet(filename=filename)
            return my_container

        if stored_class == 'SEFDSet':
            my_container = SEFDSet(filename=filename)
            return my_container
    else:
        raise RuntimeError("File not found %s" % filename)
