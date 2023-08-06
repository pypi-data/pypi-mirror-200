#!/usr/bin/env python
"""
illuminate
Inverts complex holography maps to get illumiation distributions over ASKAP antennas.

 $Author: mcc381 $


"""
import argparse as ap
import numpy as np
import matplotlib.pylab as plt
import matplotlib as mpl
import logging
import sys

from numpy import pi
import numpy.fft as nf
from numpy.linalg import lstsq

import aces.beamset.beambase as bb
import aces.beamset.beamfactory as bf

mpl.rc('image', origin='lower')
mpl.rc('image', cmap='viridis_r')
# mpl.rc('image', cmap='magma_r')

a3_size = (16.5, 11.7)

explanation = """
 Perform the following steps:
   - apply taper to i_holo - the holography complex data
    - note that the tapering option has been omitted;
   - Pad the data; amount of padding given by pad_factor
    - create larger array with zeros - making sure it is complex
    - copy in the map data into the central portion, with shift if necessary to centre the beam
   - Rotate data array to put the origin at 0,0, ready for transform
   - Fourier transform to give aperture illumination
   
 Usage:
 
 To plot amplitudes of all ports AK03, channel 270, SBID 5977
 illuminate.py  -a 3 -c 270 -o m -s 5977
 
 As before but for phase
 illuminate.py  -a 3 -c 270 -o mp -s 5977
 
 To plot aperture illumination function (amplitude and phase) for beam (or port) 26, 
 AK03, channel 270, SBID 5977
 illuminate.py  -a 3 -c 270 -o a -s 5977
 
 As previous, but also plot beam amplitude and phase
 illuminate.py  -a 3 -c 270 -o b -s 5977
 
"""


def get_diag(x, m, sw=True):
    # sw True means lower left to upper right; otherwise NW to SE.
    sh = m.shape
    if sh[0] == sh[1]:
        # all ok
        if sw:
            jys = list(range(sh[1]))
        else:
            jys = list(range(sh[1] - 1, -1, -1))
        js = list(range(sh[0]))
        diag = np.array([m[j, jy] for j, jy in zip(js, jys)])
        xy = x * np.sqrt(2.0)
        return xy, diag
    else:
        print("Must be square")
        return None


def set_bounds(coord, extr):
    # assume square arrays throughout
    size = coord.shape[0]
    c = size / 2
    b1, b2 = c - extr, c + extr + 1
    b1, b2 = max(0, b1), min(size - 1, b2)
    extent = [coord[b1], coord[b2]]
    return slice(b1, b2), extent


