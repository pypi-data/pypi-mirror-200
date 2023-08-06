import os
import pkg_resources
import logging
from math import pi
from typing import Union

from askap.footprint import FootprintFactory, Footprint
from aces.askapdata.schedblock import SchedulingBlock

logger = logging.getLogger(__name__)

class ACESConfig(object):
    def __init__(self, clear_footprint_cache=False):
        """
        Read aces config parset or create it if it doesn't exist
        :return: aces config parset
        :rtype: :class:ParameterSet
        """
        # Since python 3.7 the insertion order of dicts is guaranteed to be preserved
        self.footprint_caches = {
            'askap': 'ak', 
            'askap-commissioning': 'co', 
            'effelsberg': 'ef',
            'jodrell': 'jb', 
            'legacy': 'old', 
            'sandbox': 'xx'
        }
        
        
        self.footprint_cache_root = pkg_resources.resource_filename("aces", "data/footprints")
        logger.debug(f"Loading footprint defs from {self.footprint_cache_root=}")
                
        first_cache, first_prefix = next(iter(self.footprint_caches.items()))
        self.footprint_factory = FootprintFactory(os.path.join(self.footprint_cache_root, first_cache), first_prefix)
        
        for cache, prefix in self.footprint_caches.items():
            if cache != first_cache:
                self.footprint_factory.add_parset_folder(os.path.join(self.footprint_cache_root, cache), prefix)

    
    
    
def get_footprint(sb: Union[int,SchedulingBlock]) -> Footprint:
    """Obtain the footprint layout for a given observation

    Args:
        sb (Union[int,SchedulingBlock]): Information of the schedule block that corresponds to an observation. If int, an instance of SchedularBlock is created. 

    Returns:
        Footprint: A layout of the footprint of an observation
    """
    if isinstance(sb, int):
        sb = SchedulingBlock(sb)
    
    aces_cfg = ACESConfig()
    fp_factory = aces_cfg.footprint_factory
    name = sb.get_footprint_name()
    pitch = sb.get_footprint_pitch()
    # Catch the single mset_inx footprint, which may have zero pitch, disallowed by the footprint factory.
    if pitch == 0.0:
        pitch = 1.0
    rotation = sb.get_footprint_rotation()
    fp = fp_factory.make_footprint('ak:' + name, pitch * pi / 180, rotation * pi / 180)

    return fp

def get_footprint_pa_zero(name: str, pitch: float) -> Footprint:
    """Returns  a footprint instance based on a footprint name, with 
    a user provided pitch angle. No care or facility is given to tie it
    to a particular schedule block / SBID. 

    Args:
        name (str): Name of the footprint to use
        pitch (float): Rotation of the PAF (in degrees)

    Returns:
        Footprint: Instance of PAF footprint layout
    """
    aces_cfg = ACESConfig()
    fp_factory = aces_cfg.footprint_factory
    # Catch the single beam footprint, which may have zero pitch, disallowed by the footprint factory.
    if pitch == 0.0:
        pitch = 1.0
    fp = fp_factory.make_footprint('ak:' + name, pitch * pi / 180, 0.0)
    return fp
