#!/usr/bin/env python3
""" Clean holography data """
import copy
import logging
import os
import string
import sys
from typing import Dict, Any

import numpy as np
import numpy.fft as fft
import pkg_resources
import scipy.interpolate as sp
from astropy.io import fits
from scipy.stats import iqr
from astropy.time import Time


import aces.beamset.beamfactory as bf
from aces import __version__ as aces_version
from aces.askapdata.schedblock import SchedulingBlock
from aces.beamset.beamset import BeamSet
from aces.beamset.mapset import MapSet
from aces.holography import holo_filenames as hf

log = logging.getLogger(__name__)

# Catch annoying warnings
np.seterr(divide="ignore", invalid="ignore")


def tft(t):
    return tuple(t) == (True, False, True)


def report_flags(flags, tag):
    n_payloads = np.product(flags.shape)
    n_set = flags.sum()
    print("{:20s}  {:d} of {:d} flags set".format(tag, n_set, n_payloads))


def robust_poly_fit(spec, poly_ord=2, sigma_lim=0.8, max_iter=20, low_fact=10.):
    """Fit a polynomial to data with outliers

    The test for the presence of outliers is a comparison between standard deviation (std) and
    the inter-quartile range (IQR). The IQR is a robust measure of the distribution width,
    and for a gaussian distribution std/IQR = approx 0.6. The value of std/IQR at which to cease
    the search for outliers is sigma_lim.

    :param spec: Spectrum to fit
    :type spec: np.ndarray
    :param poly_ord: Order of polynomial, defaults to 5
    :type poly_ord: int, optional
    :param sigma_lim: Sigma limit, defaults to 0.8
    :type sigma_lim: float, optional
    :param max_iter: Maxium interations, defaults to 20
    :type max_iter: int, optional
    :return: TODO
    :rtype: TODO
    """
    ss = spec.shape
    if len(ss) == 1:
        n_spec = 1
        spec2 = spec[np.newaxis, :]
    else:
        n_spec = ss[0]
        spec2 = spec

    len_spec = spec2.shape[1]
    x0 = np.arange(len_spec)
    # First estimate the width of the distribution of first differences
    dymc = np.ma.masked_array([])

    for s in range(n_spec):
        y = spec2[s]
        dym = np.ma.masked_invalid(np.diff(y, append=0.0))
        dymc = np.ma.concatenate([dymc, dym])

    iqr_diff = iqr(dymc.compressed())

    # Use this measure for flagging places where first differences are large
    xmc = np.ma.masked_array([])
    ymc = np.ma.masked_array([])
    dymc = np.ma.masked_array([])

    for s in range(n_spec):
        y = spec2[s]
        x = np.ma.masked_array(x0, mask=y.mask)

        dym = np.ma.masked_invalid(np.diff(y, append=0.0))

        dmax = iqr_diff * 2.0
        xm = np.ma.masked_array(x, np.abs(dym) > dmax)
        for i in range(1, len(xm.mask)):
            if tft(xm.mask[i - 1:i + 2]):
                xm.mask[i] = True

        ym = np.ma.masked_array(y, xm.mask)
        xmc = np.ma.concatenate([xmc, xm])
        ymc = np.ma.concatenate([ymc, ym])
        dymc = np.ma.concatenate([dymc, dym])

    plots = []
    resid = []
    fac = low_fact
    result = {'masked_indep': np.ma.masked_array(x0, mask=True, shrink=False)}
    # Hide 'full' parameter; can be unhidden for debugging or analysis of fits
    full = False
    if xmc.count() > poly_ord + 1:
        # start with yu = ymc
        yu = ymc
        qq = np.polyfit(xmc.compressed(), yu.compressed(), poly_ord, full=full)
        if full:
            q, residuals, rank, singular_values, rcond = qq
        else:
            q = qq
            singular_values = None
            residuals = None
        yf = np.polyval(q, xmc)
        for n in range(max_iter):
            yd = ymc - yf
            plots.append(yd)
            iq = iqr(yd.compressed())
            sd = yd.std()
            med = np.ma.median(yd)
            resid.append(iq)
            lower, upper = med - fac * iq, med + fac * iq
            fac = max(1.0, fac * 0.7)
            std_excess = sd / iq
            if std_excess < sigma_lim:
                #                 print('break ',snr)
                break

            condition = np.logical_or(yd < lower, yd > upper)
            ymc = np.ma.masked_where(condition, ymc, copy=False)
            xmc = np.ma.masked_array(xmc, ymc.mask)
            if xmc.count() <= poly_ord:
                break
            q = np.polyfit(xmc.compressed(), ymc.compressed(), poly_ord)
            yf = np.polyval(q, xmc)
        resid = np.array(resid)
        result['masked_indep'] = xmc
        result['masked_input'] = ymc
        result['y_fit'] = np.polyval(q, x0)
        result['resid'] = resid
        result['coeffs'] = q
        if full:
            result['singular_vals'] = singular_values
            result['residuals'] = residuals

    return result


def fit_spec(spec, poly_ord=5, sigma_lim=3.0, max_iter=50):
    """Fit a polynomial to data with outliers

    :param spec: Spectrum to fit
    :type spec: np.ndarray
    :param poly_ord: Order of polynomial, defaults to 5
    :type poly_ord: int, optional
    :param sigma_lim: Sigma limit, defaults to 3.0
    :type sigma_lim: float, optional
    :param max_iter: Maxium interations, defaults to 50
    :type max_iter: int, optional
    :return: TODO
    :rtype: TODO
    """
    y = spec
    ym = np.ma.masked_array(y.copy())

    resid = []
    ims = []
    snrs = []

    x = range(y.shape[0])
    xm = np.ma.masked_array(x, ym.mask)
    if xm.count() > 3:
        q = np.polyfit(xm.compressed(), ym.compressed(), poly_ord)
        yf = np.polyval(q, x)

        for n in range(max_iter):
            yd = ym - yf
            resid.append(yd.std())
            ymax = np.abs(yd).max()
            snr = ymax / yd.std()
            snrs.append(snr)
            if snr < sigma_lim:
                break
            im = np.where(np.abs(yd) == ymax)[0][0]
            ims.append(im)
            ym.mask[im] = True
            xm = np.ma.masked_array(x, ym.mask)
            q = np.polyfit(xm.compressed(), ym.compressed(), poly_ord)
            yf = np.polyval(q, x)
        resid = np.array(resid)
        return y, ym, yf, resid, ims, snrs
    else:
        return y, y, y, resid, ims, snrs


