#!/usr/bin/env python
"""
Defines the MapSet subclass of BeamSet
Copyright (C) CSIRO 2017

"""
import numpy as np
import scipy.interpolate as sp
from astropy.stats import sigma_clip, mad_std
import matplotlib.pyplot as plt
from aces.beamset import beamset
from aces.beamset import beammap as bm
import time

beamset.KnownBeamSetTypes.append("MapSet")


class MapSet(beamset.BeamSet):
    """
    MapSet is based on BeamSet. See comments in that class, which describes the structure of data
    and flag arrays.

    MapSet holds sets of beam maps (the payloads), assumed to be held as 2D ndarrays of
    complex values.
    Axis length and grid interval can be different, but gird intervals are equal in the two
    directions after interpolation.

    Metadata items additional to those defined for BeamSet:
    * 'xAxis' - list of grid positions in x-direction
    * 'yAxis' - list of grid positions in y-direction

    """
    metadataDefaults = {'class': 'MapSet',
                        'xAxis': [],
                        'yAxis': []}

    allowedMapTypes = ['complex', 'amplitude', 'phase', 'power', 'real', 'imag']
    payloadtype = 'complex'

    def __init__(self, metadata=None, data=None, flags=None, filename=None):
        """
        Initialise MapSet object
        :param dict metadata: carries necessary ancillary quantities as defined in BeamSet
        :param data: map data payload
        :type data: :class:`numpy.ndarray`
        :param flags:
        :type flags: :class:`numpy.ndarray`
        :param str filename: if present, read object data from it
        
        """

        beamset.BeamSet.__init__(self, metadata, data, flags, filename)

        #: grid interval for map interpolation, set by self.set_interp()
        self.xs = self.metadata['xAxis']
        self.ys = self.metadata['yAxis']
        self.xsi = None  # overwritten by self.set_interp()
        self.ysi = None  # overwritten by self.set_interp()
        self.nx = len(self.xs)
        self.ny = len(self.ys)
        self.is1D = False
        if self.nx <= 1:
            self.dx = 0.0
            self.is1D = True
        else:
            self.dx = np.diff(self.xs).mean()
        if self.ny <= 1:
            self.dy = 0.0
            self.is1D = True
        else:
            self.dy = np.diff(self.ys).mean()
        self.delta = max(self.dx, self.dy)

        self.interp_step = self.delta
        self.need_interp = False
        self.set_interp(np.degrees(self.interp_step))
        # Add channel and antenna flags
        self.bad_ants = None
        self.bad_chans = None

    def print_summary(self):
        """
        Prints to standard output a summary
        """
        beamset.BeamSet.print_summary(self)
        print("")
        print("Maps on {:d} x {:d} x-y grid ".format(self.nx, self.ny))
        if self.nx > 1:
            print("x-axis {:.2f} to {:.2f} step {:.2f} deg".format(np.degrees(self.xs[0]),
                                                                   np.degrees(self.xs[-1]),
                                                                   np.degrees(self.dx)))
        if self.ny > 1:
            print("y-axis {:.2f} to {:.2f} step {:.2f} deg".format(np.degrees(self.ys[0]),
                                                                   np.degrees(self.ys[-1]),
                                                                   np.degrees(self.dy)))

    def set_phase_to_zero(self):
        myAmplitude = np.abs(self.data)
        self.data = myAmplitude + 1j * 0.0

    def set_interp(self, interp_step=None):
        """
        Sets the grid interval for map interpolation to be the smaller of the current interval
        and the given value.
        :param interp_step: New grid interval for interpolation, in degrees.
        """
        if interp_step is None:
            return

        # stepi = self.delta / int(self.delta / np.radians(interp_step))
        self.interp_step = min(np.radians(interp_step), self.delta)

        if self.interp_step == self.delta:
            self.xsi = self.xs
            self.ysi = self.ys
        else:
            self.xsi = self._do_axis(self.xs, self.interp_step)
            self.ysi = self._do_axis(self.ys, self.interp_step)
            self.need_interp = True

    def get_beam_positions(self):
        """
        Return beam positions in array index space.
        :return:
        """
        offsets_rad = np.radians(self.get_beam_offsets())

        ret = (offsets_rad - [-self.xsi[0], self.ysi[0]]) / self.interp_step * [-1., 1.]
        return ret

    def put_map_array(self, selection, data):
        """
        :param selection: slice destination array
        :param data: 2D ndarray of values
        """
        self.data[selection] = data

    def get_map(self,
                selection,
                maptype='amplitude',
                normalise=False,
                average=None,
                flag=None
                ):
        """
        Retrieves a single map from the set as a BeamMap object.
        
        :param selection: a slice into the data and flag arrays
        :param maptype: must be one of ['complex','amplitude','phase','power','real','imag']
        :param normalise: If True, the map data will be divided by its absolute maximum value before return
        :param average: str, can be ['antennas', 'channels', 'both']. Takes the average along the 'antennas' or 'channels' axis,  or 'both'. If specified, the corresponding value in 'section' will be ignored.
        :param flag: str, can be ['antennas', 'channels', 'both'].  If taking an average, removes the 'bad_ants' or 'bad_chans' values from the mean.
        
        :return: An instance of BeamMap
        
        """
        if maptype not in MapSet.allowedMapTypes:
            raise ValueError("Invalid map type %s" % maptype)

        x, y, m, mt, f, v = self._get_map(selection, maptype, normalise, average, flag)
        ret = bm.BeamMap(x, y, m, mt, f, v)
        return ret

    def get_map_stokes_i(self, selection, normalise=True):
        """
        Retrieves a single map from the set as a BeamMap object, constructed as Stokes I.
        The polarization portion of the selection is ignored.
        (In future this could be generalized as any linear combination of individual
        polarized images.)
        :param selection: a slice into the data and flag arrays
        :param normalise: If True, the map data will be divided by its absolute maximum value before return

        :return:  An instance of BeamMap as a "pseudo" Stokes I map: the mean of XX and YY power maps
        
        """
        nx, ny = self.xsi.shape[0], self.ysi.shape[0]
        seli1 = {'times': selection[0], 'ant': selection[1], 'beams': selection[2],
                 'chan': selection[4]}
        selv1 = {'pol': ['XX', 'YY']}
        sel1 = self.get_selector(seli1, selv1)
        imap = np.zeros([ny, nx])
        for g1 in sel1:
            xs, ys, m, mt, flg, vec = self._get_map(g1, 'power', normalise)
            imap += m
        vector = [a for a in self.get_vector(selection)]
        vector[3] = 'XX+YY'
        ret = bm.BeamMap(self.xsi, self.ysi, imap / 2.0, 'power', self.flags[selection],
                         vector)
        return ret

    def get_map_stokes(self,
                       selection,
                       stokes="I",
                       normalise=False,
                       average=None,
                       flag=None
                       ):
        """
        Retrieves a single map from the set as a BeamMap object, constructed as a Stokes
        parameter. 
        
        WARNING: Normalisation seems to break things at the moment
        
        Note the difference between ASKAP Stokes definitions and 'standard':
            # 'Standard' Stokes convention
                # I = new_XX + new_YY
                # Q = new_XX - new_YY
                # U = new_XY + new_YX
                # V = -1j * (new_XY - new_YX)

            # ASKAP Stokes convention
                # I_A = new_XX + new_YY
                # Q_A = new_XX - new_YY
                # U_A = new_XY + new_YX
                # V_A = 1j * (new_XY - new_YX)
            This will be in the *antenna* frame, and will need to be rotated to
            the sky frame.
        The polarization portion of the selection is ignored.

        :param selection: A slice into the data and flag arrays
        :param normalise: If True, the map data will be divided by its absolute maximum value
                        before return
        :param average: str, can be ['antennas', 'channels', 'both'].
                        Takes the average along the 'antennas' or 'channels' axis, 
                        or 'both'. If specified, the corresponding value in 'section' will
                        be ignored.
        :param flag: str, can be ['antennas', 'channels', 'both']. 
                    If taking an average, removes the 'bad_ants' or 'bad_chans' values
                    from the mean.
        :return:  An instance of BeamMap as a Stokes map.
        """
        nx, ny = self.xsi.shape[0], self.ysi.shape[0]
        jones = np.zeros([2, 2, ny, nx]) * 1j
        # t0 = time.time()
        xs, ys, m, mt, flg, vec = self._get_map4(selection, 'complex', normalise, average, flag)
        # print("{:f}".format(time.time()-t0), selection)
        for i in range(4):
            idxs = np.unravel_index(i, jones.shape[0:2])
            jones[idxs[0], idxs[1], :, :] = m[i]
        jones_H = np.swapaxes(np.conjugate(jones), 0, 1)
        new_jones = np.einsum('ij...,jk...->ik...', jones, jones_H, optimize=True)
        new_XX = new_jones[0, 0]
        new_XY = new_jones[0, 1]
        new_YX = new_jones[1, 0]
        new_YY = new_jones[1, 1]
        vector = [a for a in self.get_vector(selection)]

        ret = []
        for st in stokes:
            if st == "I":
                stoke_map = new_XX + new_YY
                vector[3] = 'XX+YY'
            elif st == "Q":
                stoke_map = new_XX - new_YY
                vector[3] = 'XX-YY'
            elif st == "U":
                stoke_map = new_XY + new_YX
                vector[3] = 'XY+YX'
            elif st == "V":
                stoke_map = 1j * (new_XY - new_YX)
                vector[3] = 'j(XY-YX)'
            else:
                raise (Exception(f"'{st}' is not a Stokes parameter"))
            st_image = bm.BeamMap(self.xsi,
                                  self.ysi,
                                  np.real(stoke_map),
                                  'power',
                                  self.flags[selection],
                                  vector
                                  )
            ret.append(st_image)

        if len(ret) == 1:
            return ret[0]
        else:
            return ret

    def _get_map(self, selection, maptype, normalise, average=None, flag=None):
        """
        :param selection:
        :param maptype: in ['complex', 'amplitude', 'phase', 'power', 'real', 'imag']
        :param normalise:
        :param average:
        :param flag:
        :return:
        """
        interp = self._interpolate(selection, average, flag)
        if normalise:
            interp /= np.max(np.abs(interp))

        interp_amp = np.abs(interp)
        if 'amplitude' == maptype:
            m = interp_amp
        elif 'phase' == maptype:
            # noinspection PyTypeChecker
            m = np.degrees(np.angle(interp))
        elif 'power' == maptype:
            m = interp_amp ** 2
        elif 'complex' == maptype:
            m = interp
        elif 'real' == maptype:
            m = interp.real
        elif 'imag' == maptype:
            m = interp.imag
        else:
            raise (ValueError, "Unknown map type {}".format(maptype))

        return self.xsi, self.ysi, m, maptype, self.flags[selection], self.get_vector(selection)

    def _get_map4(self, selection, maptype, normalise, average=None, flag=None):
        """
        Return a set of 4 maps, one for each native polarisation.
        :param selection:
        :param maptype: in ['complex', 'amplitude', 'phase', 'power', 'real', 'imag']
        :param normalise:
        :param average:
        :param flag:
        :return:
        """
        interps = []
        sel = list(selection)
        for ipol in [0, 1, 2, 3]:
            sel[3] = ipol
            # sel = selection[:3] + [ipol] + selection[4:]
            interps.append(self._interpolate(tuple(sel), average, flag))

        if normalise:
            beam_pos = self.get_beam_positions()[selection[2]]
            xx_fac = self._interp2D_cmplx(interps[0], beam_pos)
            yy_fac = self._interp2D_cmplx(interps[3], beam_pos)
            xy_fac = np.sqrt(xx_fac * yy_fac)
            scales = [xx_fac, xy_fac, xy_fac, yy_fac]
            # print(scales)
        else:
            scales = [1., 1., 1., 1.]
            # print(scales)
        m = []
        for ipol in [0, 1, 2, 3]:
            interp = interps[ipol] / scales[ipol]
            interp_amp = np.abs(interp)
            if 'amplitude' == maptype:
                m.append(interp_amp)
            elif 'phase' == maptype:
                # noinspection PyTypeChecker
                m.append(np.degrees(np.angle(interp)))
            elif 'power' == maptype:
                m.append(interp_amp ** 2)
            elif 'complex' == maptype:
                m.append(interp)
            elif 'real' == maptype:
                m.append(interp.real)
            elif 'imag' == maptype:
                m.append(interp.imag)
            else:
                raise (ValueError, "Unknown map type {}".format(maptype))

        return self.xsi, self.ysi, m, maptype, self.flags[selection], self.get_vector(selection)

    def _interpolate(self, selection, average=None, flag=None):
        # Interpolate data onto the desired grid. In the case of 1D data
        # where on of xAxis, yAxis has length 1, a 1D array is returned.
        in_xi, in_yi = self.xs, self.ys
        op_xi, op_yi = self.xsi, self.ysi
        if not flag == 'antennas' and not flag == 'channels' and not flag == 'both' and flag is not None:
            raise (Exception(f"'{flag}' is not a possible flag mode."))
        # Grid points that are flagged at observing time can appear as NaN in
        # the array. Replace them with zero.
        if average is None:
            grid = self.data[selection]
        elif average == 'antennas':
            grid = self.data[selection[0],
                   :,
                   selection[2],
                   selection[3],
                   selection[4],
                   ]
            if flag == 'antennas' and self.bad_ants is not None:
                grid = grid[[i for i in range(len(self.axes['antennas'])) if i not in self.bad_ants]]
            grid = np.nanmean(grid, axis=0)
        elif average == 'channels':
            grid = self.data[selection[0],
                   selection[1],
                   selection[2],
                   selection[3],
                   :,
                   ]
            if flag == 'channels' and self.bad_chans is not None:
                grid = grid[[i for i in range(len(self.axes['frequencies'])) if i not in self.bad_ants]]
            grid = np.nanmean(grid, axis=0)
        elif average == 'both':
            grid = self.data[selection[0],
                   :,
                   selection[2],
                   selection[3],
                   :,
                   ]
            if (flag == 'antennas' or flag == 'both') and self.bad_ants is not None:
                grid = grid[[i for i in range(len(self.axes['antennas'])) if i not in self.bad_ants]]
            if (flag == 'channels' or flag == 'both') and self.bad_chans is not None:
                grid = grid[:, [i for i in range(len(self.axes['frequencies'])) if i not in self.bad_chans]]
            grid = np.nanmean(grid, axis=(0, 1))
        else:
            raise (Exception(f"'{average}' is not a possible average mode."))
        cm = np.nan_to_num(grid)

        if self.need_interp:
            if self.is1D:
                if self.nx > 1:
                    fn_real = sp.UnivariateSpline(in_xi, np.real(cm[0, :]), k=2)
                    fn_imag = sp.UnivariateSpline(in_xi, np.imag(cm[0, :]), k=2)
                    interp = fn_real(op_xi) + 1j * fn_imag(op_xi)
                else:
                    fn_real = sp.UnivariateSpline(in_yi, np.real(cm[:, 0]), k=2)
                    fn_imag = sp.UnivariateSpline(in_yi, np.imag(cm[:, ]), k=2)
                    interp = fn_real(op_yi) + 1j * fn_imag(op_yi)

            else:
                # is2D
                # Note that RectBivariateSpline expects the data array to have
                # shape (x.size,y.size). Elsewhere, including matplotlib, shapes of
                # 2D arrays are expected to be (y.size,x.size). Grr.
                fn_real = sp.RectBivariateSpline(in_yi, in_xi, np.real(cm), kx=2, ky=2)
                fn_imag = sp.RectBivariateSpline(in_yi, in_xi, np.imag(cm), kx=2, ky=2)
                interp = fn_real(op_yi, op_xi) + 1j * fn_imag(op_yi, op_xi)
        else:
            interp = cm
        return self._sky_transform(interp)

    def get_badvals(self,
                    which='both',
                    show_plots=True,
                    sigma_chan=3,
                    maxiter_chan=3,
                    sigma_ant=3,
                    maxiter_ant=1,

                    ):
        """
        Get the indices of bad data. Uses the sigma clipping of the RMS across 
        beams along either the antenna or channel axis. Uses the XX polarisation.
        
        :param which: str, can be 'channels', 'antennas', or 'both'
        :param show_plots: if True show plots of the variation in each beam.
        :param sigma_chan: passed on to astropy.stats.sigma_clip
        :param maxiter_chan: passed on to astropy.stats.sigma_clip
        :param sigma_ant: passed on to astropy.stats.sigma_clip
        :param maxiter_ant: passed on to astropy.stats.sigma_clip
        """
        bad_chans, bad_ants = None, None
        data = self.data
        if which == 'channels' or which == 'both':
            # Do the channels first
            chans = np.arange(data.shape[4])
            xdata = data[0, :, :, :, :, :, :]
            tdata = np.nanmean(xdata, axis=0)
            XX = tdata[:, 0, :, :]
            means_chan = np.nanmean(XX, axis=(-2, -1))
            evenly_spaced_interval = np.linspace(0, 1, len(means_chan))
            colors = [plt.cm.rainbow(x) for x in evenly_spaced_interval]
            if show_plots:
                _ = plt.figure(facecolor='w')
                for i, beam in enumerate(means_chan):
                    _ = plt.plot(chans, np.abs(beam), '-', color=colors[i], alpha=0.3, )
                plt.xlabel('Channel')
                plt.ylabel('Abs(XX)')
            means_chan_std = np.nanstd(means_chan, axis=0)
            noise = np.abs(means_chan_std)
            idx = noise == 0
            noise[idx] = np.nan
            filtered_data = sigma_clip(noise, sigma=sigma_chan, maxiters=maxiter_chan, stdfunc=mad_std)
            if show_plots:
                _ = plt.figure(facecolor='w')
                _ = plt.plot(chans, noise, 'k-')
                plt.xlabel('Channel')
                plt.ylabel('Std(Abs(XX))')
                _ = plt.plot(chans[filtered_data.mask], noise[filtered_data.mask], 'X',
                             color='r', label="rejected data")
                _ = plt.legend()

            idx = np.logical_or(idx, filtered_data.mask)
            bad_chans = chans[idx]

        if which == 'antennas' or which == 'both':
            # Do the channels first
            ants = np.arange(data.shape[1])
            xdata = np.nanmean(data[0, :, :, :, :, :, :], axis=3)
            tdata = xdata
            tdata.shape
            XX = tdata[:, :, 0, :, :]
            means_ant = np.nanmean(XX, axis=(-2, -1)).T
            evenly_spaced_interval = np.linspace(0, 1, len(ants))
            colors = [plt.cm.rainbow(x) for x in evenly_spaced_interval]

            if show_plots:
                _ = plt.figure(facecolor='w')
                for i, beam in enumerate(means_ant):
                    _ = plt.plot(ants, np.abs(beam), '-', color=colors[i], alpha=0.3, )
                plt.xlabel('Antenna')
                plt.ylabel('Abs(XX)')
            means_ant_std = np.nanstd(means_ant, axis=0)
            noise = np.abs(means_ant_std)
            idx = noise == 0
            noise[idx] = np.nan
            filtered_data = sigma_clip(noise, sigma=sigma_ant, maxiters=maxiter_ant, stdfunc=mad_std)
            if show_plots:
                _ = plt.figure(facecolor='w')
                _ = plt.plot(ants, noise, 'k-')
                plt.xlabel('Antenna')
                plt.ylabel('Std(Abs(XX))')
                plt.plot(ants[filtered_data.mask], noise[filtered_data.mask], 'X',
                         color='r', label="rejected data")
                _ = plt.legend()
            idx = np.logical_or(idx, filtered_data.mask)
            bad_ants = ants[idx]

        self.bad_chans = bad_chans
        self.bad_ants = bad_ants

    @staticmethod
    def _do_axis(axis, step):
        """
        :param axis:
        :param step:
        :return:
        """
        n = len(axis) / 2
        if n > 0 and step > 0.0:
            a0, a1 = axis[0], axis[-1]
            ai = np.arange(a0, a1 + step / 2, step)
        else:
            ai = axis
        return ai

    @staticmethod
    def _interp2D_cmplx(z, outs):
        """
        :param z     Complex 2D function
        :param ins   X,Y grid ins[N,2] square NxN grid
        :param outs  X,Y grid for evaluation outs[M,2] M ≥ 1
        """
        # Note that RectBivariateSpline expects the data array to have
        # shape (x.size,y.size). Elsewhere, including matplotlib, shapes of
        # 2D arrays are expected to be (y.size,x.size). Grr.
        # D = 5
        # nx, ny = z.shape
        # i, j = int(outs[0]), int(outs[1])
        # i1, i2 = max(0, i - D), min(nx, i+D+1)
        # j1, j2 = max(0, j - D), min(ny, j+D+1)
        # zsub = z[i1:i2,j1:j2]
        inx = range(z.shape[0])
        iny = range(z.shape[1])
        fn_real = sp.RectBivariateSpline(iny, inx, np.real(z), kx=2, ky=2)
        fn_imag = sp.RectBivariateSpline(iny, inx, np.imag(z), kx=2, ky=2)
        interp = fn_real(outs[1], outs[0]) + 1j * fn_imag(outs[1], outs[0])
        return interp

    @staticmethod
    def _sky_transform(data):
        return data[::-1, ::-1].transpose()

    @staticmethod
    def sky_transform_hyper(data):
        return data[:, :, :, :, :, ::-1, ::-1].transpose(0, 1, 2, 3, 4, 6, 5)
