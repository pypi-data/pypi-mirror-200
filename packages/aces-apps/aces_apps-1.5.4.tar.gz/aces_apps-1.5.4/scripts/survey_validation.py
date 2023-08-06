#!/usr/bin/env python
"""
This generates a "data validation" page - a summary of various aspects of data quality.

"""
import os
import sys
import numpy as np
import warnings
import argparse as ap
import time
import tarfile

import matplotlib as mpl

mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from aces.survey.survey_class import ASKAP_Survey_factory

from astropy.wcs import WCS
from astropy.time import Time
from astropy.coordinates import SkyCoord
from astropy import units as u
from astropy.table import Table, Column
from astropy.io import ascii, fits
from astropy.io.votable import parse_single_table
import ephem

explanation = __doc__

f_small = 7
f_med = 8
f_big = 12
f_huge = 14


def arg_init():
    # code_path = os.path.dirname(os.path.abspath(survey.__file__))

    parser = ap.ArgumentParser(prog='survey_validation', formatter_class=ap.RawDescriptionHelpFormatter,
                               description=__doc__,
                               epilog='See -x for more explanation')
    # noinspection PyTypeChecker
    # parser.add_argument('fld_name', nargs=1, help='Survey field name; no default')
    parser.add_argument('-n', '--numbers', type=int, nargs='*', help="Row numbers to process")
    parser.add_argument('-b', '--bounds', type=int, nargs='*', help="Row number bounds")
    parser.add_argument('-S', '--sbid', type=int, nargs=1, help="Select by SBID")
    parser.add_argument('-C', '--calsbid', type=int, nargs=1, help="Select by CAL SBID")
    parser.add_argument('-f', '--force', action='store_true', help="Force execution on non-selected field")

    parser.add_argument('-e', '--epoch', type=int, default=0, help="Survey epoch")
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-x', '--explain', action='store_true', help="give an expanded explanation")
    return parser


def observer(horizon='15.0'):
    mro = ephem.Observer()
    mro.long = ephem.degrees('116.53')
    mro.lat = ephem.degrees('-26.98')
    mro.elevation = 360.0
    mro.horizon = ephem.degrees(horizon)
    return mro


def build_fixed_body(ra, dec):
    new_body = ephem.FixedBody()
    new_body._ra = ra
    new_body._dec = dec
    return new_body


def wrap_at(x, w):
    ret = (x + w) % (360.0) - w
    return ret


def get_HA_el(obstim, ra, dec, obs):
    # obstim - observation time MJD as seconds (as recorded in RACS db)
    # ra  Right ascension in degrees
    # dec Declination in degrees
    # obs ephem.Observer object

    mjd = obstim / 3600.0 / 24.0

    djd = mjd - 15019.5
    edate = ephem.Date(djd)

    obs.date = edate

    source = build_fixed_body(np.radians(ra), np.radians(dec))
    source.compute(edate)
    source.compute(obs)
    hangle = wrap_at(np.degrees(obs.sidereal_time() - source.ra), 180.0)
    elev = np.degrees(source.alt.real)
    return hangle, elev, source