def fit_all_spectra(hm, poly_ord=3):
    """
    Determines the best fitting models and generates that model for a given mean cube
    Args:
        hm ([array]): data cube (masked array)
        poly_ord (int):

    Returns:
        [array]: Returns the best fitting model over all pixels and the associated frequencies.
    """

    ret = np.zeros((hm.shape[0], hm.shape[1], hm.shape[2],
                    hm.shape[3], hm.shape[4]))  # create output array of same dimension as hm cube

    # TODO: Replace these loops - they are inefficient
    for js in range(hm.shape[1]):  # loop over stokes
        log.info(f"Stokes parameter {js+1} of {hm.shape[1]}")
        for jb in range(hm.shape[0]):  # loop over beams
            log.info(f"\tBeam number {jb+1} of {hm.shape[0]}")
            for jx in range(hm.shape[-2]):  # loops over x pixels
                for jy in range(hm.shape[-1]):  # loops over y pixels
                    spec = hm[jb, js, :, jx, jy]  # creates slice of hm cube
                    result = robust_poly_fit(spec, poly_ord=poly_ord)
                    # save out model of slice
                    if 'y_fit' in result:
                        ret[jb, js, :, jx, jy] = result['y_fit']

    return ret


# # # Some (temporary?) routines for interpolation needed for holography sampling-grid error.
def add_metadata_to_header(header: fits.header.Header, metadata: dict[str, Any]) -> None:
    """Common function to add metadata from a MapSet into the FITS header. Some 
    items from the MapSet metadata structure are recorded as a list of values. 
    Here these are handled by taking the first element of the list. 
    
    :param header: The HDU header that is being added to
    :type header: fits.header.Header
    :param metadata: The key-value pair of items to add to header
    :type metadata: dict
    """
    log.info("Adding metadata items to FITS header")
    
    header['ACESVER'] = aces_version
    
    for key, value in metadata.items():
        if key == 'times':
            mjd_time = Time(value[0], format='mjd')
            header['DATE-OBS'] = (f"{mjd_time.isot}", "Time of observing in UTC")
        elif key == 'beamformingSBID':
            header['BFSBID'] = (int(value), "Beamformer weight SBID") 
        elif key == 'holographySBID':
            header['HOLOSBID'] = (int(value), "Holography SBID")
        
        
def write_to_fits(
    data_clean: np.ndarray, mapset: MapSet, interp_factor: float, output_dir: str
):
    """Write data cube to FITS:
    :param data_clean: Cleaned array (with Stokes axis).
    :type data_clean: np.ndarray
    :param mapset: Input holography dataset
    :type mapset: MapSet
    :param interp_factor: Intperpolation grid used in deg
    :type interp_factor: float
    :param output_dir: Directory to save file to
    :type output_dir: str
    """
    freq = mapset.frequencies
    hdu = fits.PrimaryHDU(data_clean.astype(np.float32))
    hdu.header['CTYPE1'] = 'RA---SIN'
    hdu.header['CRVAL1'] = 0.0
    hdu.header['CDELT1'] = -interp_factor
    hdu.header['CRPIX1'] = data_clean.shape[4] // 2 + 1.0

    hdu.header['CTYPE2'] = 'DEC--SIN'
    hdu.header['CRVAL2'] = 0.0
    hdu.header['CDELT2'] = interp_factor
    hdu.header['CRPIX2'] = data_clean.shape[3] // 2 + 1.0

    hdu.header['CTYPE3'] = 'FREQ'
    hdu.header['CRVAL3'] = freq[0] * 1e6
    hdu.header['CDELT3'] = np.diff(freq)[0] * 1e6
    hdu.header['CRPIX3'] = 1.0

    hdu.header['CTYPE4'] = 'STOKES'
    hdu.header['CRPIX4'] = 1.0
    hdu.header['CDELT4'] = 1.0
    hdu.header['CRVAL4'] = 1.0

    hdu.header['CTYPE5'] = 'BEAM'
    hdu.header['CRVAL5'] = 0.0
    hdu.header['CDELT5'] = 1.0
    hdu.header['CRPIX5'] = 1.0

    hdu.header['EQUINOX'] = 2.000000000000E+03
    hdu.header['RADESYS'] = 'FK5     '
    hdu.header['LONPOLE'] = 1.800000000000E+02
    hdu.header['LATPOLE'] = 0.000000000000E+00
    hdu.header['SPECSYS'] = 'TOPOCENT'

    add_metadata_to_header(
        hdu.header, mapset.metadata
    )
    
    log.debug('Output header:')
    log.debug(repr(hdu.header))

    fits_name = f'{output_dir}/{hf.make_file_name(mapset, kind="cube.fits")}'
    log.info(f'Saving to {fits_name}')
    hdu.writeto(fits_name, overwrite=True, output_verify='fix+warn')


