#
# @copyright (c) 2017 CSIRO
# Australia Telescope National Facility (ATNF)
# Commonwealth Scientific and Industrial Research Organisation (CSIRO)
# PO Box 76, Epping NSW 1710, Australia
# atnf-enquiries@csiro.au
#
# @author Aaron Chippendale <Aaron.Chippendale@csiro.au>
#
"""
Tools to generate signal ACMs from EM simulations for a given footprint
"""

import numpy as np


def make_acm_points(sampled_fields):
    """
    Make ACM from field sampled at desired beam pointing directions
    
    Args:
        sampled_fields (`numpy.ndarray`): port patterns sampled at desired beam pointing directions 

    Returns:
        acm (`numpy.ndarray`): ACM matrices, one for each beam pointing direction

    """
    acm = np.zeros((sampled_fields.shape[1], sampled_fields.shape[0], sampled_fields.shape[0]), dtype='complex64')

    for i_point in range(sampled_fields.shape[1]):
        acm[i_point, :, :] = np.outer(sampled_fields[:, i_point, 0], np.conj(sampled_fields[:, i_point, 0]))
        acm[i_point, :, :] += np.outer(sampled_fields[:, i_point, 1], np.conj(sampled_fields[:, i_point, 1]))

    return acm
