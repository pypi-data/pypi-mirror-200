#!/usr/bin/env python
"""
Defines classes for holding beam maps and models for ASKAP

Copyright (C) CSIRO 2017
"""
import numpy as np
from aces.obsplan.config import ACESConfig


class BeamBase(object):
    """
    A base class for holding and providing information about beams.
    The subclasses in mind are BeamFormed and BeamSingleports. 
       
    :param int num_beams: number of beams
    :param offsets_rect: rectangular offsets in l,m about antenna boresight
    :type offsets_rect: :class:`numpy.ndarray` of dimension (num_beams, 2)
    """
    def __init__(self, num_beams=0, offsets_rect=None):
        # check valid inputs

        self.numBeams = num_beams
        if offsets_rect is None:
            self.offsetsRect = np.zeros([0, 2])
        else:
            self.offsetsRect = offsets_rect

        if self.numBeams != self.offsetsRect.shape[0]:
            raise(ValueError, 'offsets_rect.shape[0] is {} but should equal num_beams which is {}'.format(
                self.offsetsRect.shape[0], self.numBeams))

    def get_num_beams(self):
        return self.numBeams

    def get_beam_offset(self, beam):
        if beam >= self.numBeams:
            raise RuntimeError("Illegal beam number requested {:d}".format(beam))
        else:
            return self.offsetsRect[beam]


def get_port_positions():
        ports_per_pol = 94
        irowa = range(6, 2, -1)
        irowb = range(8, 0, -1)
        irowc = range(9, -1, -1)
        rowa = np.array(irowa) - 4.5
        rowb = np.array(irowb) - 4.5
        rowc = np.array(irowc) - 4.5
        na, nb, nc = 4, 8, 10
        p1x = na*[10] + nb*[9] + nc*[8] + nc*[7] + nc*[6] + nc*[5] + nc*[4] + nc*[3] + nc*[2] + nb*[1] + na*[0]
        xgrid_x = np.concatenate((rowa, rowb,
                                 rowc, rowc, rowc, rowc, rowc, rowc, rowc,
                                 rowb, rowa))
        xgrid_y = np.array(p1x) - 5.0

        ygrid_x = -xgrid_y
        ygrid_y = xgrid_x

        num_beams_total = ports_per_pol * 2
        xy0 = np.zeros([num_beams_total, 2])
        xy0[:ports_per_pol, 0] = -xgrid_x
        xy0[:ports_per_pol, 1] = +xgrid_y
        xy0[ports_per_pol:, 0] = -ygrid_x
        xy0[ports_per_pol:, 1] = +ygrid_y
        ang = -3.0 * np.pi/4
        c45, s45 = np.cos(ang), np.sin(ang)
        posOnPAF = np.zeros([num_beams_total, 2])
        posOnPAF[:, 0] = c45 * xy0[:, 0] - s45 * xy0[:, 1]
        posOnPAF[:, 1] = s45 * xy0[:, 0] + c45 * xy0[:, 1]
        return posOnPAF


class BeamFormed(BeamBase):
    """ 
    Provides beam information, given the footprint specification
    """
    def __init__(self, fp_name, fp_pitch, fp_angle=0.0, beamforming_pa=0.0):
        """
        Initialise footprint and beamforming info in BeamFormed object
        :param str fp_name: footprint name 
        :param float fp_pitch: footprint pitch in radians
        :param float fp_angle: footprint rotation angle in radians
        :param float beamforming_pa: roll angle during beamforming in radians
        """

        aces_cfg = ACESConfig()
        fp_factory = aces_cfg.footprint_factory
        valid_names = fp_factory.get_footprint_names()
        if fp_name in valid_names:
            # Put the footprint into the antennas frame by adding (or subtracting?) the PA at beamforming time.
            angle = fp_angle - beamforming_pa
            self.fp = fp_factory.make_footprint(fp_name, fp_pitch, angle)

            BeamBase.__init__(self, self.fp.n_beams, self.fp.offsetsRect)
        elif fp_name == 'none':
            pass
        else:
            raise ValueError("Invalid footprint name {}".format(fp_name))


class BeamSinglePorts(BeamBase):
    """
    Provides beam information for single port beams
    Mounting and geometry errors can be incorporated.
    """
    def __init__(self, port_numbers):
        """
        Geometry according to the JER green paper
        Naming: lower-case x,y denotes which set of ports. Upper case X,Y denotes X,Y position on PAF
        Changed 2017-Feb-02 to match view from rear, and orientation used in port gain quiver plots.
        """
        pitch = 90.0
        fl = 6000.0
        plate_scale = 0.86/fl
        pos_on_PAF = get_port_positions()
        offsets_rect_all = pos_on_PAF * plate_scale*pitch
        num_ports_total = offsets_rect_all.shape[0]
        num_beams = len(port_numbers)
        offsets_rect = np.array([offsets_rect_all[i-1] for i in range(1, num_ports_total+1) if i in port_numbers])
        BeamBase.__init__(self, num_beams, offsets_rect)