def write_tt_to_fits(
    beamtt: np.ndarray, 
    mapset: MapSet, 
    fref: float, 
    bw: float, 
    dxy:float, 
    output_dir: float
):
    """Write Taylor Terms to FITS:
    :param beamtt: Taylor term beams
    :type beamtt: np.ndarray
    :param mapset: Input holography dataset
    :type mapset: MapSet
    :param fref: Reference frequency for Taylor terms
    :type fref: float
    :param bw; The observing bandwidth that is recorded to the header
    :type bw: float
    :param dxy: Interpolation grid in deg
    :type dxy: float
    :param output_dir: Directory to save file to
    :type output_dir: str
    """
    # beamtt axes are: beam, taylor, stokes, freq, dec, ra
    # need to swap to: beam, stokes, taylor, freq, dec, ra for LINMOS
    beamtt = beamtt.swapaxes(1, 2)

    hdu = fits.PrimaryHDU(beamtt.astype(np.float32))
    hdu.header['CTYPE1'] = 'RA---SIN'
    hdu.header['CRVAL1'] = 0.0
    hdu.header['CDELT1'] = -dxy
    hdu.header['CRPIX1'] = beamtt.shape[-1] // 2 + 1.0

    hdu.header['CTYPE2'] = 'DEC--SIN'
    hdu.header['CRVAL2'] = 0.0
    hdu.header['CDELT2'] = dxy
    hdu.header['CRPIX2'] = beamtt.shape[-2] // 2 + 1.0

    hdu.header['CTYPE3'] = 'FREQ'
    hdu.header['CRVAL3'] = fref
    hdu.header['CDELT3'] = bw
    hdu.header['CRPIX3'] = 1.0

    hdu.header['CTYPE4'] = 'TAYLOR'
    hdu.header['CRVAL4'] = 0.0
    hdu.header['CDELT4'] = 1.0
    hdu.header['CRPIX4'] = 1.0

    hdu.header['CTYPE5'] = 'STOKES'
    hdu.header['CRVAL5'] = 1.0  # Start at Stokes I
    hdu.header['CDELT5'] = 1.0  # One Stokes per pixel
    hdu.header['CRPIX5'] = 1.0  # Start at pixel 1 (fortran convention)

    hdu.header['CTYPE6'] = 'BEAM'
    hdu.header['CRVAL6'] = 0.0
    hdu.header['CDELT6'] = 1.0
    hdu.header['CRPIX6'] = 1.0
    hdu.header['EQUINOX'] = 2.000000000000E+03
    hdu.header['RADESYS'] = 'FK5     '
    hdu.header['SPECSYS'] = 'TOPOCENT'
    hdu.header['RESTFRQ'] = fref

    add_metadata_to_header(
        hdu.header, mapset.metadata
    )
    

    log.debug(repr(hdu.header))
    # need to add header items for spatial and spectral axes
    out_name = f'{output_dir}/{hf.make_file_name(mapset, kind="taylor.fits")}'
    hdu.writeto(out_name, overwrite=True, output_verify='fix+warn')


def interp2D_cmplx(z, pixpos, k=2):
    """
    :param z:  (ndarray)     Complex cube of shape Nt,Na,Nb,Np,Nf,nx,ny
    :param pixpos: (ndarray) Array of shape (nbeams,2) giving beam positions in pixels
    :param k: (int)         Order of spline interpolation used.
    :return interp (ndarray) Interpolated values at beam positions - shape Nt,Na,Nb,Np,Nf
    """
    # Note that RectBivariateSpline expects the data array to have
    # shape (x.size,y.size). Elsewhere, including matplotlib, shapes of
    # 2D arrays are expected to be (y.size,x.size). Grr.

    nt, na, nb, nq, nf, nx, ny = z.shape
    newshape = [nt * na * nb * nq * nf, nx, ny]
    t = np.reshape(z, newshape)
    outr = pixpos[:, np.newaxis, :]
    outr = np.repeat(outr, nq * nf, axis=1)[np.newaxis]
    outr = np.repeat(outr, na, axis=0).reshape([nt * na * nb * nq * nf, 2])
    inx = range(nx)
    iny = range(ny)
    fn_real = [sp.RectBivariateSpline(
        iny, inx, np.real(zi), kx=k, ky=k) for zi in t]
    fn_imag = [sp.RectBivariateSpline(
        iny, inx, np.imag(zi), kx=k, ky=k) for zi in t]
    interp = np.array([fri(out[1], out[0]) + 1j * fii(out[1], out[0])
                       for fri, fii, out in zip(fn_real, fn_imag, outr)])
    return interp.reshape([nt, na, nb, nq, nf])


def normalise(v, bpos, refant):
    """
    Given an array of raw holography visibilities v, normalise to give
    the response of each antenna relative to its response to a point source
    at beam centre.  Each map value at beam centre is determined by
    interpolation: vxx0, vyy0. The normalised quantities are computed as
    Nxx = vxx/vxx0, Nxy = vxy/vxx0, Nyx = vyx/vyy0, Nyy = vyy/vyy0
    :param v:(numpy.ndarray) visibilities
    :param bpos: (np.ndarray) beam position in pixels (nb,2)
    :param refant: (int) Reference antenna number (0 based)
    :return N: (numpy.ndarray) normalised visibilities

    NOTE: This scheme works provided the reference antenna has a lower index than all target antennas
    For cases where the correlation is Target * Reference we need:
    scale_xy = scale_yy
    scale_yx = scale_xx
    """
    vxx = v[:, :, :, :1, :, :, :]
    vxx0 = interp2D_cmplx(vxx, bpos)
    vyy = v[:, :, :, -1:, :, :, :]
    vyy0 = interp2D_cmplx(vyy, bpos)

    vxy0 = vxx0
    vyx0 = vyy0
    scales = 1.0 / np.concatenate((vxx0, vxy0, vyx0, vyy0), axis=3)
    if refant > 0:
        sh = list(scales.shape)
        sh1 = sh[:3] + [2, 2] + sh[4:]
        scales = scales.reshape(sh1)
        scales[:, :refant] = np.einsum('ijkmln', scales[:, :refant])
        scales = scales.reshape(sh)

    log.info("Scales found")

    N = np.einsum('ijklmno,ijklm->ijklmno', v, scales)
    return N


def volt_to_power(v):
    """
    Given a Jones matrix v, return the corresponding brightness
    matrix b as
    b = v * v(h) where (h) is the hermitian transpose.
    In both v and b, the polarisation axis is the 4th of 7 axes:
    sh = (nt,ne,nb,4,nf,nx,ny)
    :param v: (numpy.ndarray) voltage vector of shape sh
    :return b: (numpy.ndarray) brightness vector of shape sh
    """
    sh = list(v.shape)
    new_shape = sh[:3] + [2, 2] + sh[4:]
    J = np.reshape(v, new_shape)
    # produce the hermitian
    JH = np.conjugate(J).transpose((0, 1, 2, 4, 3, 5, 6, 7))

    b = np.einsum('tabij...,tabjk...->tabik...', J, JH)
    b = np.reshape(b, sh)
    return b


