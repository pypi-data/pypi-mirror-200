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

"""
Example script to generate signal ACMs from EM simulations for a given footprint
"""

import h5py
import os
import numpy as np
# todo: migrate to ASKAPsoft footprint
from askap.footprint import Footprint
from emsim.readmat import interpolate_sub
import matplotlib.pyplot as plt
# noinspection PyUnresolvedReferences
import seaborn as sns
from emsim.emacm import make_acm_points

antenna = 'ak00'
out_path = '/data/chi139/askap-paf-model/aces/'
# 'SB00000-000.ak0.acm.hdf5'
acm_fbase = 'SB00000'

FP_PITCH = 1.25  # deg
FP_ANGLE = 45.  # deg
FP_NAME = 'square_6x6'

# noinspection PyTypeChecker
# todo: update as named footprints are deprecated
fp = Footprint.named(FP_NAME, np.radians(FP_PITCH), np.radians(FP_ANGLE))

offsets_deg = np.degrees(fp.offsetsRect)

xyz_offsets = np.c_[np.ones((fp.nBeams,)), fp.offsetsRect]
xyz_offsets[:, 1] = -1*xyz_offsets[:, 1]

i_ant = 0  # one antenna per file
n_cyc = 2  # two cycles for now as first cycle is dropped

# todo: swap frequency and beam loop order

with h5py.File('/data/chi139/askap-paf-model/aces/askap_paf_patterns_Struts2.hdf5', 'r') as h5infile:
    freq_MHz = h5infile['frequency'][...]/1e6
    # noinspection PyTypeChecker
    n_freq = len(freq_MHz)

    for i_beam in range(fp.nBeams):
        scan = '{:03d}'.format(i_beam)
        print('scan {}/{}:'.format(i_beam, fp.nBeams))
        acm_fname = acm_fbase + '-' + scan + '.000000000000.' + antenna + '.acm.hdf5'

        with h5py.File(os.path.join(out_path, acm_fname), 'w') as h5out:

            # noinspection PyTypeChecker
            for i_freq, freq in enumerate(freq_MHz):
                print ('  freq {}/{}: {} MHz'.format(i_freq + 1, n_freq, freq))
                if i_beam > 0:
                    points_per_region = h5infile['points_per_region'][i_freq]
                    group = '{}/'.format(points_per_region)
                    i_freq_in_group = h5infile['frequency_number_in_group'][i_freq]

                    e_field = h5infile[group + 'e_field'][i_freq_in_group, ...]
                    xyz = h5infile[group + 'xyz'][i_freq_in_group, ...]
                    # interpolate patterns in directions of footprint offsets
                    e_point = interpolate_sub(e_field, xyz, xyz_offsets)
                    acm = make_acm_points(e_point)
                else:
                    acm = np.eye(188, dtype=np.complex64)

                # now write this out as an ACM file
                # one file per antenna pointing as per SB

                if i_freq == 0:
                    h5out.create_dataset('ACMdata', (n_cyc, n_freq, 192, 192), dtype=np.complex64,
                                         maxshape=(None, n_freq, 192, 192))
                    h5out.create_dataset('skyFrequency', (n_cyc, n_freq), dtype=np.float64, maxshape=(None, n_freq))
                    h5out.create_dataset('onSource', (n_cyc,), dtype=np.bool, maxshape=(None,))
                    h5out['ACMdata'].attrs['band'] = 'SIMULATION_NO_FILTER'

                for i_cyc in range(n_cyc):
                    if i_beam > 0:
                        h5out['ACMdata'][i_cyc, i_freq, :188, :188] = acm[i_beam, :, :]
                    else:
                        h5out['ACMdata'][i_cyc, i_freq, :188, :188] = acm
                    h5out['ACMdata'][i_cyc, i_freq, 188:, :] = np.zeros((4, 192), 'complex64')
                    h5out['ACMdata'][i_cyc, i_freq, :, 188:] = np.zeros((192, 4), 'complex64')
                    h5out['skyFrequency'][i_cyc, i_freq] = freq
                    h5out['onSource'][i_cyc] = True

flip_sign = 1.
plt.figure()
plt.plot(offsets_deg[:, 0], offsets_deg[:, 1], '.')
for i_beam in range(offsets_deg.shape[0]):
    plt.text(flip_sign*offsets_deg[i_beam, 0]+0.1, offsets_deg[i_beam, 1]+0.1, '{}'.format(i_beam), fontsize=7,
             color='k')

# plt.figure()
# plt.plot(np.abs(e_point[:, 0, 0]))
# plt.plot(np.abs(e_point[:, 0, 1]))

plt.show()