def correct_catmatch_for_psf(aks, sbid, fld, refcat, fcor=None):
    # reads a cat_match table from csv file, and returns
    # an astropy table with RACS fluxes corrected for PSF area variation
    # The integrated flux of a source can be calculated as the sum of pixel values,
    # divided by the PSF area in pixels. If the PSF area is incorrect, as is often the case for
    # unconvolved RACS images, then the integrated flux computed buy naive procedures (assuming a
    # single PSF size over the image) will be in error by a factor of PSF(assumed)/PSF(true).
    # fcor, if given, is a 2d array on the same grid as psf images. Its value will be used as an
    # extra multiplicative factor.
    inx = aks.get_inx_from_fld_sbid(fld, sbid)
    bmaj_ref, bmin_ref = aks.get_field_data(inx, ['PSF_MAJOR', 'PSF_MINOR'])
    rad, decd, pol = aks.get_field_data(inx, ['RA_DEG', 'DEC_DEG', 'POL_AXIS'])
    pang = np.radians(pol + 45.0)

    psf_bma = aks.get_sub_fitsdata(fld, sbid, 'bma')
    psf_bmi = aks.get_sub_fitsdata(fld, sbid, 'bmi')
    if isinstance(refcat, str):
        kw = {'C_SURVEY': refcat}
        which = 'cat'
        atab = aks.get_sub_table(fld, sbid, which, **kw)
    elif isinstance(refcat, Table):
        atab = refcat
    else:
        raise TypeError("refcat is wrong type")

    if psf_bma is None or psf_bmi is None or atab is None:
        ret = None
    elif len(atab) < 2:
        ret = None
    else:
        if len(atab) < 2:
            ret = None
        else:
            psf_area_ref = bmaj_ref * bmin_ref
            flux_factor = psf_area_ref / (psf_bma * psf_bmi)
            if fcor is not None:
                flux_factor *= fcor

            boresight = SkyCoord(rad, decd, unit=u.deg, frame='icrs')
            ra = np.radians(atab['RA'])
            dec = np.radians(atab['DEC'])

            scs = [SkyCoord(ra, dec, unit=u.rad, frame='icrs') for ra, dec in zip(ra, dec)]
            seps = [boresight.separation(sc).radian for sc in scs]
            pas = [boresight.position_angle(sc).radian for sc in scs]
            cx = [np.degrees(d * +np.cos(pa)) for d, pa in zip(seps, pas)]
            cy = [np.degrees(d * -np.sin(pa)) for d, pa in zip(seps, pas)]
            # rotation to account for PA of observation
            cxr = [cxi * np.cos(pang) + cyi * -np.sin(pang) for cxi, cyi in zip(cx, cy)]
            cyr = [cxi * np.sin(pang) + cyi * +np.cos(pang) for cxi, cyi in zip(cx, cy)]

            ix = [int(cxi / 0.1 + 42.5) for cxi in cxr]
            iy = [int(cyi / 0.1 + 42.5) for cyi in cyr]

            fac = [flux_factor[ixi, iyi] for ixi, iyi in zip(ix, iy)]

            atab['ASKAP_flux'] *= fac
            atab['Flux_Ratio_AlphaCorr'] *= fac
            atab['Flux_Ratio_NOAlphaCorr'] *= fac
            ixc = Column(ix, name='IX')
            iyc = Column(iy, name='IY')
            atab.add_columns([ixc, iyc])
            ret = atab
    return ret


def sky_plot(data, fig, ax, colourbar=False):
    im = ax.imshow(np.log10(data), vmin=2.0, vmax=3.0, origin='lower', cmap='YlOrRd')
    ax.grid(color='0.5', ls='solid')
    ax.set_xlabel('RA (J2000)')
    ax.set_ylabel('Dec (J2000)')

    if colourbar:
        cbar = fig.colorbar(im, cax=None, ax=ax, use_gridspec=True, pad=0.09, shrink=0.5, orientation='vertical')
        cbar.set_label(r'Image rms ($\mu$Jy/beam)', fontsize=f_small)
        yt = np.log10(np.array([100, 200, 300, 500, 1000]))
        ytl = ["{:.0f}".format(10. ** lx) for lx in yt]
        cbar.set_ticks(yt)
        cbar.set_ticklabels(ytl)

    gal_col = 'b'
    overlay = ax.get_coords_overlay('galactic')
    overlay.grid(color=gal_col, ls='dashed', alpha=0.6)
    overlay[0].tick_params(colors=gal_col)
    overlay[1].tick_params(colors=gal_col)
    overlay[0].set_axislabel('Galactic long.', color=gal_col)
    overlay[1].set_axislabel('Galactic lat.', color=gal_col)
    return im


def get_weighted_alphas(cattab, fref, freq_cat):
    s1 = cattab['ASKAP_flux']
    s2 = cattab['Comp_flux']
    rat = s2 / s1
    lrat = np.log(rat)
    lav = np.average(lrat, weights=s1)

    variance = np.average((lrat - lav) ** 2, weights=s1)
    lav_lo = lav - np.sqrt(variance)
    lav_hi = lav + np.sqrt(variance)
    lfr = np.log(freq_cat / fref)
    alph = lav_lo / lfr, lav / lfr, lav_hi / lfr
    return alph