def feed_to_stokes(f):
    """
    Given a matrix (voltage or power) in the feed frame, return the corresponding
    Stokes matrix. Do this for ASKAP, assuming the measurements were made with the
    antenna rotated +45 degrees.
    In both f and s, the polarisation axis is the 4th of 7 axes:
    sh = (nt,ne,nb,4,nf,nx,ny)
    :param f: (numpy.ndarray) vector in feed frame: XX,XY,YX,YY
    :return s:  (numpy.ndarray) vector in Stokes frame: I,Q,U,V
    """
    i = 0 + 1j

    # Referring to ASKAP Science Observation Guide (Appendix C) that sets out the
    # Mueller matrix for ASKAP with its X-Y probes rotated 45 degrees:
    #     T = np.array([[1, 0, 0, 1], [s, c, c, -s],[-c, s, s, c], [0, -i, i, 0]])
    #   where s = sin(2*PA), c = cos(2*PA)
    #
    # for PA = -45deg (used in the holography observations)

    T = np.array([[1, 0, 0, 1], [-1, 0, 0, 1], [0, -1, -1, 0], [0, -i, i, 0]])
    s = np.real(np.einsum('ji,tabi...->tabj...', T, f))
    return s


def raw_to_stokes(raw_file_name, refant):
    """
    Reads holography data in hdf5 MapSet format. Performs operations on the
    data hyper-cube:
    * transforms to axes aligned with celestial coords
    * determines map values at beam positions in Vxx, Vyy
    * derives normalising factors for Vxx, Vxy, Vyx, Vyy visibilities
    * normalises the complex data
    * determines brightness vector XX, XY, YX, YY
    * converts to Stokes I Q U V
    * saves both Stokes vector and scale values in hdf5 MapSet format
    
    :param raw_file_name: (str) Name of hdf5 holography data file
    :param refant: (int) Reference antenna
    :return stokes_obj (MapSet) Holography maps, normalised and in Stokes brightness I Q U V
    :return centre_obj (MapSet) Normalising scales - visibilities at beam positions (interpolated).

    """
    # Load holography data: mapset.data in ndarray
    mso = bf.load_beamset_class(raw_file_name)

    log.info("Got data")

    # SKY_TRANSFORM - products are XX,XY,YX,YY
    products = MapSet.sky_transform_hyper(mso.data)
    log.info("Transformed")

    # beam positions
    pixoff = mso.get_beam_positions()
    prod_norm = normalise(products, pixoff, refant)
    log.info("Normalised")

    # We now have (assuming a good model for the reference source), the polarised response to a source
    # with I,Q,U,V = 1,0,0,0 in the complex correlator products Vxx, Vxy, Vyx, Vyy (a Jones matrix)
    # Now convert to brightness matrix Bxy
    Bxy = volt_to_power(prod_norm)

    # and form the stokes brightness vector Bstokes
    Bstokes = feed_to_stokes(Bxy)

    log.info("Stokes formed")

    md = copy.deepcopy(mso.metadata)
    md['polarizations'] = ['I', 'Q', 'U', 'V']
    # md['payloadshape'] = stokes_cube[0, 0, 0, 0, 0].shape

    n_data = MapSet.sky_transform_hyper(Bstokes)
    n_flags = np.zeros(Bstokes.shape[:-2], dtype=int)
    log.debug(f'n flags sum {n_flags.sum()}')

    mso_stokes = MapSet(metadata=md,
                        data=n_data,
                        flags=n_flags,
                        filename=None
                        )
    mso_stokes.add_to_history('Normalised, converted to Stokes')

    return mso_stokes


def get_quality_flags(mapset, amp_max=1.4):
    """
    Take MapSet object holding Holography power patterns in the IQUV
    Stokes parameters;
    look for and flag image planes whose maximum stokes I value significantly exceeds the expected value
    of 2.0.

    Typically, the large value flags arise from planes that were effected by RFI and produce large
    values at random locations away from the beam peak:
    :param mapset: MapSet object holding cube of beam images
    :type mapset: aces.beamset.mapset.MapSet
    :param amp_max: Maximum allowed amplitude
    :type amp_max: float, optional
    :return: result - a dict holding flags and correspondingly masked data
    :rtype: dict
    """
    data = MapSet.sky_transform_hyper(mapset.data)
    flags = (np.array(mapset.flags)).astype(bool)
    report_flags(flags, 'in get_quality_flags')
    if flags.all():
        log.warning('All flags are True - this is not expected. Setting all flags to False')
        flags = np.zeros(flags.shape, dtype=bool)

    nt, na, nb, nq, nf = flags.shape
    nx = data.shape[5]

    # Form a masked version of the data using the flags derived earlier
    # the flags array from MapSet object are given two additional axes to
    # allow the construction of a masked array from the data.
    a = np.repeat(flags[:, :, :, :, :, np.newaxis], nx, axis=-1)
    flg = np.repeat(a[:, :, :, :, :, :, np.newaxis], nx, axis=-1)
    fdata = np.ma.masked_array(data, mask=flg)

    #  First flag image planes with an unrealistic maximum in Stokes I
    fmax = fdata[0, :, :, 0, :].max(axis=3).max(axis=3)
    # Factor of 2 required because we have normalised XX and YY and formed sum.
    mk_max = fmax > 2.0 * amp_max
    # and remask data buffer
    a = np.repeat(mk_max[:, :, np.newaxis, :], nq, axis=2)

    flags[0] = np.logical_or(flags[0], np.array(a))
    a = np.repeat(flags[:, :, :, :, :, np.newaxis], nx, axis=-1)
    flg = np.repeat(a[:, :, :, :, :, :, np.newaxis], nx, axis=-1)
    fdata = np.ma.masked_invalid(np.ma.masked_array(data, mask=flg))

    result = {'flags': flags, 'masked_data': fdata}
    return result


def form_mean(mapset):
    """
    Take MapSet object holding Holography power patterns in the IQUV
    Stokes parameters;
    Compute the mean over the antenna axis for all beams, polarisations and spectral points
    using the MapSet flags to include only image planes judged to be of high quality:
    :param mapset: Object holding cube of beam images
    :type mapset: aces.beamset.mapset.MapSet
    :return: mean_cube: Mean cube of shape [nB, nP, nF, nx, ny]
    :rtype: numpy.ndarray
    """
    data = MapSet.sky_transform_hyper(mapset.data)
    flags = (np.array(mapset.flags)).astype(bool)
    nx = data.shape[5]
    msk = np.repeat(flags, nx * nx).reshape(data.shape)
    fdata = np.ma.masked_array(data, msk)
    mean_cube = fdata[0].mean(axis=0)

    # Scale the data so that at beam centre, XX + YY = 1.0
    return mean_cube * 0.5