class Aperture(object):
    # Perform the following steps:
    #   apply taper to i_holo - the holography complex data
    #   Pad the tapered data; amount of padding given by pad_factor
    #    - create larger array with zeros - making sure it is complex
    #    - copy in the map data into the central portion, with shift if necessary to centre the beam
    #   Rotate data array to put the origin at 0,0, ready for transform
    #   Fourier transform to give aperture illumination
    def __init__(self, beam_map, pad_factor):
        """

        :param beam_map:
        :param pad_factor:
        """
        do_centre = True
        self.sbid = 0
        self.chan = 0
        self.mpc = beam_map
        self.i_holo = self.mpc.data
        self.pad_factor = pad_factor
        self.nx = self.mpc.nx
        self.dx = self.mpc.dx
        self.taper = self.make_taper()
        self.i_pad, self.i_win, self.xy_shift = self.pad_taper(do_centre)
        self.a_field = self.transform_to_aperture()

        self.wavelen, self.i_xg, self.a_xg = self.get_scales()
        # Establish some plottable quantities: extracts from the primary complex data
        self.i_ampl = None
        self.i_phase = None
        self.a_ampl = None
        self.a_phase = None
        self.i_real = None
        self.i_imag = None
        self.a_real = None
        self.a_imag = None
        self.ext_a = None
        self.ext_i = None
        self.a_xg_s = None
        self.i_xg_s = None
        self.a_phase_cor = None
        self.a_phase_flat = None
        self.prepare_plot_quantities()

    def set_sbid(self, s):
        self.sbid = s

    def set_chan(self, s):
        self.chan = s

    def make_taper(self):
        """

        :return:
        """
        nx = self.nx
        ix = list(range(-nx / 2, nx / 2))
        i_gx, i_gy = np.meshgrid(ix, ix)
        i_gr = np.sqrt((i_gx + 0.5) ** 2 + (i_gy + 0.5) ** 2)

        R1, R2 = nx / 2 * 0.9, nx / 2
        i_taper = (np.cos((i_gr - R1) / (R2 - R1) * np.pi) + 1.0) / 2.0

        i_taper[i_gr < R1] = 1.0
        i_taper[i_gr > R2] = 0.0

        return i_taper

    def pad_taper(self, do_centre=True, taper=None):
        """

        :param do_centre:
        :param taper:
        :return:
        """
        # Apply taper
        if taper:
            self.i_holo *= self.taper

        # Make padded map array
        #     pad_factor = 8
        pshape = [i * self.pad_factor + 1 for i in self.i_holo.shape]
        i_pad = np.zeros(pshape) + 0j * np.zeros(pshape)
        i_win = np.zeros(pshape) + 0j * np.zeros(pshape)
        #     print "Interpolated map size : {:d}, Padded map size : {:d}".format(i_holo.shape[0], pshape[0])

        # Copy map data into padded array
        pex = self.nx / 2  # half extent of input data
        pc = pshape[0] / 2  # centre of padded array
        if do_centre:
            # find peak in absolute magnitude, and compute shift (Noting python's tendency to give y (up/down) first)
            pko = np.where(np.abs(self.i_holo) == np.abs(self.i_holo).max())
            xo, yo = self.nx / 2 - pko[1][0], self.nx / 2 - pko[0][0]
        else:
            # or no shift
            xo, yo = 0, 0
        # Note again that the x offset needs to apply to the "y" coordinate and vice versa
        i_pad[pc - pex + yo:pc + pex + 1 + yo, pc - pex + xo:pc + pex + 1 + xo] = self.i_holo

        # and construct the window for later
        i_win[pc - pex:pc + pex + 1, pc - pex:pc + pex + 1] = 1.0
        return i_pad, i_win, (xo, yo)

    def transform_to_aperture(self):
        """

        :return:
        """
        # Rotate the data array around for the transform
        # Note that the i form of the shift is used. ifftshift and fftshift are identical for
        # even length arrays. But the i form seems to do the correct thing for odd lengths.
        # We try and arrange the holography grids to have odd numbers of rows and columns, with
        # the map centre unambigously on the central grid line.
        i_pad_sh = nf.ifftshift(self.i_pad)

        # and transform, by Fourier
        # * Caution (2018-SEP-28) : here the original code was nf.fft2(i_pad_sh). It looked like the
        # orientation of the aperture functions was inverted, so the ifft version was tried.
        # With ifft, the orientation looks correct. There is no deeper reasoning behind this change
        # and choice of trasnform direction.

        return nf.fftshift(nf.ifft2(i_pad_sh))

    def get_scales(self):
        """

        :return:
        """
        #   Compute the scales of the aperture illumnation functions

        # raw_delta = objh.metadata['xAxis'][1] - objh.metadata['xAxis'][0]
        nx = self.nx
        delta_x = self.dx
        mpfrq = self.mpc.vector[4]
        wavelen = 300./mpfrq
        ft_extent = wavelen/delta_x
        # ft_grid = ft_extent/(self.a_field.shape[0]-1)
        # holo_grid_extent = self.mpc.x[-1] - self.mpc.x[0]
        # resolution = wavelen/holo_grid_extent

        fac = 1.0 * nx/(nx - 1)
        i_xg = np.linspace(self.pad_factor*self.mpc.x[0], self.pad_factor*self.mpc.x[-1], self.a_field.shape[0]) * fac

        a_xg = np.linspace(-ft_extent/2, ft_extent/2, self.a_field.shape[0])
        return wavelen, i_xg, a_xg

    def prepare_plot_quantities(self):
        i_pad = self.i_pad
        i_xg = self.i_xg
        a_field = self.a_field
        a_xg = self.a_xg
        # set_vector = self.mpc.vector

        halfi = self.nx / 2
        halfa = 40
        sla, exta = set_bounds(a_xg, halfa)
        sli, exti = set_bounds(i_xg, halfi)
        self.ext_i = np.array(exti + exti) * 180.0 / pi
        self.ext_a = np.array(exta + exta)
        self.a_xg_s = a_xg[sla]
        self.i_xg_s = i_xg[sli]

        a_field_sub = a_field[sla, sla]
        i_pad_sub = i_pad[sli, sli]

        self.a_ampl = np.abs(a_field_sub)
        self.a_ampl /= self.a_ampl.max()

        ph = np.angle(a_field_sub)
        xh, yh = np.meshgrid(self.a_xg_s, self.a_xg_s)
        rh = np.sqrt(xh ** 2 + yh ** 2)

        self.a_phase = np.ma.masked_array(ph, mask=rh > 6.1)
        self.a_phase_cor, self.a_phase_flat = self.fix_phase()
        self.a_real = np.real(a_field_sub)
        self.a_imag = np.imag(a_field_sub)

        self.i_ampl = np.abs(i_pad_sub)
        self.i_phase = np.angle(i_pad_sub)
        self.i_real = np.real(i_pad_sub)
        self.i_imag = np.imag(i_pad_sub)

    def summary(self):
        # print "Raw grid spacing     = {:.3f} deg".format(np.degrees(raw_delta))
        ft_extent = self.wavelen / self.dx
        ft_grid = ft_extent/(self.a_field.shape[0]-1)
        holo_grid_extent = self.mpc.x[-1] - self.mpc.x[0]
        resolution = self.wavelen/holo_grid_extent
        print(("Interp. grid spacing = {:.3f} deg".format(np.degrees(self.dx))))
        print(("Grid size            = {:.3f} deg".format(np.degrees(self.mpc.x[-1] - self.mpc.x[0]))))

        print(('Wavelength           = {:.3f} m'.format(self.wavelen)))
        print(('Transform extent     = {:.2f} m'.format(ft_extent)))
        print(('Transform grid       = {:.3f} m'.format(ft_grid)))
        print(('Resolution           = {:.2f} m'.format(resolution)))

    def insert_test(self):
        # ------- test code, puts gaussian at centre
        ii = np.arange(0, self.i_pad.shape[0], 1)
        iic = self.i_pad.shape[0]/2
        iu, iv = np.meshgrid(ii, ii)
        ir = np.sqrt((iu-iic)**2 + (iv-iic)**2)
        self.i_pad = np.exp(-(ir/3.)**2) * (1.0+0j)
        self.xy_shift = [0.0, 0.0]
        # -------- end test code

    def plot_filename(self, option, plot_num, amppha=""):
        sbid = self.sbid
        tim, ant, beam, pol, frq = self.mpc.vector
        if option == 'ports':
            beam_pol = "ports_"
            opt = amppha
        else:
            beam_pol = "beam{:d}_{:s}_".format(beam, pol)
            opt = option
        pname = "SB{:d}_AK{:02d}_{}_{}_{:03d}.png".format(sbid, ant, beam_pol, opt, plot_num)

        # if option == 'both':
        #     pname = "SB{:d}_AK{:02d}_beam{:d}_{:s}_{:d}_{}.png".format(sbid, ant, beam, pol, plot_num, option)
        # elif option == 'aper':
        #     pname = "SB{:d}_AK{:02d}_beam{:d}_{:s}_{:d}_aper.png".format(sbid, ant, beam, pol, plot_num)
        # elif option == 'ports':
        #     pname = "SB{:d}_AK{:02d}_{:d}_port_{}.png".format(sbid, ant, plot_num, amppha)
        return pname

    def plot_both(self, sbid):
        # i_pad, i_xg, a_field, a_xg, hol_ext, sbid, set_vector):
        # Plot the FT inputs and outputs
        # select the central portion
        set_vector = self.mpc.vector

        ext_i = self.ext_i
        ext_a = self.ext_a
        fig, axes = plt.subplots(4, 3, figsize=(12.0, 16.0))

        # Top column is map: real, imaginary, amplitude, phase
        axes[0, 0].imshow(self.i_real, extent=ext_i)
        axes[1, 0].imshow(self.i_imag, extent=ext_i)
        axes[2, 0].imshow(self.i_ampl, extent=ext_i)
        axes[3, 0].imshow(self.i_phase, extent=ext_i)

        # second column is aperture illumination: real, imaginary, amplitude, phase
        axes[0, 1].imshow(self.a_real, extent=ext_a)
        axes[1, 1].imshow(self.a_imag, extent=ext_a)
        axes[2, 1].imshow(self.a_ampl, extent=ext_a)
        axes[3, 1].imshow(self.a_phase, extent=ext_a)

        # print a_field_sub.shape
        # xs = np.arange(a_field_sub.shape[0])
        x = self.a_xg_s
        xy, d = get_diag(x, self.a_ampl)
        xy, do = get_diag(x, self.a_ampl, sw=False)

        # Third column in slices through images of second row:
        axes[0, 2].plot(x, self.a_real)
        axes[1, 2].plot(x, self.a_imag)

        axes[2, 2].plot(xy, d)
        axes[2, 2].plot(xy, do)
        axes[2, 2].set_xlim(x[0], x[-1])

        axes[3, 2].plot(x, self.a_phase[30, :])
        axes[3, 2].plot(x, self.a_phase[:, 30])

        axes[0, 0].set_title('Beam')
        axes[0, 1].set_title('Aperture')

        axes[3, 0].set_xlabel('degrees x degrees')
        axes[3, 1].set_xlabel('metres x metres')
        axes[3, 2].set_xlabel('metres')

        kw = {'rotation': 'horizontal', 'size': 'large', 'ha': 'right'}
        axes[0, 0].set_ylabel('Real', **kw)
        axes[1, 0].set_ylabel('Imaginary', **kw)
        axes[2, 0].set_ylabel('Amplitude', **kw)
        axes[3, 0].set_ylabel('Phase', **kw)

        tim, ant, beam, pol, frq = set_vector
        f_title = "Aperture illumination  SB{:d}  AK{:02d} beam {:d} {:s}  {:.0f} MHz".format(sbid, ant, beam, pol, frq)
        plt.suptitle(f_title)
        pname = self.plot_filename('both', self.chan)
        plt.savefig(pname, dpi=300)
        plt.close()

    def plot_aperture(self, sbid, plot_num):
        a_ampl = self.a_ampl
        a_phase = self.a_phase

        set_vector = self.mpc.vector

        # prepare to draw dish and PAF extents
        dish_rad = 6.0
        paf_rad = dish_rad * 165./1680    # scaled off ASKAP_antenna.pdf
        th = np.linspace(-180.0, 181.0, 360) * np.pi/180.0
        xd = dish_rad * np.cos(th)
        yd = dish_rad * np.sin(th)
        xp = paf_rad * np.cos(th)
        yp = paf_rad * np.sin(th)

        fig, axes = plt.subplots(2, 2, figsize=(12.0, 12.0))
        fig.subplots_adjust(hspace=0.01)

        # print "Putative aperture efficiency {:.3f}".format((amplm**2).mean())

        p_mean = a_phase.mean()
        levs = np.array([0.03, 0.05, 0.08, 0.13, 0.21, 0.35])
        ax = axes[0, 0]
        ax.contour(self.a_xg_s, self.a_xg_s, a_ampl, linewidths=0.5, colors='r', levels=levs)
        ax.imshow(a_ampl, origin='lower', cmap='Greys', extent=self.ext_a)
        ax.plot(xd, yd, '-k', lw=1.5)
        ax.plot(xp, yp, '-k', lw=1.5)
        ax.set_ylabel('metres')
        ax.grid()
        ax.set_title('Amplitude')
        ax.xaxis.set_ticklabels([])

        plevs = np.linspace(-60.0, 60.0, 25) * np.pi/180 + p_mean
        # cs = axes[0,1].contourf(a_xg_1, a_xg_1, phas, linewidths=0.5, colors = 'r', levels=plevs)
        axes[0, 1].set_aspect('equal')
        cs = axes[0, 1].contourf(self.a_xg_s, self.a_xg_s, a_phase, linewidths=0.5, levels=plevs)
        # axes[0,1].imshow(phas, extent=ext)
        ax = axes[0, 1]
        ax.plot(xd, yd, '-k', lw=1)
        ax.plot(xp, yp, '-k', lw=1)
        ax.grid()
        ax.set_title('Phase')
        ax.xaxis.set_ticklabels([])

        xa, a_diag_sw = get_diag(self.a_xg_s, a_ampl, True)
        xa, a_diag_nw = get_diag(self.a_xg_s, a_ampl, False)
        ax = axes[1, 0]
        ax.plot(xa, a_diag_sw, '-b', label='SW')
        ax.plot(xa, a_diag_nw, '-r', label='NW')
        ax.set_xlim(self.ext_a[0], self.ext_a[1])
        ax.vlines([-6., 6], 0., 1.0)
        ax.set_xlabel('metres')
        ax.set_ylabel('relative amplitude')
        ax.grid()
        ax.legend()

        xa, p_diag_sw = get_diag(self.a_xg_s, a_phase, True)
        xa, p_diag_nw = get_diag(self.a_xg_s, a_phase, False)
        ax = axes[1, 1]
        ax.plot(xa, np.degrees(p_diag_sw), '-b', label='SW')
        ax.plot(xa, np.degrees(p_diag_nw), '-r', label='NW')
        ax.set_xlim(self.ext_a[0], self.ext_a[1])
        ax.set_ylim(-200.0, 200.0)
        yl, yu = plt.ylim()
        ax.vlines([-6., 6], yl, yu)
        ax.set_xlabel('metres')
        ax.set_ylabel('degrees')
        ax.grid()
        ax.legend()

        tim, ant, beam, pol, frq = set_vector
        f_title = "Aperture illumination  SB{:d}  AK{:02d} beam {:d} {:s}  {:.0f} MHz".format(sbid, ant, beam, pol, frq)
        plt.suptitle(f_title)
        pname = self.plot_filename('aper', plot_num)
        plt.savefig(pname, dpi=300)
        print(("Written to {}".format(pname)))
        plt.close()

    def plot_port(self, ax, port, **kw):
        params = {}
        # ext_a = self.ext_a
        a_xg_1 = self.a_xg_s

        # prepare to draw dish and PAF extents
        dish_rad = 6.0
        paf_rad = dish_rad * 165./1680    # scaled off ASKAP_antenna.pdf
        th = np.linspace(-180.0, 181.0, 360) * np.pi/180.0
        xd = dish_rad * np.cos(th)
        yd = dish_rad * np.sin(th)
        xp = paf_rad * np.cos(th)
        yp = paf_rad * np.sin(th)

        if kw['which'] == 'ampl':
            # levs = np.array([0.03, 0.05, 0.08, 0.13, 0.21, 0.35])
            # ax.contour(self.a_xg_s, self.a_xg_s, self.a_ampl, linewidths=0.2, colors='r', levels=levs)
            # ax.imshow(self.a_ampl, origin='lower', cmap='Greys', extent=ext_a)
            levs = np.linspace(0.2, 1.0, 25)**2
            cs = ax.contourf(self.a_xg_s, self.a_xg_s, self.a_ampl, linewidths=0.2, levels=levs)
            ax.patch.set_alpha(0.5)
            ax.plot(xd, yd, '-k', lw=0.2)
            ax.plot(xp, yp, '-k', lw=0.2)
            ax.xaxis.set_ticklabels([])
            params['phase_range'] = None
        else:
            range_factor = 1.0
            if kw['do_flatten']:
                phase_plot = self.a_phase_flat * 180.0/pi
                range_factor = 1.3
            else:
                phase_plot = self.a_phase_cor * 180.0/pi

            vmin = phase_plot.min()
            vmax = phase_plot.max()

            ph_range = kw['phase_range']
            if ph_range == 0.0:
                ph_range = vmax - vmin
            vcentre = (vmin + vmax)/2.0
            vmin = vcentre - range_factor * ph_range/2.
            vmax = vcentre + range_factor * ph_range/2.
            params['phase_range'] = ph_range
            phase_plot -= vcentre
            plevs = np.linspace(vmin - vcentre, vmax - vcentre, 25)
            ax.set_aspect('equal')
            cs = ax.contourf(a_xg_1, a_xg_1, phase_plot, linewidths=0.2, levels=plevs)
            ax.plot(xd, yd, '-k', lw=0.2)
            ax.plot(xp, yp, '-k', lw=0.2)
            ax.xaxis.set_ticklabels([])

        ax.text(7.0, 7.0, "{:d}".format(port), fontsize=8, va='center', ha='center')
        params['image'] = cs
        return params

    def fix_phase(self):
        """

        """
        phase = self.a_phase
        a_xg = self.a_xg_s
        wavelen = self.wavelen
        xy_shift = self.xy_shift
        xh, yh = np.meshgrid(a_xg, a_xg)
        rh = np.sqrt(xh ** 2 + yh ** 2)

        # ic = phase.shape[0] / 2
        phase_range = phase.max() - phase.min()
        if phase_range > pi:
            ph_incr = 2.*pi
        else:
            ph_incr = -phase.min()
        phase_unwound = np.mod(phase + ph_incr, 2.0 * pi)
        phase_f = phase_unwound.flatten()
        xh_f = xh.flatten()
        yh_f = yh.flatten()
        rh_f = rh.flatten()
        xyg = np.zeros((phase.flatten().shape[0], 3))
        xyg[:, 0] = xh_f
        xyg[:, 1] = yh_f
        xyg[:, 2] = 1.0
        msk = (rh_f > 6.0)
        xym = np.ma.masked_array(phase_f, mask=msk)

        a, b, aa = [], [], []
        for g, m in zip(xyg, xym):
            aa.append(g)
            if not np.ma.is_masked(m):
                a.append(g)
                b.append(m)
        a = np.array(a)
        b = np.array(b)
        q = lstsq(a, b)
        x, res, rank, s = q
        a0, b0, ph0 = x
        # print x, res

        ox, oy = xy_shift
        dthx, dthy = ox * self.dx, oy * self.dx
        a1 = dthx * 2. * pi / wavelen
        b1 = dthy * 2. * pi / wavelen

        phase_cor = phase_unwound + a1 * xh + b1 * yh
        phase_z = phase_unwound - a0 * xh - b0 * yh

        return phase_cor, phase_z