def get_astrom_err(atab):
    ra1 = np.radians(atab['RA'])
    dec1 = np.radians(atab['DEC'])
    ra2 = np.radians(atab['RA_comp'])
    dec2 = np.radians(atab['DEC_comp'])
    sp = [SkyCoord(ra, dec, unit=u.rad, frame='icrs') for ra, dec in zip(ra1, dec1)]
    sp2 = [SkyCoord(ra, dec, unit=u.rad, frame='icrs') for ra, dec in zip(ra2, dec2)]
    seps = [s.separation(s2).radian for s, s2 in zip(sp, sp2)]
    pas = [s.position_angle(s2).radian for s, s2 in zip(sp, sp2)]
    err_dpa = [(d, pa) for d, pa in zip(seps, pas)]
    srv_pos = sp
    return srv_pos, err_dpa


def t_string(db_time):
    time_val = Time(db_time / 3600.0 / 24.0, format='mjd', scale='utc')
    time_val.format = 'iso'
    return "{}".format(time_val)


def show_row(r):
    mro = observer(horizon='15.0')
    outlines = []
    q0 = r['SBID', 'CAL_SBID', 'FIELD_NAME', 'RA_HMS', 'DEC_DMS', 'GAL_LONG', 'GAL_LAT']
    sbid, calsbid, field, rahms, decdms, glon, glat = q0
    field = field.replace('test4_1.05_', '')
    rahms = rahms.replace(' ', ':')
    decdms = decdms.replace(' ', ':')

    q1 = r['SCAN_START', 'RA_DEG', 'DEC_DEG', 'SBID', 'CAL_SBID', 'MED_RMS_uJy']
    start, ra, dec, sbid, csbid, medrms = q1
    sc_int = r['SCAN_TINT']

    hangle, ele, source = get_HA_el(start, ra, dec, mro)
    obstim = t_string(start)
    li0 = "{}".format(field)
    li1 = "      J2000 : ({},{})\n   Galactic : ({:.2f},{:.2f})\n".format(rahms, decdms, glon, glat)
    li2 = "       SBID : {:5d} \n        CAL : {:5d}\n".format(sbid, calsbid)
    li3 = "      Start : {} UT\nIntegration : {:.1f}s\n Hour angle : {:.1f}h\n  Elevation : {:.2f}".format(obstim,
                                                                                                           sc_int,
                                                                                                           hangle / 15.,
                                                                                                           ele)

    li4 = r'Median rms  : {:.0f} ($\mu$Jy/beam)'.format(r['MED_RMS_uJy']) + '\n'
    li5 = 'Selavy comp : {:d}'.format(r['NUM_SELAVY'])
    li6 = 'Imaged at   : {}'.format(t_string(r['MOSAIC_TIME']))

    outlines.append(li0)
    outlines.append(li1 + li2 + li3)
    outlines.append(li4 + li5)
    outlines.append(li6)
    return outlines


def scounts(fluxes, minlogf, maxlogf, Nbins, area):
    logf = np.linspace(minlogf, maxlogf, Nbins)
    f = np.power(10., logf)

    area_sky_total = 360.0 * 360.0 / np.pi
    solid_angle_skads = 4. * np.pi * area / area_sky_total

    Nflux, bins = np.histogram(fluxes, f)
    binsmid = 0.5 * ((bins[:-1]) + (bins[1:]))
    ds = bins[1:] - bins[:-1]

    counts_err = np.array(np.sqrt(Nflux), dtype=int)

    scount = np.power(binsmid, 2.5) * Nflux / (ds * solid_angle_skads)
    scount_err = np.power(binsmid, 2.5) * 1. * counts_err / (ds * solid_angle_skads)
    return bins[:-1], bins[1:], binsmid, Nflux, counts_err, scount, scount_err