def save_mean(mean_cube, mapset, out_name):
    """
    Takes the array-wide mean cube and writes it to an hdf5 file in the BeamSet format
    :param mean_cube: Data cube of shape (nb, npol, nf, nx, ny)
    :param mapset:  BeamSet object from full Stokes cube; used to derive new metadata for output
    :param out_name: Name of output file
    :type out_name: str
    :return:
    """
    in_shape = mean_cube.shape
    out_shape = [1, 1] + list(in_shape)
    mdc = copy.deepcopy(mapset.metadata)
    mdc['antennas'] = [0]
    p_data = np.zeros(out_shape, dtype=float)
    p_data[0, 0] = mean_cube.data
    p_data = MapSet.sky_transform_hyper(p_data)
    p_flags = np.zeros(out_shape[:-2], dtype=bool)
    if isinstance(mean_cube, np.ma.core.MaskedArray):
        p_flags[0, 0] = mean_cube.mask.all(axis=(-2, -1))
    mso_mean = MapSet(metadata=mdc,
                      data=p_data,
                      flags=p_flags,
                      filename=None
                      )
    mso_mean.add_to_history('mean obj made')
    mso_mean.write_to_hdf5(out_name)


def centre_beams(mean_cube, mapset, kxy=5, nxy=101):
    """Takes the mean holography cube (averaged over antennas) and
    interpolates each beam onto a grid centred on its nominal position
    and with the given grid spacing

    :param mean_cube: shape Nb,Np,Nf,Nx,Ny
    :type mean_cube: np.ndarray
    :param mapset: parent object - for metadata
    :type mapset: [type]
    :param kxy: Degrees of bivariate spline used in RecBivariateSpline, defaults to 5
    :type kxy: int, optional
    :param nxy: Size of output grid (must be odd integer)., defaults to 101
    :type nxy: int, optional
    :return: TODO
    :rtype: TODO
    """
    big = 100.

    pixpos = mapset.get_beam_positions()
    # Determine size from minimum position to edge distance
    nb = mapset.Nb
    xstep = mapset.xs[1] - mapset.xs[0]

    x0, y0 = 0, 0
    x1, y1 = mapset.metadata['payloadshape']
    minx, miny = big, big
    for ib in range(nb):
        px, py = pixpos[ib]
        minx = min(minx, abs(px - x0), abs(px - x1))
        miny = min(miny, abs(py - y0), abs(py - y1))
    semi_size = min(minx, miny)

    nxy_out = nxy
    xh = np.linspace(pixpos[:, 0] - semi_size,
                     pixpos[:, 0] + semi_size, nxy_out)
    yh = np.linspace(pixpos[:, 1] - semi_size,
                     pixpos[:, 1] + semi_size, nxy_out)

    nb, nq, nf, nx, ny = mean_cube.shape
    # Change shape from beams x pols x channels to channels x pols x beams
    work = mean_cube.transpose((2, 1, 0, 3, 4))
    work = np.reshape(work, [nq * nf, nb, nx, ny])

    inx = range(nx)
    iny = range(ny)
    res = []
    for ib in range(nb):
        xy = np.array([xh[:, ib], yh[:, ib]])
        outr = xy
        fn = [sp.RectBivariateSpline(iny, inx, w, kx=kxy, ky=kxy)
              for w in work[:, ib]]
        interp = np.array([fni(outr[1], outr[0]) for fni in fn])
        res.append(interp)
    # Set result shape to be beams x channels x pols
    res = np.array(res).reshape((nb, nf, nq, nxy_out, nxy_out))
    res = np.array(res)

    dxy = np.degrees((xh[1] - xh[0]) * xstep)
    return res, dxy[0]


def tt(fstart, beam_cube, nterm):
    """For correction of continuum images we turn the frequency axis
    into a taylor term axis.

     - Note this requires picking a centre frequency f0, for which the
     Taylor coefficients are computed

    :param fstart: Starting frequency in MHz
    :type fstart: float
    :param beam_cube: Beam maps, averaged over antennas
    :type beam_cube: np.ndarray
    :param nterm: Number of Taylor terms
    :type nterm: int
    :return: TODO
    :rtype: TODO
    """
    nb, nstokes, nchan, nx, ny = beam_cube.shape

    # Assuming 1MHz channels
    chanw = 1.e6
    fend = fstart + (nchan - 1) * chanw
    f0 = (fstart + fend) / 2
    f = np.arange(fstart, fend + chanw / 10, chanw)
    bw = fend - fstart

    # frequency weights
    w = (f - f0) / f0
    wv = np.array([w / w, w, w * w][:nterm])

    # Hessian
    H = np.zeros((nterm, nterm))
    for i in range(nterm):
        for j in range(nterm):
            H[i, j] = np.sum(w ** (i + j))

    # Inverse hessian
    Hinv = np.linalg.inv(H)

    #              t  -1 t
    # Calculating (A A)  A b, with A = frequency weights vector
    speclist = []
    pblist = []
    for s in range(nstokes):
        b = np.tensordot(wv, beam_cube[:, s], axes=([1], [1]))
        pbt = np.tensordot(Hinv, b, axes=([1], [0]))
        pbt = pbt.swapaxes(0, 1)
        pblist.append(pbt)

        # evaluate terms
        ttspectra = np.tensordot(pbt, wv, axes=([1], [0]))
        ttspectra = np.moveaxis(ttspectra, -1, 1)
        speclist.append(ttspectra)

    # Stack the taylor terms
    pbcube = np.stack(pblist, axis=2)
    tt_cube = np.stack(speclist, axis=2)

    # Axes are: beam, taylor, stokes, freq, dec, ra
    # Add empty axis for dummy frequency
    pbcube = np.expand_dims(pbcube, axis=3)
    tt_cube = np.expand_dims(tt_cube, axis=3)

    return pbcube, tt_cube, f0, bw