def make_port_axis(fig, port_pos):
    scales = 1.0/fig.get_size_inches()
    centre = np.array([0.65, 0.5])
    wh = 0.9 * scales
    w, h = wh
    l, b = port_pos * scales + centre - wh/2.
    ax = fig.add_axes([l, b, w, h])
    return ax


def make_label_axes(fig):
    scales = 1.0/fig.get_size_inches()
    axes = []
    # Left box:
    l, b, w, h = 0.0, 0.7, 0.35, 0.3
    axes.append(fig.add_axes([l, b, w, h]))
    # top right
    d = 2.0 * scales
    l, b, w, h = 1.0 - d[0], 1.0 - d[1], d[0], d[1]
    axes.append(fig.add_axes([l, b, w, h]))
    # colour bar
    # d = 2.0 * scales
    l, b, w, h = 0.32, 0.7, 0.02, 0.25
    axes.append(fig.add_axes([l, b, w, h]))
    for ax in axes:
        ax.set_axis_off()
    return axes



def arg_init():
    parser = ap.ArgumentParser(prog='illuminate', formatter_class=ap.RawDescriptionHelpFormatter,
                               description='Generate illumination distributions',
                               epilog='See -x for more explanation')
    # noinspection PyTypeChecker
    parser.add_argument('sbid', type=int, help="SBID")
    parser.add_argument('-a', '--antennas', default=list(range(36)), action=IntList,
                        help="Antennas to model [%(default)s]")
    parser.add_argument('-b', '--beams', default=list(range(37)), action=IntList,
                        help="Beam numbers to model [%(default)s]")
    parser.add_argument('-p', '--polarizations', default=['XX', 'YY'], action=PolList,
                        help="Polarizations to model [%(default)s]")
    parser.add_argument('-c', '--channels', default=list(range(0, 300, 30)), action=IntList, type=str,
                        help="Channel numbers to model [%(default)s]")
    parser.add_argument('-m', '--use_mean', action="store_true", help="Use a mean over antennas")
    parser.add_argument('-o', '--plot_options', default='a',
                        help="B (beam and aperture), A (aperture), M (port map), P (phase port map")
    parser.add_argument('-C', '--colour', default=None, help='Colour map to use')
    parser.add_argument('-f', '--do_flatten', action="store_true", help="Flatten the phase with linear fit (shift)")
    parser.add_argument('-s', '--single_port', action="store_true", help="The single port beams for this sbid")
    parser.add_argument('-y', '--movie', action="store_true", help="Number files suitable for animation")
    parser.add_argument('-v', '--verbose', action="store_true")
    parser.add_argument('-x', '--explain', action="store_true", help="Give an expanded explanation")
    return parser


