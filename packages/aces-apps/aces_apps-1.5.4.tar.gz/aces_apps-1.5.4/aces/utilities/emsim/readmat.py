#
# @copyright (c) 2017 CSIRO
# Australia Telescope National Facility (ATNF)
# Commonwealth Scientific and Industrial Research Organisation (CSIRO)
# PO Box 76, Epping NSW 1710, Australia
# atnf-enquiries@csiro.au
#
# @author Aaron Chippendale <Aaron.Chippendale@csiro.au>
#
from __future__ import print_function

"""Script to read simulated ASKAP PAF port patterns from .mat files"""

import numpy as np
import h5py
from scipy import io
from scipy.interpolate import griddata
# import scipy.interpolate as spint
import scipy.spatial.qhull as qhull
# import itertools

N_REGIONS = 54
POINTS_PER_REGION = 961
N_PORTS = 188

# this list gives the indices to the simulated port labels in the ASKAP PAF port order
portmapx = list(range(94, 90, -1)) + list(range(86, 78, -1)) + list(range(78, 68, -1)) + list(range(68, 58, -1)) + list(range(58, 48, -1)) \
           + list(range(48, 38, -1)) + list(range(38, 28, -1)) + list(range(28, 18, -1)) + list(range(18, 8, -1)) + list(range(8, 0, -1)) \
           + list(range(90, 86, -1))
portmapy = list(range(184, 180, -1)) + list(range(102, 94, -1)) + list(range(112, 102, -1)) + list(range(122, 112, -1)) + list(range(132, 122, -1)) \
           + list(range(142, 132, -1)) + list(range(152, 142, -1)) + list(range(162, 152, -1)) + list(range(172, 162, -1)) \
           + list(range(180, 172, -1)) + list(range(188, 184, -1))
portmap = portmapx + portmapy
portmap = [x-1 for x in portmap]


def grid_from_file(regions_fname, n_regions=N_REGIONS):
    """
    Load cartesian grid and differential solid angle from .mat files made by Stuart's simulations of ASKAP patterns
    
    Args:
        regions_fname (str): 
        n_regions (int): 

    Returns:
        xyz (`numpy.ndarray`): with (x,y,z) cartesian coordinates defining unit vector describing angle 
            one row per coordinate with each coordinate in a separate column, real valued.
        domega (`numpy.ndarray`): vector of differential solid angle for each pattern point, real valued.
    """
    regions_fo = io.loadmat(regions_fname)

    points_per_region = regions_fo['x1'].shape[0]

    xyz = np.zeros((n_regions * points_per_region, 3))
    domega = np.zeros((n_regions * points_per_region,))
    for i_region in range(n_regions):
        region_label = i_region + 1
        xyz[i_region * points_per_region:(i_region + 1) * points_per_region, 0] = regions_fo[
            'x{}'.format(region_label)].squeeze()
        xyz[i_region * points_per_region:(i_region + 1) * points_per_region, 1] = regions_fo[
            'y{}'.format(region_label)].squeeze()
        xyz[i_region * points_per_region:(i_region + 1) * points_per_region, 2] = regions_fo[
            'z{}'.format(region_label)].squeeze()
        domega[i_region * points_per_region:(i_region + 1) * points_per_region] = regions_fo[
            'domega{}'.format(region_label)].squeeze()

    return xyz, domega

# def get_points_per_region(field_fname):
#     """
#     Load a single far-field electric field file and report number of points per region
#
#     Args:
#         field_fname:
#
#     Returns:
#         n_regions (int): number of points in this pattern
#
#     """
#     with h5py.File(field_fname + '0.mat', 'r') as pattern_fo:
#         n_regions =


def field_from_file(field_fname, n_regions=N_REGIONS, debug=False):
    """
    Load far-field electric field (far-field pattern) from Stuart's simulations of ASKAP patterns

    Args:
        field_fname (str): template name of field file
        n_regions (int): number of regions (each in individual .mat file)
        debug (bool): print debug info if True
        
    Returns:
        e_field (`numpy.ndarray`): Ex,Ey,Ez field components in columns and one row per simulation point (direction)
        complex valued    
    """
    # peek in first file to get dimensions of data
    file1 = h5py.File(field_fname + '1.mat', 'r')
    n_ports = file1['Ex1'].shape[0]
    points_per_region = file1['Ex1'].shape[1]
    file1.close()

    e_field = np.zeros((n_ports, n_regions * points_per_region, 3), 'complex')
    for i_region in range(n_regions):
        if debug:
            print('region', i_region)
        region_label = i_region + 1
        pattern_fo = h5py.File(field_fname + '{}.mat'.format(region_label), 'r')
        if debug:
            print(pattern_fo.keys())
            print(pattern_fo['Ex{}'.format(region_label)][...].shape)
        e_field[:, i_region * points_per_region:(i_region + 1) * points_per_region, 0] = \
            pattern_fo['Ex{}'.format(region_label)][...]
        e_field[:, i_region * points_per_region:(i_region + 1) * points_per_region, 1] = \
            pattern_fo['Ey{}'.format(region_label)][...]
        e_field[:, i_region * points_per_region:(i_region + 1) * points_per_region, 2] = \
            pattern_fo['Ez{}'.format(region_label)][...]
        if debug:
            print (np.max(e_field[0, i_region * points_per_region:(i_region + 1) * points_per_region, 0].real))
        pattern_fo.close()
    return e_field