class BeamModel(object):
    """
    Class - to be improved 1. hold data in hdf5 file, not pickle.
    """

    def __init__(self, bs_obj):
        pkg = self._radial_gau_gen()
        xk, ref_freq, model, fn = pkg
        self.xs = xk
        xax = np.degrees(bs_obj.metadata['xAxis'])
        self.nperside = len(xax)
        self.centre = (self.nperside - 1) / 2.0
        self.delta_x = xax[1] - xax[0]
        self.edge = xax[-1]
        self.ref_freq = ref_freq
        self.model = model
        self.bv_func = fn

    def get(self, pixoff, freq):
        """TODO

        :param pixoff: TODO
        :type pixoff: TODO
        :param freq: TODO
        :type freq: TODO
        :return: TODO
        :rtype: TODO
        """
        px, py = self.delta_x * (pixoff - self.centre) * freq / self.ref_freq
        end = self.edge * freq / self.ref_freq
        xm = np.linspace(-end - px, end - px, self.nperside)
        ym = np.linspace(-end - py, end - py, self.nperside)
        return self.bv_func(ym, xm)

    @staticmethod
    def _radial_gau_gen():
        """
        Parameters used here were derived from a 'good set' of mid-band beams (SBID=16881),
        the Gaussian parameter (0.6945) minimises the difference between model gaussian and measured
        average beam shape at 1438.5 MHz.
        """
        ref_freq = 1438.5
        xg = np.linspace(-4.2, 4.2, 211)
        yg = xg
        xh, yh = np.meshgrid(xg, yg)
        rh = np.sqrt(xh ** 2 + yh ** 2)

        ga = np.exp(-(rh / 0.6945) ** 2) * 2
        fn2 = sp.RectBivariateSpline(xg, yg, ga, kx=2, ky=2)
        pkg2 = (xg, ref_freq, ga, fn2)
        return pkg2


def get_beampos_errs(mapset, bmodel):
    """TODO

    :param mapset: TODO
    :type mapset: TODO
    :param bmodel: TODO
    :type bmodel: TODO
    :return: TODO
    :rtype: TODO
    """
    na, nb, nf = mapset.Na, mapset.Nb, mapset.Nf
    shiftss = np.ones((na, nb, nf, 2))
    resid = np.zeros([na, nb, nf])
    amps = np.zeros([na, nb, nf])
    pixoff = mapset.get_beam_positions()
    cube_s = MapSet.sky_transform_hyper(mapset.data)[0]
    flags = mapset.flags[0]
    ants = range(na)
    for chan in range(nf):
        for beam in range(nb):
            ref = bmodel.get(pixoff[beam], mapset.frequencies[chan])
            for ant in ants:
                if flags[ant, beam, 0, chan]:
                    shiftss[ant, beam, chan] = [np.nan, np.nan]
                    resid[ant, beam, chan] = np.nan
                else:
                    refa = np.abs(cube_s[ant, beam, 0, chan])
                    gs_ret = get_shift(mapset, ref, refa, frac=0.25)
                    shiftss[ant, beam, chan] = gs_ret['shift']
                    amps[ant, beam, chan] = gs_ret['amp_ratio']
                    result = gs_ret['result']

                    if len(result[1]) == 0:
                        resid[ant, beam, chan] = np.nan
                    else:
                        resid[ant, beam, chan] = result[1][0] / result[4]
    return shiftss, resid, amps


def get_shift(mapset, ref_im, target_im, frac=0.25):
    """Compute the shift of target_im relative to ref_im.
    Use Fourier shift theorem
    The sense of the returned shifts:
    If the returned value shift = (dl, dm), and if the position of reference and target
    beams are (lr, mr) and (lt, mt) respectively, then dl > 0.0 indicates lt > lr
    and if dm > 0.0 then tm > rm. Coordinate $l$ increases towards the west; $m$ increases towards the north.

    :param mapset: Primary mapset
    :type mapset: [type]
    :param ref_im: Reference image ndim=2
    :type ref_im: np.ndarray
    :param target_im: Target image
    :type target_im: np.ndarray
    :param frac: Mask transform values < ampMax * frac in phase fit, defaults to 0.25
    :type frac: float, optional
    :return: TODO
    :rtype: TODO
    """
    n = ref_im.shape[0]
    n2 = n // 2
    f = fft.fftshift(fft.fft2(ref_im))
    fa = fft.fftshift(fft.fft2(target_im))

    zf = np.angle(fa / f).flatten()
    amp = np.abs(fa)
    clip = amp.max() * frac
    zm = np.ma.masked_array(zf, amp < clip)
    x = np.arange(0, n, 1) - n2
    y = np.arange(0, n, 1) - n2
    xg, yg = np.meshgrid(x, y)
    xf = xg.flatten()
    yf = yg.flatten()
    zf = zm[~zm.mask]
    xf = xf[~zm.mask]
    yf = yf[~zm.mask]
    zf = np.expand_dims(zf, 1)
    npts = zf.shape[0]

    A = np.c_[xf, yf]
    result = np.linalg.lstsq(A, zf, rcond=None)
    coeff, r, rank, s = result
    result_ret = result + (npts,)
    xs = mapset.metadata['xAxis']
    span = xs[-1] - xs[0]
    shift = -1.0 * coeff[:, 0] / (2.0 * np.pi) * span

    if len(r) > 0:
        qual = np.ma.masked_array(np.abs(fa / f), amp < clip).mean()
    else:
        qual = np.nan
    result = {'shift': shift,
              'result': result_ret,
              'G': f,
              'H': fa,
              'amp_ratio': qual}
    return result


def centre_mass(im, xaxis):
    xg, yg = np.meshgrid(xaxis, xaxis)
    imx = im * xg
    imy = im * yg
    sh = np.array([imx.sum() / im.sum(), imy.sum() / im.sum()])
    return sh


def get_beampos_errs_from_fits(fits_header, fits_data):
    fh = fits_header
    fd = fits_data
    na, nb, nf = 1, fd.shape[0], 1
    shiftss = np.ones((na, nb, nf, 2))
    resid = np.zeros([na, nb, nf])
    amps = np.zeros([na, nb, nf])
    dx = fh['CDELT2']
    xax = (np.arange(0.0, 101., 1.0) - (fh['CRPIX1'] - 1.0)) * dx

    cube_s = np.expand_dims(fd, axis=0)
    ants = range(na)
    for chan in range(nf):
        for beam in range(nb):
            for ant in ants:
                refa = np.abs(cube_s[ant, beam, chan])
                sh = centre_mass(refa, xax)
                shiftss[ant, beam, chan] = np.radians(sh)
    return shiftss, resid, amps