def logn_logs(file, axis, skads, dezotti, minlogf=-4., maxlogf=2., Nbins=81, freq=887.5, alpha=-0.8, area=60.):
    fluxcol = 'flux_int'
    data = parse_single_table(file).array
    data_sc = scounts(data['col_' + fluxcol] * 1.e-3, minlogf, maxlogf, Nbins, area)

    alpha_convert = np.power(freq / 1400., alpha)

    axis.errorbar(skads['fl_bin_mid'] * 1.e3 * alpha_convert, skads['SC'] * np.power(alpha_convert, 1.5),
                  yerr=skads['SC_err'] * np.power(alpha_convert, 1.5), fmt=':', color='k', label='Wilman et al. 2008')
    axis.errorbar(np.power(10., dezotti['col1']) * 1.e3 * alpha_convert, dezotti['col2'] * np.power(alpha_convert, 1.5),
                  yerr=[dezotti['col4'] * np.power(alpha_convert, 1.5), dezotti['col3'] * np.power(alpha_convert, 1.5)],
                  fmt='d', color='grey', alpha=0.2, label='de Zotti et al. 2010')
    axis.errorbar(data_sc[2] * 1.e3, data_sc[5], yerr=data_sc[6], fmt='.', color='darkred',
                  label='Raw Component Catalogue - %i sources' % len(data))
    axis.set_xscale('log')
    axis.set_yscale('log')
    axis.set_xlabel('Flux Density at %.1lf MHz (mJy)' % freq)
    axis.set_ylabel(r'$\frac{dN}{dS} S^{\frac{5}{2}}$ (Jy$^{\frac{3}{2}}$ sr$^{-1}$)')
    axis.set_xlim(0.2, 1.e4)
    axis.set_ylim(5.e-2, 1.e4)
    axis.grid()
    axis.legend(loc='lower right', fontsize=f_small)


def get_icrf_ast(aks):
    ta = aks.f_table
    # mk = ta['SELECT'] == 1
    # tab = ta[mk]
    tab = ta

    kw = {'C_SURVEY': 'ICRF'}
    which = 'cat'
    all_errs = []
    tile_errs = []
    all_pos = []
    for r in tab:
        fld, sb = r['FIELD_NAME'], r['SBID']
        indx = r['INDEX']
        atab = aks.get_sub_table(fld, sb, which, **kw)
        if atab is None:
            pass
            # print('-')
        elif len(atab) > 0:
            #         print(len(atab))
            pos, errs = get_astrom_err(atab)
            all_errs += errs
            all_pos += pos
            errs = np.array(errs)
            dx = errs[:, 0] * -np.sin(errs[:, 1])
            dy = errs[:, 0] * np.cos(errs[:, 1])
            tile_errs.append([dx.mean(), dy.mean()])

            mag = np.array([a[0] for a in errs]) * 206265.
            if mag.max() > 13.0:
                print("{:4d} {:5d} {} {:f}".format(indx, sb, fld, mag.max()))
                csvnam = "admin/epoch_0/cat_match_ICRF_{:d}-{}.csv".format(sb, fld)
    #             print("rm {}".format(csvnam))

    all_errs = np.array(all_errs)
    # print("all_errs.shape = {}".format(all_errs.shape))
    dx = np.degrees(all_errs[:, 0] * -np.sin(all_errs[:, 1])) * 3600.0
    dy = np.degrees(all_errs[:, 0] * np.cos(all_errs[:, 1])) * 3600.
    return dx, dy