def interpolate_sub_slow(e_field, xyz, xyz_target):
    """
    Interpolate function at finite list of coordinates that are not necessarily on a grid
    
    Interpolation is performed in the Sin projection, with tangent at the positive x direction that is the forward 
    hemisphere of the antenna pattern.  This is probably okay near the boresight.
    
    Args:
        e_field (`numpy.ndarray`): Complex valued function of direction in 3-space
        xyz (`numpy.ndarray`): Grid points representing directions in 3-space at which e_field is evaluated
        xyz_target (`numpy.ndarray`): List of specific directions in 3-space to interpolate at

    Returns:
        e_interp (`numpy.ndarray`): Values of e_field at directions xyz_target

    """
    pts = xyz_target[:, 1:]

    # extract_indices for positive x direction (theta = 0, phi = 0)
    # noinspection PyTypeChecker,PyUnresolvedReferences
    ind_forward = np.nonzero(xyz[:, 0] >= 0)[0]

    e_interp = np.zeros((e_field.shape[0], xyz_target.shape[0], 2), 'complex64')

    print (e_field.shape)
    print (xyz.shape)
    print (xyz_target.shape)

    for i_port in range(e_field.shape[0]):
        for i_component in range(1, 3):
            # noinspection PyTypeChecker
            eir = griddata((xyz[ind_forward, 1], xyz[ind_forward, 2]),
                           np.real(e_field[i_port, ind_forward, i_component]), pts, method='cubic')
            # noinspection PyTypeChecker
            eii = griddata((xyz[ind_forward, 1], xyz[ind_forward, 2]),
                           np.imag(e_field[i_port, ind_forward, i_component]), pts, method='cubic')
            ei = eir + 1j * eii
            e_interp[i_port, :, i_component - 1] = ei

    return e_interp


def interp_weights(xy, uv, d=2):
    """
    Setup function for reimplementation of scipy.interpolate.griddata to avoid repeating setup for repeated 
    interpolation for common input and output grids.
    
    1. Call sp.spatial.qhull.Dealunay is made to triangulate the irregular grid coordinates.
    2. For each point in the new grid, the triangulation is searched to find in which triangle (actually, in which 
    simplex, which in your 3D case will be in which tetrahedron) does it lay.
    3. The barycentric coordinates of each new grid point with respect to the vertices of the enclosing simplex are 
    computed.
    
    From http://stackoverflow.com/questions/20915502
    
    Args:
        xy: existing coordinates for available data
        uv: points to interpolate to
        d: dimension 

    Returns:
        vertices:
        weights: 

    """
    tri = qhull.Delaunay(xy)
    simplex = tri.find_simplex(uv)
    # noinspection PyUnresolvedReferences
    vertices = np.take(tri.simplices, simplex, axis=0)
    temp = np.take(tri.transform, simplex, axis=0)
    delta = uv - temp[:, d]
    bary = np.einsum('njk,nk->nj', temp[:, :d, :], delta)
    return vertices, np.hstack((bary, 1 - bary.sum(axis=1, keepdims=True)))


def interpolate(values, vtx, wts):
    """  
    Reimplementation of scipy.interpolate.griddata to avoid repeating setup for repeated interpolation for common input
    and output grids.
    
    4. An interpolated values is computed for that grid point, using the barycentric coordinates, and the values of the 
    function at the vertices of the enclosing simplex.
    
    http://stackoverflow.com/questions/20915502

    
    Args:
        values: available data
        vtx: vertices from interp_weights()
        wts: weights from interp_weights()

    Returns:
        values interpolated to points determined by setup function interp_weights()

    """
    return np.einsum('nj,nj->n', np.take(values, vtx), wts)


def interpolate_sub(e_field, xyz, xyz_target):
    """
    Interpolate function at finite list of coordinates that are not necessarily on a grid

    Interpolation is performed in the Sin projection, with tangent at the positive x direction that is the forward 
    hemisphere of the antenna pattern.  This is probably okay near the boresight.

    Args:
        e_field (`numpy.ndarray`): Complex valued function of direction in 3-space
        xyz (`numpy.ndarray`): Grid points representing directions in 3-space at which e_field is evaluated
        xyz_target (`numpy.ndarray`): List of specific directions in 3-space to interpolate at

    Returns:
        e_interp (`numpy.ndarray`): Values of e_field at directions xyz_target

    """
    pts = xyz_target[:, 1:]

    # extract_indices for positive x direction (theta = 0, phi = 0)
    # noinspection PyTypeChecker,PyUnresolvedReferences
    ind_forward = np.nonzero(xyz[:, 0] >= 0)[0]

    e_interp = np.zeros((e_field.shape[0], xyz_target.shape[0], 2), 'complex64')

    vtx, wts = interp_weights(xyz[ind_forward, 1:], pts)

    for i_port in range(e_field.shape[0]):
        for i_component in range(1, 3):
            # noinspection PyTypeChecker
            eir = interpolate(np.real(e_field[i_port, ind_forward, i_component]), vtx, wts)
            # noinspection PyTypeChecker
            eii = interpolate(np.imag(e_field[i_port, ind_forward, i_component]), vtx, wts)

            ei = eir + 1j * eii
            e_interp[i_port, :, i_component - 1] = ei

    return e_interp