def shifts_to_mapset(mapset, shifts, resids, amps):
    """
    Package the beam shift data into a Mapset object
    :param mapset: Input mapset object, holdng the holography maps
    :param shifts: Stokes I beam position offsets
    :param resids: Residuals to offset fit
    :param amps:
    :return: Mapset object holdong shift data
    """
    mds = copy.deepcopy(mapset.metadata)
    mds['polarizations'] = ['I']
    mds['payloadshape'] = (4,)
    mds['xAxis'] = [0.0]
    mds['yAxis'] = [0.0]
    sdata = np.zeros([1, mapset.Na, mapset.Nb, 1, mapset.Nf, 4])
    sdata[0, :, :, 0, :, :2] = shifts
    sdata[0, :, :, 0, :, 2] = resids
    sdata[0, :, :, 0, :, 3] = amps

    sflags = np.array(mapset.flags)

    bso_shift = BeamSet(metadata=mds,
                        data=sdata,
                        flags=sflags,
                        filename=None
                        )
    bso_shift.add_to_history('Beam position errs, resid, amps')
    return bso_shift


def save_shifts(beamset, holo_dir):
    """
    Save a BeamSet object holding beam errors to an hdf5 file:
    :param beamset: BeamSet object holding beam pos errors
    :type beamset: BeamSet
    :param holo_dir: Directory to receive hdf5 file
    :type holo_dir: str
    """
    outnam = f'{holo_dir}/{hf.make_file_name(beamset, "beam_shifts.hdf5")}'
    print('Save shifts to {}'.format(outnam))
    beamset.write_to_hdf5(outnam)


def design_mat(x, op):
    N = len(x)
    M = op
    a = np.zeros([N, M])
    for j in range(op):
        a[:, M - 1 - j] = x ** j
    return a


def pfit(x, y, op):
    a = design_mat(x, op + 1)
    yc = y.filled(fill_value=0.0)
    am = a.copy()
    am[y.mask] = 0.0
    coeff, r, rank, s = np.linalg.lstsq(am, yc, rcond=None)
    return coeff, r, a


def get_posfit_flags(resid, amps, res_limits, amp_limits):
    """TODO

    :param resid: TODO
    :type resid: TODO
    :param amps: TODO
    :type amps: TODO
    :return: n_flags New flags of shape to match obj.flags; True for bad data
    :rtype: TODO
    """

    na, nb, nf = resid.shape
    xs = np.arange(0, nf, 1.0)
    coeffs, upper = res_limits

    poly_order = coeffs.shape[0]
    A = design_mat(xs, poly_order)
    base = np.dot(A, coeffs).T
    upper_div = upper[:, None] / base
    resid_div = np.ma.masked_invalid(resid / base[None, :, :]).filled(fill_value=-1.0)
    compr = np.logical_or(resid_div > 1.0 + upper_div[None, :, :], resid_div < 0.0)

    amp_lo, amp_hi = amp_limits
    compa = np.logical_or(amps < amp_lo, amps > amp_hi)
    comp = np.logical_or(compr, compa)
    # print('compr sum ', compr.sum())
    # print('compa sum ', compa.sum())
    # print('comp  sum ', comp.sum())
    n_flags = np.repeat(comp[:, :, None, :], 4, axis=2)
    # print('n_flags  sum ', n_flags.sum())
    return n_flags[np.newaxis]


def set_resid_lim(resids, order=2, iqr_fac=2.0):
    # Look at statistics to guess a fair limit above which to flag.
    # Do this separately for each beam
    # At some frequencies, the shift residuals are quite beam and frequency
    # dependent. The current (new as of 2022June) approach is to fit a low-order
    # polynomial to the array-wide spectrum for each beam, robustly, excluding outliers.
    # This routine returns, for each beam, coefficients and lower and upper increments:
    # the intention is that, for any antenna,beam spectrum of residuals, points outside
    # the range [poly-lower,poly+upper] should be flagged.

    na, nb, nf = resids.shape
    coeffs = np.zeros([order + 1, nb])
    upper = np.zeros(nb)

    for beam in range(nb):
        ys = np.ma.masked_invalid(resids[:, beam])

        rpf = robust_poly_fit(ys, poly_ord=order, sigma_lim=0.8, max_iter=17)

        ymsk = rpf['masked_input']
        yfit = rpf['y_fit']
        yres = rpf['resid']
        coeff = rpf['coeffs']
        coeffs[:, beam] = coeff
        upper[beam] = rpf['resid'][-1] * iqr_fac
    return coeffs, upper


def get_shift_flags(shifts, shift_fit_flags):
    """TODO

    :param shifts:
    :param shift_fit_flags:
    :return: n_flags New flags of shape to match obj.flags; True for bad data
    :rtype: TODO
    """
    abshifts = np.ma.masked_array(np.sqrt(shifts[:, :, :, 0] ** 2 + shifts[:, :, :, 1] ** 2),
                                  mask=shift_fit_flags[0, :, :, 0])
    na, nb, nf = abshifts.shape
    flagged = np.ones([na, nb, nf], dtype=bool)
    for a in range(na):
        for b in range(nb):
            spec = abshifts[a, b]
            if spec.count() > 0:
                spf = robust_poly_fit(spec, poly_ord=3)

                flagged[a, b] = spf['masked_indep'].mask
    n_flags = np.repeat(flagged[:, :, None, :], 4, axis=2)
    return n_flags[np.newaxis]