class IntList(ap.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        # print 'ACTION : %r %r %r' % (namespace, values, option_string)
        safe_dict = {'range': range}
        rp = eval(values, safe_dict)
        if isinstance(rp, tuple):
            rp = list(rp)
        if not isinstance(rp, list):
            rp = [rp]
        setattr(namespace, self.dest, rp)


class PolList(ap.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        # print 'ACTION : %r %r %r' % (namespace, values, option_string)
        pols = ['XX', 'YY', 'XY', 'YX', 'I', 'Q', 'U', 'V']
        rp = []
        for p in pols:
            if p in values:
                rp.append(p)
        setattr(namespace, self.dest, rp)


def main():
    # Set up logging
    logging.info('started')
    args = arg_init().parse_args()
    verbose = args.verbose
    sbid = args.sbid
    sp = args.single_port
    ant = args.antennas[0]
    chans = args.channels
    use_mean = args.use_mean
    do_flatten = args.do_flatten
    do_movie = args.movie
    plot_options = args.plot_options.lower()

    if args.colour:
        plt.rcParams["image.cmap"] = args.colour

    if args.verbose:
        print("ARGS = ", args)
    if args.explain:
        print(explanation)
        return

    if plot_options not in ['a', 'b', 'm', 'mp']:
        print("\nInput error:\n  -o argument must be one of 'A', 'B', 'M', 'MP'.\n")
        return

    if use_mean:
        file_template = '/Users/mcc381/askap/ASKAP/beams/{:d}_Holo_ss_mean.hdf5'
        ant = 0
    else:
        if sp:
            file_template = '/Users/mcc381/askap/ASKAP/beams/{:d}_Holo_sp.hdf5'
        else:
            file_template = '/Users/mcc381/askap/ASKAP/beams/{:d}_Holo.hdf5'

    holo = bf.load_beamset_class(file_template.format(sbid))
    if sp and 'm' in plot_options:
        beams = holo.metadata['beams']
    else:
        beams = args.beams

    if verbose:
        holo.print_summary()
    interp = 0.3  # degrees
    holo.set_interp(interp)

    seli = {'times': 0, 'channels': chans, 'polarizations': [0]}
    selv = {'antennas': [ant], 'beams': beams}
    sgen = holo.get_selector(seli, selv)
    if 'm' in plot_options:
        fig1 = plt.figure(figsize=a3_size)
        port_pos = bb.get_port_positions()
        phase_range = 0.0

    seq = 0
    for smap in sgen:
        ti, ai, bi, poli, ci = holo.get_vector(smap)
        chan = smap[4]

        print("Selected item {:f} {:d} {:d} {} {:f} ".format(ti, ai, bi, poli, ci))
        mpc = holo.get_map(smap, maptype='complex')

        pad_fac = 8
        aper = Aperture(mpc, pad_fac)
        aper.set_sbid(sbid)
        aper.set_chan(chan)

        tim, ant, beam, pol, frq = aper.mpc.vector

        if 'b' in plot_options:
            aper.plot_both(sbid)

        if 'a' in plot_options:
            if do_movie:
                i = seq
                seq += 1
            else:
                i = chan
            aper.plot_aperture(sbid, i)

        if 'm' in plot_options:
            bp = beam - 1
            ax = make_port_axis(fig1, port_pos[bp])
            kwargs = {'do_flatten': do_flatten}
            ax.set_axis_off()
            if 'p' in plot_options:
                kwargs['which'] = 'phas'
                kwargs['phase_range'] = phase_range
                cbar_label = r'Phase (deg)'
            else:
                kwargs['which'] = 'ampl'
                cbar_label = r'Relative amplitude'
            r_params = aper.plot_port(ax, beam, **kwargs)
            phase_range = r_params['phase_range']

    if 'm' in plot_options:
        axes = make_label_axes(fig1)

        axes[0].text(0.1, 0.7, "SBID {:d}".format(sbid), fontsize=16)
        axes[0].text(0.1, 0.6, "AK{:02d}".format(ant), fontsize=16)
        axes[0].text(0.1, 0.5, "Channel {:d}, {:.1f} MHz".format(chan, frq), fontsize=14)
        if 'p' in plot_options:
            pname = aper.plot_filename('ports', chan, amppha='phase')
            if do_flatten:
                axes[0].text(0.1, 0.4, "Phase (flattened)", fontsize=16)
            else:
                axes[0].text(0.1, 0.4, "Phase", fontsize=16)
        else:
            pname = aper.plot_filename('ports', chan, amppha='amplitude')
            axes[0].text(0.1, 0.4, "Amplitude", fontsize=16)

        axes[2].set_axis_on()
        cbar = fig1.colorbar(r_params['image'], axes[2])
        cbar.ax.set_ylabel(cbar_label)

        w = kwargs['which']

        fig1.savefig(pname, dpi=300)


# ====END of process ================


if __name__ == "__main__":
    fmt = '%(asctime)s %(levelname)s  %(name)s %(message)s'
    logging.basicConfig(format=fmt, level=logging.DEBUG)
    sys.exit(main())


