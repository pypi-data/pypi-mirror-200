"""
Coordinate transformations
"""

import numpy as np


def move_main_beam_from_z_to_x(xyz):
    """
    Convert cartesian (x,y,z) with main beam at positive z to cartesian (x,y,z) with main beam at positive x.  This is 
    equivalent to a 90 degree rotation about the y axis.
    
    Args:
        xyz (`numpy.ndarray`): matrix of cartesian coordinates with one row per point (N_POINTS, 3)
        
    Returns:
        rotated_xyz (`numpy.ndarray`): xyz rotated 90 deg about the Y axis so that the main beam is at positive x 
        instead of positive z
    """
    rotated_xyz = xyz[..., [2, 1, 0]].copy()
    rotated_xyz[..., 2] = -1*xyz[..., 0]
    return rotated_xyz


def rotate_field_z_to_x(e_field):
    """
    Convert pattern with main beam at positive z to pattern with main beam at positive x.  This is 
    equivalent to a 90 degree rotation about the y axis.
    
    Args:
        e_field (`numpy.ndarray`): matrix of e_field components in cartesian coordinates with one row per point 
            (N_POINTS, 3)
        
    Returns:
        rotated_e_field (`numpy.ndarray`): e_field rotated 90 deg about the Y axis so that the main beam is at positive 
        x instead of positive z
    """
    rotated_e_field = e_field[:, :, [2, 1, 0]].copy()
    rotated_e_field[:, :, 2] = -1*e_field[:, :, 0]
    return rotated_e_field


def rotate_xyz_about_x(xyz, theta):
    """
    Rotate coordinate system (x,y,z) about x axis by theta radians

    Args:
        xyz (`numpy.ndarray`): matrix of cartesian coordinates with one row per point (N_POINTS, 3)
        theta (float): angle of rotation in radians
        
    Returns:
        rotated_xyz (`numpy.ndarray`): xyz rotated by theta radians about the x axis
    """

    rotation_x = np.array([[1, 0, 0],
                           [0, np.cos(theta), -np.sin(theta)],
                           [0, np.sin(theta), np.cos(theta)]])

    rotated_xyz = np.dot(rotation_x, xyz.T).T

    return rotated_xyz


def xyz_to_rtp(xyz):
    """
    Convert cartesian (x,y,z) coordinates to spherical (r, theta, phi)

    Args:
        xyz (`numpy.ndarray`): matrix of cartesian coordinates with one row per point (N_POINTS, 3)

    Returns:
        rtp: spherical coordinates (r,theta,phi) in radians
    """

    rtp = np.zeros_like(xyz, dtype=float)

    rtp[:, 0] = np.sqrt(xyz[:, 0] ** 2 + xyz[:, 1] ** 2 + xyz[:, 2] ** 2)  # radius, should be 1.0 for unit circle
    rtp[:, 1] = np.arccos(xyz[:, 2] / (rtp[:, 0]))  # theta measured from +'ve z direction down towards z=0 plane
    rtp[:, 2] = np.arctan2(xyz[:, 1], xyz[:, 0])  # phi measured from positive x axis to positive y axis in z=0 plane

    return rtp


def cartesian_to_spherical_basis(xyz):
    """
    Calculate spherical coordinate basis for given direction in cartesian basis
    
    Args:
        xyz (`numpy.ndarray`): matrix of cartesian coordinates with one row per point (N, 3)
        
    Returns:
        a_r (`numpy.ndarray`): matrix of a_r (radius) basis vectors in cartesian coordinates (N, 3) corresponding to 
            each direction (row) in xyz
        a_t (`numpy.ndarray`): matrix of a_t (theta) basis vectors in cartesian coordinates (N, 3) corresponding to each
            direction (row) in xyz
        a_p (`numpy.ndarray`): matrix of a_p (phi) basis vectors in cartesian coordinates (N, 3) corresponding to each
            direction (row) in xyz
    """

    rtp = xyz_to_rtp(xyz)

    a_r = np.zeros_like(xyz, dtype='float')
    a_t = np.zeros_like(xyz, dtype='float')
    a_p = np.zeros_like(xyz, dtype='float')

    a_r[:, 0] = np.sin(rtp[:, 1]) * np.cos(rtp[:, 2])
    a_r[:, 1] = np.sin(rtp[:, 1]) * np.sin(rtp[:, 2])
    a_r[:, 2] = np.cos(rtp[:, 1])

    a_t[:, 0] = np.cos(rtp[:, 1]) * np.cos(rtp[:, 2])
    a_t[:, 1] = np.cos(rtp[:, 1]) * np.sin(rtp[:, 2])
    a_t[:, 2] = -np.sin(rtp[:, 1])

    a_p[:, 0] = -np.sin(rtp[:, 2])
    a_p[:, 1] = np.cos(rtp[:, 2])
    a_p[:, 2] = 0.

    return a_r, a_t, a_p


# this is inefficient because it is not vectorized
def project_field_slow(e_field, a_1, a_2, a_3):
    """
    Project electric field (pattern) onto given basis

    Args:
        e_field (`numpy.ndarray`): (M,N,3) complex valued electric field with 3 vector components (columns) evaluated at 
            N points (rows) for M ports
        a_1 ():  (N,3) coordinate system basis vector a_1 for each of N points (directions)
        a_2 ():  (N,3) coordinate system basis vector a_2 for each of N points (directions)
        a_3 ():  (N,3) coordinate system basis vector a_3 for each of N points (directions)

    """
    e_field_proj = np.zeros_like(e_field)

    # port, field point, xyz
    for i_port in range(e_field_proj.shape[0]):
        for i_point in range(e_field_proj.shape[1]):
            e_field_proj[i_port, i_point, 0] = np.dot(a_1[i_point, :], e_field[i_port, i_point, :])
            e_field_proj[i_port, i_point, 1] = np.dot(a_2[i_point, :], e_field[i_port, i_point, :])
            e_field_proj[i_port, i_point, 2] = np.dot(a_3[i_point, :], e_field[i_port, i_point, :])

    return e_field_proj


def project_field(e_field, a_1, a_2, a_3):
    """
    Project electric field (pattern) onto given basis

    Args:
        e_field (`numpy.ndarray`): (M,N,3) complex valued electric field with 3 vector components (columns) evaluated at 
            N points (rows) for M ports
        a_1 ():  (N,3) coordinate system basis vector a_1 for each of N points (directions)
        a_2 ():  (N,3) coordinate system basis vector a_2 for each of N points (directions)
        a_3 ():  (N,3) coordinate system basis vector a_3 for each of N points (directions)
    """
    e_field_proj = np.zeros_like(e_field)

    e_field_proj[:, :, 0] = np.einsum("ijk, jk -> ij", e_field, a_1)
    e_field_proj[:, :, 1] = np.einsum("ijk, jk -> ij", e_field, a_2)
    e_field_proj[:, :, 2] = np.einsum("ijk, jk -> ij", e_field, a_3)

    return e_field_proj