def main(sbid,
         holo_dir='.',
         remake_stokes=False,
         max_order=5,
         param='BIC',
         max_iter=50,
         snr_limit=3):
    """Main script
    :param sbid: SBID
    :type sbid: int
    :param holo_dir: Directory containing holo data, defaults to '.'
    :type holo_dir: str, optional
    :param remake_stokes: Remake Stokes parameters, defaults to False
    :type remake_stokes: bool, optional
    :param max_order: Maximum polynomial to fit, defaults to 5
    :type max_order: int, optional
    :param param: Criterion to evaluate fit, defaults to 'BIC'
    :type param: str, optional
    :param max_iter: Maximum interations for fitting, defaults to 50
    :type max_iter: int, optional
    :param snr_limit: SNR limit for fitting, defaults to 3
    :type snr_limit: int, optional
    """
    # Stage 1:
    # Raw holography visibility data to Stokes hypercube and Scales data (both in MapSet format)
    # Either construct the Stokes cube, or read it from a previous determination.

    # Clean up dir
    if holo_dir[-1] == '/':
        holo_dir = holo_dir[:-1]

    try:
        sb = SchedulingBlock(sbid)
        myRA = int(''.join(filter(lambda char: char in string.digits,
                                  sb.get_parameters()['holography.ref_antenna'])))
    except:
        myRA = 1
    refant = myRA - 1  # 0-based

    if remake_stokes:
        # Construct Stokes cube from raw holography data
        in_name_g = hf.find_holo_file(holo_dir, pol='xxyy', sbid=sbid, kind='grid.hdf5')
        if in_name_g is not None:
            in_name = in_name_g
            log.info("Using regridded data : {}".format(in_name_g))
        else:
            log.warning("No regridded data found : {}".format(in_name_g))
            in_name = hf.find_holo_file(holo_dir, pol='xxyy', sbid=sbid, kind='hdf5')
        mso_stokes = raw_to_stokes(in_name, refant)
        report_flags(mso_stokes.flags, 'raw to stokes')

        # Estimate, from Stokes I images, the beam positions relative to nominal
        model_file = pkg_resources.resource_filename("aces.holography", "mean_beam_model.pkl")
        if os.path.exists(model_file):
            bmodel = BeamModel(mso_stokes)
            qf = get_quality_flags(mso_stokes)
            quality_flags = qf['flags']
            report_flags(quality_flags, 'get_quality_flags')

            log.debug(quality_flags.shape, np.product(quality_flags.shape), quality_flags.sum())
            if quality_flags.all():
                log.warning('All quality flags are True - this is not expected! Not updating flags.')
            else:
                mso_stokes.flags = quality_flags
                mso_stokes.add_to_history('Flags updated')

            shifts, resids, amps = get_beampos_errs(mso_stokes, bmodel)
            bso_shift = shifts_to_mapset(mso_stokes, shifts, resids, amps)
            save_shifts(bso_shift, holo_dir)
            res_lims = set_resid_lim(resids, order=3, iqr_fac=3.0)
            amp_lims = [0.8, 1.25]
            shift_fit_flags = get_posfit_flags(resids, amps, res_lims, amp_lims)
            report_flags(shift_fit_flags, 'after posfit flags')
            shift_flags = get_shift_flags(shifts, shift_fit_flags)
            report_flags(shift_flags, 'after get shift flags')

            log.debug(f'new_flags sum {shift_flags.sum()}')
            if shift_flags.all():
                log.warning('All shift flags are True - this is not expected! Not updating flags.')
            else:
                mso_stokes.flags = shift_flags
                mso_stokes.add_to_history('Flags updated')

            log.info("Shifts and flags done")
        else:
            log.warning("No beam model file found {}".format(model_file))

        report_flags(mso_stokes.flags, 'on writing')
        out_name = f'{holo_dir}/{hf.make_file_name(mso_stokes, kind="stokes.hdf5")}'
        mso_stokes.write_to_hdf5(out_name)

    else:
        # Read the Stokes cube from hdf5 file
        in_name = hf.find_holo_file(holo_dir, pol='iquv', sbid=sbid, kind='hdf5')
        # Load holography data: obj.data in ndarray
        mso_stokes = bf.load_beamset_class(in_name)

    # Stage 2:
    # prepare_mean: find good/bad antennas, form mean over good.
    # Interpolate spectra over bad channels
    # Shift each beam image to the centre of its grid, and write FITS file for LINMOS.

    mean_cube = form_mean(mso_stokes)
    log.info("Mean prepared")

    mean_name = f'{holo_dir}/{hf.make_file_name(mso_stokes, kind="mean.hdf5")}'
    save_mean(mean_cube, mso_stokes, mean_name)

    mean_cube_interp = fit_all_spectra(mean_cube, poly_ord=max_order)

    mean_name_int = f'{holo_dir}/{hf.make_file_name(mso_stokes, kind="mean_interp.hdf5")}'
    save_mean(mean_cube_interp, mso_stokes, mean_name_int)

    log.info("Spectral interpolation done")

    kxy = 5
    res, dxy = centre_beams(mean_cube_interp, mso_stokes, kxy=kxy)

    log.info("Beams centred")

    res = res.transpose((0, 2, 1, 3, 4))

    # Correct for Stokes I falloff
    i_res = res[:, 0]

    res[:, 1:] /= i_res[:, np.newaxis]
    log.info("QUV divided by I")

    write_to_fits(
        res,
        mso_stokes,
        dxy,
        holo_dir,
    )

    # Finally, produce a Taylor Term cube
    nterm = 3
    fstart = mso_stokes.frequencies[0] * 1.0e6
    (beamtt, beamcubefit, f0, bw) = tt(fstart, res, nterm)

    write_tt_to_fits(beamtt, mso_stokes, f0, bw, dxy, holo_dir)

    log.info("All finished")


def cli():
    import argparse
    """
    Command line interface
    """

    # Help string to be shown using the -h option
    descStr = """
    Clean holography data (2022Aug10)
    """

    epilog_text = """

    """

    # Parse the command line options
    parser = argparse.ArgumentParser(description=descStr,
                                     epilog=epilog_text,
                                     formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument(
        'sbid',
        metavar='sbid',
        type=int,
        help='SBID of processed holography (stored in HDF5) [no default].')

    parser.add_argument(
        '-d',
        dest='holo_dir',
        type=str,
        default='.',
        help='Directory containing holography data [./].')

    parser.add_argument(
        "-r",
        dest="remake_stokes",
        action="store_true",
        help="Remake averaged Stokes cube [False]."
    )

    parser.add_argument(
        "--snr_limit",
        type=float,
        default=3,
        help="SNR clipping level on model fitting [3]."
    )

    parser.add_argument(
        "--max_order",
        type=int,
        default=5,
        help="Maximum polymomial to fit to spectra [5]."
    )

    parser.add_argument(
        "--param",
        type=str,
        choices=['AIC', 'BIC'],
        default='BIC',
        help="How to evaluation fits [BIC]."
    )

    parser.add_argument(
        "-v",
        "--verbosity",
        action="count",
        help="Increase output verbosity",
        default=0
    )

    args = parser.parse_args()
    if args.verbosity == 1:
        log.basicConfig(
            level=log.INFO,
            format="%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    elif args.verbosity >= 2:
        log.basicConfig(
            level=log.DEBUG,
            format="%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    main(sbid=args.sbid,
         holo_dir=args.holo_dir,
         remake_stokes=args.remake_stokes,
         max_order=args.max_order,
         param=args.param,
         snr_limit=args.snr_limit,
         )


if __name__ == "__main__":
    sys.exit(cli())