def main():
    args = arg_init().parse_args()
    run_date = time.strftime("%Y%m%d-%H%M%S")

    if args.explain:
        print(explanation)
        sys.exit()
    verbose = args.verbose

    print("")
    print("Running survey_validation.py with the following input:")
    print("ARGS = ", args)
    print("")

    epoch = args.epoch
    aks = ASKAP_Survey_factory(verbose=False, epoch=epoch)
    root = aks.get_data_root()
    fn = aks.survey_files.file_name
    freq_ref = aks.get_freq_ref()

    # First, select on valid state, and possibly on given CAL_SBID or SBID
    if args.force:
        crit = [['STATE', '!=', '--NULL--']]
    else:
        crit = [['SELECT', '==', 1]]

    if args.calsbid:
        crit.append(['CAL_SBID', '==', args.calsbid])
    elif args.sbid:
        crit.append(['SBID', '==', args.sbid])

    rows = aks.select_indices(crit)
    if verbose:
        print("criteria  : {}".format(crit))
        print(rows)

    # Now, if specific numbers or ranges are given, use them instead.
    if args.numbers is not None:
        if len(args.numbers) > 0:
            rows = args.numbers
    if args.bounds is not None:
        if len(args.bounds) == 2:
            bounds = args.bounds
            rows = range(bounds[0], bounds[1])

    if len(rows) == 0:
        print("No rows specified")
        sys.exit(0)

    dx_icrf, dy_icrf = get_icrf_ast(aks)

    folder_sc = os.environ['SURVEY'] + '/db-inputs/'

    dezotti = Table(ascii.read(folder_sc + 'de_zotti_1p4.txt'))
    skads = Table(fits.getdata(folder_sc + 'SKADS_1p4GHz.fits'))

    for indx in rows:
        row = aks.f_table[indx]

        fld = row['FIELD_NAME']
        sb = row['SBID']
        csb = row['CAL_SBID']

        if verbose:
            print("{:4d} {:5d} {}".format(indx, sb, fld))

        # Try possible selavy file names
        selavy = fn('selavy-components', indx)

        imname1 = fn('mosaic_rms', indx)
        if imname1.exists() and selavy.exists():
            print('IQR image : ', imname1)

            hdu = fits.open(str(imname1))[0]
            wcs = WCS(hdu.header)
            wsub = wcs.sub(2)
            im1 = hdu.data

            data1 = np.squeeze(im1)
            datam1 = np.ma.masked_invalid(data1)
            tile_area = datam1.count() * (250. / 3600.) ** 2

            kwf1 = {'C_SURVEY': 'SUMSS'}
            cattab1 = aks.get_sub_table(fld, sb, 'cat', **kwf1)
            kwf2 = {'C_SURVEY': 'NVSS'}
            cattab2 = aks.get_sub_table(fld, sb, 'cat', **kwf2)
            ncat1, ncat2 = 0, 0
            if cattab1:
                ncat1 = len(cattab1)
                alphas1 = get_weighted_alphas(cattab1, freq_ref, 843.0)

            if cattab2:
                ncat2 = len(cattab2)
                alphas2 = get_weighted_alphas(cattab2, freq_ref, 1400.0)

            fref = aks.get_freq_ref()
            ht = 8.0
            wd = ht * np.sqrt(2.0)
            fig = plt.figure(figsize=(wd, ht))
            plt.rc('axes', labelsize=8)
            plt.rc('xtick', labelsize=7.5)
            plt.rc('ytick', labelsize=7.5)

            gs = gridspec.GridSpec(nrows=100, ncols=141)
            gs.update(left=0.0, right=0.9999, bottom=0.001, top=0.999, hspace=0.0, wspace=0.0)

            ax_le = fig.add_subplot(gs[0:28, 0:37])
            ax_le.axis('off')
            ax_im = fig.add_subplot(gs[35:99, 0:70], projection=wsub)

            ax_psf = fig.add_subplot(gs[0:28, 87:107])
            ax_logn = fig.add_subplot(gs[0:28, 44:84])

            ax_c2 = fig.add_subplot(gs[66:98, 74:105])
            ax_c1 = fig.add_subplot(gs[33:65, 74:105], sharex=ax_c2)

            ax_ast2 = fig.add_subplot(gs[66:98, 110:])
            ax_ast1 = fig.add_subplot(gs[33:65, 110:], sharex=ax_ast2)
            ax_ast = fig.add_subplot(gs[0:32, 110:], sharex=ax_ast2)

            for ax in [ax_c1, ax_c2, ax_ast, ax_ast1, ax_ast2]:
                ax.set_aspect(1.0)

            logn_logs(selavy, ax_logn, skads, dezotti, freq=freq_ref, area=tile_area)

            # PSF   ------------------------------
            #
            # For data after RACS(I), change the way this works, as it is now standard to create "common-resolution" mosaics
            # so that the range of PSF shapes over the mosaic should not be an issue to record.
            ta = aks.f_table
            # mk = ta['SELECT'] == 1
            # tab = ta[mk]
            tab = ta
            bmaj = tab['PSF_MAJOR']
            bmin = tab['PSF_MINOR']
            ax_psf.plot(bmin, bmaj, '.', c='0.6', ms=2)
            ax_psf.set_aspect(1.0)
            bma_i = row['PSF_MAJOR']
            bmi_i = row['PSF_MINOR']

            ax_psf.plot(bmi_i, bma_i, 'ok', ms=3)
            if aks.survey_name == "RACS" and epoch == 0:
                psf_bma = aks.get_sub_fitsdata(fld, sb, 'bma')
                psf_bmi = aks.get_sub_fitsdata(fld, sb, 'bmi')
                bmi_min, bmi_max = psf_bmi.min(), psf_bmi.max()
                bma_min, bma_max = psf_bma.min(), psf_bma.max()
                ax_psf.plot([bmi_i, bmi_i], [bma_min, bma_max], 'k')
                ax_psf.plot([bmi_min, bmi_max], [bma_i, bma_i], 'k')
            ax_psf.set_xlim(5., 20.)
            ax_psf.set_ylim(5., 40.)
            ax_psf.grid()
            ax_psf.set_xlabel('PSF minor axis (arcsec)')

            ax_psf.set_ylabel('PSF major axis (arcsec)')

            # RMS image  ------------------------------
            # Convert image to microJy/beam
            imm = sky_plot(data1 * 1.0e6, fig, ax_im, colourbar=True)
            # ax_im.scatter(row['RA_DEG'], row['DEC_DEG'], transform=ax_im.get_transform('fk5'), marker='+', s=300,
            #               edgecolor='k', facecolor='k')
            ax_im.set_title('Image noise', loc='left', fontsize=f_med)

            # Flux-flux plots  ------------------------------
            ax_c1.set_xlim(1.0, 1.0e4)
            ax_c2.set_xlim(1.0, 1.0e4)
            ax_c1.set_ylim(1.0, 1.0e4)
            ax_c2.set_ylim(1.0, 1.0e4)

            if ncat1 > 0:
                fref2 = 843.0
                sp_fac = (fref / fref2) ** 0.8

                ax_c1.loglog(cattab1['ASKAP_flux'], cattab1['Comp_flux'], 'ok', ms=2)
                ax_c1.set_ylabel('{} integrated flux (mJy)'.format(kwf1['C_SURVEY']))
                ax_c1.text(2., 6000., '{} ({:d})'.format(kwf1['C_SURVEY'], ncat1), fontsize=f_med)
                ax_c1.loglog([2., 8000.], [2., 8000.], '-', c='r')
                ax_c1.loglog([2., 8000.], [2. * sp_fac, 8000. * sp_fac], '--', c='r')
                a0 = "{:.2f}".format(alphas1[1])
                al = "{:.2f}".format(abs(alphas1[0] - alphas1[1]))
                le_s1 = r' $\alpha_{SU} : {%s}\pm{%s}$' % (a0, al)
                ax_c1.text(2., 4000., '{}'.format(le_s1), fontsize=f_med)

            else:
                ax_c1.loglog([2.0, 2000.0], [2.0, 2000.0], 'ow')
                ax_c1.text(100., 100., 'No data for {}'.format(kwf1['C_SURVEY']), va='center', ha='center')
            q = plt.setp(ax_c1.get_xticklabels(), visible=False)
            ax_c1.grid()

            if ncat2 > 0:
                fref2 = 1400.0
                sp_fac = (fref / fref2) ** 0.8
                ax_c2.loglog(cattab2['ASKAP_flux'], cattab2['Comp_flux'], 'ok', ms=2)
                ax_c2.set_xlabel('ASKAP integrated flux (mJy)')
                ax_c2.set_ylabel('{} integrated flux (mJy)'.format(kwf2['C_SURVEY']))
                ax_c2.text(2., 6000., '{} ({:d})'.format(kwf2['C_SURVEY'], ncat2), fontsize=f_med)
                ax_c2.loglog([2., 8000.], [2., 8000.], '-', c='r')
                ax_c2.loglog([2., 8000.], [2. * sp_fac, 8000. * sp_fac], '--', c='r')
                a0 = "{:.2f}".format(alphas2[1])
                al = "{:.2f}".format(abs(alphas2[0] - alphas2[1]))
                le_s2 = r' $\alpha_{NV} : {%s}\pm{%s}$' % (a0, al)
                ax_c2.text(2., 4000., '{}'.format(le_s2), fontsize=f_med)

            else:
                ax_c2.loglog([2.0, 2000.0], [2.0, 2000.0], 'ow')
                ax_c2.text(100., 100., 'No data for {}'.format(kwf2['C_SURVEY']), va='center', ha='center')
            ax_c2.set_xlabel('ASKAP integrated flux (mJy)')
            ax_c2.grid()

            # Astrometry  ------------------------------

            kwa = {'C_SURVEY': 'ICRF'}
            asttab = aks.get_sub_table(fld, sb, 'cat', **kwa)
            n_icrf = 0
            if asttab:
                pos, err = get_astrom_err(asttab)
                n_icrf = len(err)
                if n_icrf > 0:
                    err = np.array(err)
                    dx = np.degrees(err[:, 0] * -np.sin(err[:, 1])) * 3600.
                    dy = np.degrees(err[:, 0] * np.cos(err[:, 1])) * 3600.

                ax_ast.errorbar(dx, dy, xerr=0.55, yerr=0.55, fmt='ok', ms=3)

            ax_ast.plot(dx_icrf, dy_icrf, '.', c='0.7', zorder=0, ms=2)

            ax_ast.set_xlim(-8., 8.)
            ax_ast.set_ylim(-8., 8.)
            ax_ast.grid()
            ax_ast.set_ylabel('Offset (arcsec)')
            ax_ast.text(0.0, 7.0, 'Astrometry', va='center', ha='center', fontsize=f_med)
            ax_ast.text(-7.0, 7.0, 'ICRF-3  ({:d})'.format(n_icrf), fontsize=f_med)
            ax_ast.plot([5., 3., 3.], [-7., -7., -5.], '-k')
            ax_ast.text(3., -5., 'N', ha='center', va='bottom')
            ax_ast.text(5.2, -7., 'W', ha='left', va='center')

            if ncat1 > 0:
                pos, err = get_astrom_err(cattab1)
                if len(err) > 0:
                    err = np.array(err)
                    dx = np.degrees(err[:, 0] * -np.sin(err[:, 1])) * 3600.
                    dy = np.degrees(err[:, 0] * np.cos(err[:, 1])) * 3600.

                ax_ast1.plot(dx, dy, '.r', zorder=0, ms=2)
                ax1 = dx.mean()
                ay1 = dy.mean()
                ex1 = dx.std()
                ey1 = dy.std()
                ax_ast1.errorbar(ax1, ay1, xerr=ex1, yerr=ey1, fmt='ok')
                ax_ast1.set_xlim(-8., 8.)
                ax_ast1.set_ylim(-8., 8.)
                ax_ast1.grid()
                ax_ast1.set_ylabel('Offset (arcsec)')
                ax_ast1.text(-7.0, 7.0, kwf1['C_SURVEY'], fontsize=f_med,
                             bbox=dict(facecolor='white', edgecolor='none', alpha=0.8))
                le_a1 = r' $\epsilon_{SU} : ({%.1f}\pm{%.1f},{%.1f}\pm{%.1f})$' % (ax1, ex1, ay1, ey1)
                ax_ast1.text(7.6, 7.6, le_a1, va='top', ha='right', fontsize=f_med,
                             bbox=dict(facecolor='white', edgecolor='none', alpha=0.8))

            else:
                ax_ast1.set_xlim(-8., 8.)
                ax_ast1.set_ylim(-8., 8.)

                ax_ast1.text(0., 0., 'No data for {}'.format(kwf1['C_SURVEY']), va='center', ha='center')

            if ncat2 > 0:
                pos, err = get_astrom_err(cattab2)
                if len(err) > 0:
                    err = np.array(err)
                    dx = np.degrees(err[:, 0] * -np.sin(err[:, 1])) * 3600.
                    dy = np.degrees(err[:, 0] * np.cos(err[:, 1])) * 3600.

                ax_ast2.plot(dx, dy, '.r', zorder=0, ms=2)
                ax2 = dx.mean()
                ay2 = dy.mean()
                ex2 = dx.std()
                ey2 = dy.std()
                ax_ast2.errorbar(ax2, ay2, xerr=ex2, yerr=ey2, fmt='ok')

                ax_ast2.set_xlim(-8., 8.)
                ax_ast2.set_ylim(-8., 8.)
                ax_ast2.grid()
                ax_ast2.set_xlabel('Offset (arcsec)')
                ax_ast2.set_ylabel('Offset (arcsec)')
                ax_ast2.text(-7.0, 7.0, kwf2['C_SURVEY'], fontsize=f_med,
                             bbox=dict(facecolor='white', edgecolor='none', alpha=0.8))
                le_a2 = r' $\epsilon_{NV} : ({%.1f}\pm{%.1f},{%.1f}\pm{%.1f})$' % (ax2, ex2, ay2, ey2)
                ax_ast2.text(7.6, 7.6, le_a2, va='top', ha='right', fontsize=f_med,
                             bbox=dict(facecolor='white', edgecolor='none', alpha=0.8))

            else:
                ax_ast2.set_xlim(-8., 8.)
                ax_ast2.set_ylim(-8., 8.)
                ax_ast2.set_xlabel('Offset (arcsec)')

                ax_ast2.text(0., 0., 'No data for {}'.format(kwf2['C_SURVEY']), va='center', ha='center')

            q = plt.setp(ax_ast.get_xticklabels(), visible=False)
            q = plt.setp(ax_ast1.get_xticklabels(), visible=False)

            # Text information ------------------------------

            legend = show_row(row)

            ax_le.axis('off')
            # for i, li in enumerate(legend):
            ax_le.text(0.01, 0.95, legend[0], fontsize=f_huge, va='top')
            ax_le.text(0.01, 0.8, legend[1], fontsize=f_small, family='monospace', va='top')

            ax_le.text(0.01, 0.3, legend[2], fontsize=f_small, family='monospace', va='top')
            ax_le.text(0.01, 0.15, legend[3], fontsize=f_small, family='monospace', va='top')

            x0, x1 = ax_le.get_xlim()
            y0, y1 = ax_le.get_ylim()
            ax_le.plot([x0, x1, x1, x0, x0], [y0, y0, y1, y1, y0], '-r', lw=1)

            print_date = time.strftime("%Y%m%d-%H%M%S")
            ax_le.text(0.98, 0.02, print_date, fontsize=f_small, family='monospace', va='bottom', ha='right')

            # Compose output.
            # im_path = sut.get_product_name(aks, indx, which='mosaic_fcor')
            im_path = fn('mosaic_image_convolved', indx)
            im_name = str(im_path.stem)
            im_dir = str(im_path.parent.parent)
            v_dir = "validation_{}".format(im_name)
            val_dir = "{}/{}".format(im_dir, v_dir)

            if not os.path.exists(val_dir):
                os.mkdir(val_dir)

            field = fld.replace('test_1.05_', '')
            pname = "{}/{:d}-{}_valid.png".format(val_dir, sb, field)
            hname = "{}/index.html".format(val_dir)
            pfile = str(root.joinpath("{:d}/{}".format(csb, pname)).name)
            hfile = str(root.joinpath("{:d}/{}".format(csb, hname)))
            tfile = str(root.joinpath("{:d}/validation_SB{:d}_{}.tar".format(csb, sb, field)))
            fig.savefig(pname, dpi=300, bbox_inches='tight')

            f = open(hname, 'wb')

            message = """<html>
            <head></head>
            <body>
            <p>RACS field {}</p>
            <p>
            
            <img src="{}" height=600/>
            
            </a>
            </p>
            
            
            </body>
            </html>"""
            output = message.format(field, pfile)
            f.write(output.encode())
            f.close()
            # The tar process is done from the directory holding the files to be tarred.
            cwd = os.getcwd()
            os.chdir(im_dir)
            tar = tarfile.open(tfile, "w")
            tar.add(v_dir)
            tar.close()
            os.chdir(cwd)
            print("Plot written to ", pname)
        else:
            if not imname1.exists():
                print("No IQR file found : {}".format(imname1))
            if not selavy.exists():
                print("No selavy file found : {}".format(selavy))

            print("Skipping {}  {:d} ".format(fld, indx))


if __name__ == "__main__":
    sys.exit(main())
