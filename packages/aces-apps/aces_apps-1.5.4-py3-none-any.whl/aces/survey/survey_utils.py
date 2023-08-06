#!/usr/bin/env python

import os
import re
import glob

import aces.survey.survey_class as aks
import aces.survey.data_source as sds
import aces.survey.survey_leakage as slk

import numpy as np

from astropy.io import fits
from astropy.table import Table, hstack, vstack
from astropy.time import Time
from astropy.io import ascii
from astropy.io.votable import parse_single_table

from astropy.coordinates import SkyCoord
from astropy import units as u

import aces.misc.image_stats as ims

from pathlib import Path

beam_colnames = ['BEAM_NUM', 'BEAM_TIME', 'RA_DEG', 'DEC_DEG', 'GAL_LONG', 'GAL_LAT',
                 'PSF_MAJOR', 'PSF_MINOR', 'PSF_ANGLE', 'VIS_TOTAL', 'VIS_FLAGGED']
beam_coltypes = ['i4', 'f4', 'f4', 'f4', 'f4', 'f4',
                 'f4', 'f4', 'f4', 'i4', 'i4']
beam_types = {k: v for k, v in zip(beam_colnames, beam_coltypes)}

stats_colnames = ['FLD_NAME', 'SBID', 'NPIXV', 'MINIMUM', 'MAXIMUM', 'MED_RMS_uJy', 'MODE_RMS_uJy', 'STD_RMS_uJy',
                  'MIN_RMS_uJy',
                  'MAX_RMS_uJy']
stats_coltypes = ['S20', 'i4', 'i4', 'f4', 'f4', 'f4', 'f4', 'f4', 'f4', 'f4']
stats_types = {k: v for k, v in zip(stats_colnames, stats_coltypes)}

astrom_colnames = ['BEAM1', 'BEAM2', 'DX_MEAN', 'DX_STD', 'DY_MEAN', 'DY_STD']
astrom_coltypes = ['i4', 'i4', 'f4', 'f4', 'f4', 'f4']
astrom_types = {k: v for k, v in zip(astrom_colnames, astrom_coltypes)}

arcs = np.pi / 180.0 / 3600.

# Beam adjacency for square_6x6
adjacent = {0: [5, 1, 15, 2],
            1: [6, 8, 3],
            2: [3, 14, 12],
            3: [9, 11],
            4: [17, 5, 35, 15],
            5: [18, 6],
            6: [19, 7],
            7: [20, 22, 8],
            8: [23, 9],
            9: [24, 10],
            10: [25, 11, 27],
            11: [12, 28],
            12: [13, 29],
            13: [14, 32, 30],
            14: [15, 33],
            15: [34]}


def from_ra_dec_deg(ra, dec):
    sc = SkyCoord(ra, dec, frame='icrs', unit="deg")
    return [sc.icrs.ra.degree, sc.icrs.dec.degree, sc.galactic.l.degree, sc.galactic.b.degree]


def stale_files(pre, post):
    if isinstance(pre, Path) and isinstance(post, Path):
        if pre.exists():
            o_time = pre.stat().st_mtime
            if post.exists():
                d_time = post.stat().st_mtime
            else:
                d_time = 0
            ret = (o_time > d_time)
        else:
            ret = False

    elif isinstance(pre, (list, tuple)) and isinstance(post, Path):
        if all([a.exists() for a in pre]):
            if post.exists():
                d_time = post.stat().st_mtime
            else:
                d_time = 0
            o_time = max([a.stat().st_mtime for a in pre])
            ret = (o_time > d_time)
        else:
            ret = False

    else:
        ret = []
        for o, d in zip(pre, post):
            if o.exists():
                o_time = o.stat().st_mtime
                if d.exists():
                    d_time = d.stat().st_mtime
                else:
                    d_time = 0
                ret.append(o_time > d_time)
            else:
                ret.append(False)

    return ret


def func_mosaic_info(sv_obj, row_num=None, field=None, sbid=None, **kwargs):
    fn = sv_obj.survey_files.file_name
    if row_num is None:
        inx = sv_obj.get_inx_from_fld_sbid(field, sbid)
    else:
        inx = row_num
    row = sv_obj.get_row(inx)

    m_name = fn('mosaic_image_convolved', inx)

    cols = ['STATE', 'MOSAIC_TIME', 'PSF_MAJOR', 'PSF_MINOR', 'PSF_ANGLE']
    if m_name.exists():
        size = m_name.stat().st_size

        if size > 6000:
            fits_file = fits.open(m_name)
            fits_header = fits_file[0].header
            # get time of imaging from header
            filedate = fits_header['DATE'].replace('T', ' ')
            time_val = Time(filedate, format='iso', scale='utc')
            time_val.format = 'mjd'
            ftime = time_val.value * 3600.0 * 24.0

            rtime = row['MOSAIC_TIME']
            if ftime > rtime:
                # fits_data = np.squeeze(fits_file[0].data)
                # Move the following to stats_info below.
                # fmin = np.nanmin(fits_data)
                # fmax = np.nanmax(fits_data)
                # npixv = np.count_nonzero(~np.isnan(fits_data))

                info = ['IMAGED', ftime]
                if 'BMAJ' not in fits_header:
                    print("Corrupt FITS file? {}".format(m_name))
                    info += [-1.] * 3
                else:
                    info.append(fits_header['BMAJ'] * 3600.)  # in arcsec
                    info.append(fits_header['BMIN'] * 3600.)  # in arcsec
                    info.append(fits_header['BPA'])  # in degrees
                # info += [fmin, fmax]
                sv_obj.put_field_data(inx, cols, info)
                # refresh row
                row = sv_obj.get_row(inx)

        # Find the processing parset
        parfile = find_parset(sv_obj, inx)
        if parfile:
            val = get_input(parfile, 'Cimager.MinUV')
            # val has form '[0,0,30]'; we seek the final item as an integer.
            # print("val = ", val)
            if val is None:
                minuv = 0
            else:
                minuv = int(re.findall('[0-9]+', val)[-1])
            sv_obj.put_field_data(inx, ['MinUV'], [minuv])
        else:
            print("No parset found for {}  SBID = {:d}".format(row['FIELD_NAME'], row['SBID']))

    else:
        sv_obj.put_field_data(inx, ['MOSAIC_TIME'], [-1.0])
        print("{} not found or incomplete".format(m_name))


def func_beam_info(sv_obj, row_num=None, field=None, sbid=None, **kwargs):
    db = sv_obj.db_dir
    desc_file = sv_obj.db_inputs.joinpath('beam_table_desc.csv')
    beam_desc = ascii.read(str(desc_file), format='csv')
    arguments = [a.split(';') for a in beam_desc['ARGS']]
    # Any files need to be mentioned in the first argument
    files = [a[0].split('@') for a in arguments]
    mkb = [a[0] == 'beam' for a in files]
    mkf = [a[0] == 'flag_summary' for a in files]

    im_desc = beam_desc[mkb]
    ms_desc = beam_desc[mkf]

    if row_num is None:
        inx = sv_obj.get_inx_from_fld_sbid(field, sbid)
    else:
        inx = row_num
    row = sv_obj.get_row(inx)
    sb, fld = row['SBID'], row['FIELD_NAME']

    fn = sv_obj.survey_files.file_name
    beam_image_names = [fn('beam_image_raw', inx, beam=i) for i in range(36)]
    ms_names = [fn('flag_summary', inx, beam=i) for i in range(36)]

    ds1 = [sds.data_source_factory(f) for f in beam_image_names]
    tabs = [ds.get(im_desc) for ds in ds1]
    b_tab1 = vstack(tabs)
    ds2 = [sds.data_source_factory(f) for f in ms_names]
    tabs = [ds.get(ms_desc) for ds in ds2]
    b_tab2 = vstack(tabs)
    b_tab = hstack([b_tab1, b_tab2])
    b_tab['BEAM_NUM'] = np.arange(36)
    sds.func_cols(b_tab, beam_desc)
    b_tab = b_tab[list(beam_desc['CNAME'])]

    b_name = aks.make_beam_csv_name(sb, fld)
    b_path = db.joinpath(b_name)
    b_tab_len = np.ma.sum(b_tab['BEAM_TIME'] > 0.0).astype(int)
    print("func_beam_info ", inx, b_tab_len)
    if b_tab_len:
        b_tab.write(str(b_path), format='ascii.csv', delimiter=',', overwrite=True)
        sv_obj.put_field_data(inx, ['NBEAMS_I'], [b_tab_len])


def func_stats_info(sv_obj, row_num=None, field=None, sbid=None, stokes='i', method='iqr', **kwargs):
    fn = sv_obj.survey_files.file_name
    db_update = False
    do_replace = False
    if 'db_update' in kwargs:
        db_update = kwargs['db_update']

    if 'do_replace' in kwargs:
        do_replace = kwargs['do_replace']

    in_type = 'mosaic_image_convolved'
    out_type = 'mosaic_rms'

    if row_num is None:
        inx = sv_obj.get_inx_from_fld_sbid(field, sbid)
    else:
        inx = row_num
    row = sv_obj.get_row(inx)

    ima = fn(in_type, inx, stokes=stokes)
    sta = fn(out_type, inx, stokes=stokes)
    if not ima.exists() or ima.is_symlink():
        # print(ima)
        alt = Path(str(ima).replace('RACS_', 'RACS_test4_1.05_'))
        if alt.exists():
            ima = alt
            sta = Path(str(sta).replace('RACS_', 'RACS_test4_1.05_'))
        else:
            print("{} file {} not found (alt). ".format(in_type, alt))

    ret = None
    if ima.exists():
        stale = stale_files(ima, sta)

        # calculate the statistics of the image
        replace = stale or do_replace
        if method == 'rms':
            mos_st, stats, fname = ims.image_cell_statistic(ima, sta.parent, statistic='rms', replace_old=replace)
        elif method == 'iqr':
            mos_st, stats, fname = ims.image_cell_statistic(ima, sta.parent, statistic='iqr', replace_old=replace)
        elif method == 'med':
            mos_st, stats, fname = ims.image_cell_statistic(ima, sta.parent, statistic='med', replace_old=replace)

        ret = mos_st, stats
        if db_update:
            s_data = [stats['median'], stats['mode'], stats['std'], stats['minimum'], stats['maximum']]
            cols = ['MED_RMS_uJy', 'MODE_RMS_uJy', 'STD_RMS_uJy', 'MIN_RMS_uJy', 'MAX_RMS_uJy']
            sv_obj.put_field_data(inx, cols, s_data)

            cols = ['MINIMUM', 'MAXIMUM', 'NPIXELS_V']
            m_data = [mos_st['MINIMUM'], mos_st['MAXIMUM'], mos_st['NPIXV']]
            sv_obj.put_field_data(inx, cols, m_data)
    else:
        print("{} file {} not found. ".format(in_type, ima))
    return ret


# To remind of previous routine to match sources in adjacent beams. Reinstate from RACS if necessary.
# def func_astrom_bb_info(sv_obj, row_num=None, field=None, sbid=None, **kwargs):
#     fn = sv_obj.survey_files.file_name
#     db = sv_obj.db_dir
#


def func_leakage_info(sv_obj, 
    row_num=None, 
    field=None, 
    sbid=None, 
    pols=["v", "q", "u"],
    zone=-1.,
    snr=0):
    """Get Stokes V/Q/U leakage based on sources in selavy catalogue."""
    fn = sv_obj.survey_files.file_name
    db = sv_obj.db_dir

    if row_num is None:
        inx = sv_obj.get_inx_from_fld_sbid(field, sbid)
    else:
        inx = row_num
    row = sv_obj.get_row(inx)
    sb, fld = row['SBID'], row['FIELD_NAME']

    selavy_comp = fn('selavy-components', inx)
    if not selavy_comp.exists():
        print("No selavy {:d}".format(inx))
        return

    for pol in pols:
    
        f_name = aks.make_leakage_csv_name(sb, fld, pol=pol)
        f_path = db.joinpath(f_name)
        pol_image = fn('mosaic_image_convolved'.format(pol), inx, stokes=pol)

        if not pol_image.exists():
            print("No Stokes {} image {:d}".format(pol, inx))
            continue

        print("Getting leakage from {}".format(pol_image))

        prefix = 'col_'

        sdata = slk.StokesData(
            catalogue_i=str(selavy_comp),
            image_p=str(pol_image),
            ra_key=prefix + "ra_deg_cont",
            dec_key=prefix + "dec_deg_cont",
            multiplier=0.001
        )
        sdata.get_isolated(zone=zone/3600.)
        sdata.get_compact(
                int_flux=prefix + "flux_int",
                peak_flux=prefix + "flux_peak",
                ratio=(0.5, 2.0)
        )
        sdata.get_xycoords()
        sdata.get_leakage(local_rms=prefix + "rms_image", sigma=snr) 
        sdata.get_table_leakage(outname=str(f_path), prefix=prefix, pol=pol)

        print("Stokes {} leakage catalogue prepared {:d}.".format(pol, inx))

# --- Compare offsets ---
def func_cat_match_info(sv_obj, row_num=None, check_stale=True, field=None, sbid=None, **kwargs):
    fn = sv_obj.survey_files.file_name
    db = sv_obj.db_dir

    if row_num is None:
        inx = sv_obj.get_inx_from_fld_sbid(field, sbid)
    else:
        inx = row_num
    row = sv_obj.get_row(inx)
    sb, fld = row['SBID'], row['FIELD_NAME']
    tag = kwargs['comparison_survey']
    f_name = aks.make_cat_match_csv_name(sb, fld, tag)
    f_path = db.joinpath(f_name)

    selavy_comp = fn('selavy-components', inx)
    # print("selavy_comp :  {}".format(str(selavy_comp)))
    if not selavy_comp.exists():
        print("No selavy {:d}".format(inx))

    # print('fcmi : ', selavy_comp)

    cols = ['SELAVY_TIME', 'NUM_SELAVY']
    if selavy_comp.exists():
        # get file time in MJD seconds
        s_time = selavy_comp.stat().st_mtime + 40587.0 * 86400.
        stale = stale_files(selavy_comp, f_path)
        if stale or not check_stale:
            n_comp, flux_table = catalogue_compare(str(selavy_comp), **kwargs)
            if len(flux_table) > 0:
                flux_table.write(str(f_path), format='ascii', delimiter=',', overwrite=True)

        else:
            print("{} already prepared".format(f_path.name))
            c_tab = Table(parse_single_table(str(selavy_comp)).array)
            n_comp = len(c_tab)

        s_data = [s_time, n_comp]
        sv_obj.put_field_data(inx, cols, s_data)

    else:
        sv_obj.put_field_data(inx, cols, [-1., -1])
        print("Selavy file {} not found".format(selavy_comp))


def catalogue_compare(cat_file, **kwargs):
    """
    :param cat_file: Name of selavy components file

    :rtype: astropy Table

    Derived from Catherine Hale's Flux_Scale.py (Feb 2020).
    Tidied Apr 2021.
    """
    comp_survey = kwargs['comparison_survey']
    settings_file = kwargs['match_params']
    settings = ascii.read(settings_file, format='csv')
    prefix = 'col_'

    # Get values pertaining to this (THIS) catalogue - the selavy file.
    ir = np.where(settings['cat'] == 'THIS')[0][0]
    irow = settings[ir]
    srv_freq = irow['freq']
    srv_ident = prefix + irow['ident']
    srv_ra = prefix + irow['ra']
    srv_dec = prefix + irow['dec']
    srv_tflux = prefix + irow['tflux']
    srv_pflux = prefix + irow['flux']
    srv_rms = prefix + irow['im_rms']

    ares_min = irow['ares_min']
    ares_max = irow['ares_max']
    snr_min = irow['snr_min']
    rad_match = irow['rad1']
    rad_isol = irow['rad2']
    alpha = irow['alpha']

    # Now find the values for the comparison survey
    jr = np.where(settings['cat'] == comp_survey)[0][0]
    jrow = settings[jr]
    jfile = jrow['file']
    cat_freq = jrow['freq']
    cat_ra = jrow['ra']
    cat_dec = jrow['dec']
    cat_tflux = jrow['tflux']
    got_flux = bool(cat_tflux)

    # --- Open ASKAP Catalogue ---
    print("Open ASKAP Catalogue - ", cat_file, sep=" ")
    srv = Table(parse_single_table(cat_file).array)
    num_in = len(srv)
    print("{:d} entries in ASKAP".format(num_in))
    offsets_all = Table()
    if num_in < 1:
        print('Primary catalogue empty')
        return num_in, offsets_all

    # --- Open Comparison survey ---
    print("Open Comparison Catalogue")
    infile_v = jfile
    infile = os.path.expandvars(infile_v)
    print(infile, infile.endswith('.csv'))
    if infile.endswith('.fits'):
        cat_tab = Table(fits.getdata(infile, ext=1))
    elif infile.endswith('.csv'):
        cat_tab = ascii.read(infile, format='csv')
    num_in = len(cat_tab)
    print("{:d} entries in {}".format(num_in, comp_survey))

    # --- Ensure isolated Catalogues ---
    # --- Survey Catalogue ---
    print("Find isolated sources in ASKAP Catalogue")
    c_srv_comp_iso, d_srv_comp, id_srv_comp = ast_self(srv[srv_ra], srv[srv_dec],
                                                       rad_isol, 'gt')
    srv_iso = srv[id_srv_comp]
    print("Isolated in ASKAP {:d}".format(len(id_srv_comp)))

    # --- Comparison Catalogue ---
    print("Find isolated sources in Comparison Catalogue")
    c_comp_iso, d_comp, id_comp = ast_self(cat_tab[cat_ra], cat_tab[cat_dec], rad_isol, 'gt')
    cat_iso = cat_tab[id_comp]
    print("Isolated in Comp {:d}".format(len(id_comp)))

    # --- Impose Other Cuts ---
    print("Impose Other Cuts on Sources")
    filt_snr = (srv_iso[srv_tflux] / srv_iso[srv_rms] >= snr_min)
    filt_r_lo = (srv_iso[srv_tflux] / srv_iso[srv_pflux] >= ares_min)
    filt_r_hi = (srv_iso[srv_tflux] / srv_iso[srv_pflux] <= ares_max)
    #         filt_tot = (srv_iso['col_' + srv_tflux_col] >= flux_rat)
    #         srv_iso = srv_iso[filt_snr & filt_r_lo & filt_r_hi & filt_tot]
    srv_iso = srv_iso[filt_snr & filt_r_lo & filt_r_hi]

    print("{:d} entries in ASKAP".format(len(srv_iso)))
    # --- Match two surveys ---
    print("Match Two Surveys")
    c_srv_c, c_r_comp, d2_r_c, id_srv_c, id_r_comp = ast(srv_iso[srv_ra],
                                                         srv_iso[srv_dec],
                                                         cat_iso[cat_ra],
                                                         cat_iso[cat_dec], rad_match, 1)
    #     print(c_srv_c.info())
    # --- Define Output matches ---
    if got_flux:
        flux_ratio_comp = 1.0
        print("Find Flux Ratios")
        tf_comp = cat_iso[cat_tflux][id_r_comp] / np.power(cat_freq / srv_freq,
                                                           alpha) * flux_ratio_comp
        tf_comp_orig = cat_iso[cat_tflux][id_r_comp] * flux_ratio_comp
        tf_srv = srv_iso[srv_tflux][id_srv_c]
        rms_srv = srv_iso[srv_rms][id_srv_c]

        flux_rat_comp = tf_srv / tf_comp
        flux_rat_comp_orig = tf_srv / tf_comp_orig

        srv_snr = tf_srv / rms_srv

    # --- Flux Ratio ASKAP/Comp ---
    print("Output Catalogue with Comparison")
    if len(c_srv_c) > 0:
        offsets_all['Component_ID'] = srv_iso[srv_ident][id_srv_c]
        offsets_all['RA'] = srv_iso[srv_ra][id_srv_c]
        offsets_all['DEC'] = srv_iso[srv_dec][id_srv_c]
        if got_flux:
            offsets_all['ASKAP_flux'] = tf_srv
            offsets_all['ASKAP_flux_SNR'] = srv_snr
        offsets_all['RA_comp'] = cat_iso[cat_ra][id_r_comp]
        offsets_all['DEC_comp'] = cat_iso[cat_dec][id_r_comp]
        if got_flux:
            offsets_all['Comp_flux'] = tf_comp_orig
            offsets_all['Flux_Ratio_AlphaCorr'] = flux_rat_comp
            offsets_all['Flux_Ratio_NOAlphaCorr'] = flux_rat_comp_orig

            print("Median Offset (with alpha corr): ", np.median(flux_rat_comp), "+",
                  np.percentile(flux_rat_comp, 84) - np.median(flux_rat_comp), "-",
                  np.median(flux_rat_comp) - np.percentile(flux_rat_comp, 16), sep=" ")
            print("Median Offset (without alpha corr): ", np.median(flux_rat_comp_orig), "+",
                  np.percentile(flux_rat_comp_orig, 84) - np.median(flux_rat_comp_orig), "-",
                  np.median(flux_rat_comp_orig) - np.percentile(flux_rat_comp_orig, 16), sep=" ")
    return num_in, offsets_all


# --- Define Astrometric matched ---

def ast(ra1, dec1, ra2, dec2, radius, nneigh):
    """
    Matches two catalogues within a certain angular separation
    * Uses input of ra/dec in degrees and radius in degrees
    * Output match has best matches for catalogue 1 and may have sources that \
        are matched to the same source in catalogue 2
    * Returns matched (within radius) skycoord array and distances
    
    :param ra1: Catalogue 1 RA (degrees)
    :param dec1: Catalogue 1 Dec (degrees)
    :param ra2: Catalogue 2 RA (degrees)
    :param dec2: Catalogue 2 Dec (degrees)
    :param radius: Angular separation (degrees) required for match
    :param nneigh: Which closest neighbor to search for: 1 (1st) or 2 (2nd).
    :return: c1_out Cat 1 coords of matched sources
             c2_out Cat 2 coords of matched sources
             d2_out Source angular separation (degrees)
             id_match_1 Indices in Cat 1
             id_match_2 Indices in Cat 2
    """

    c1 = SkyCoord(ra=ra1 * u.degree, dec=dec1 * u.degree)
    c2 = SkyCoord(ra=ra2 * u.degree, dec=dec2 * u.degree)

    id_m, d2_m, d3_m = c1.match_to_catalog_sky(c2, nthneighbor=nneigh)

    mk = d2_m.value <= radius / 3600.
    c1_out = c1[mk]
    c2_out = c2[id_m[mk]]
    d2_out = d2_m.value[mk]

    id_match_1 = np.arange(len(c1))[mk]
    id_match_2 = id_m[mk]

    return c1_out, c2_out, d2_out, id_match_1, id_match_2


def ast_self(ra1, dec1, radius, cmp):
    """
    Matches the same catalogues within a certain angular separation
    - Uses input of ra/dec in degrees and radius in arcsec
    - if type==gt then only keep those sources with matches father away,
    - if lt then chooses nearby matches
    """

    c1 = SkyCoord(ra=ra1 * u.degree, dec=dec1 * u.degree)

    id_m, d2_m, d3_m = c1.match_to_catalog_sky(c1, nthneighbor=2)
    if cmp == 'lt':
        mk = d2_m.value <= radius / 3600.
    elif cmp == 'gt':
        mk = d2_m.value >= radius / 3600.

    c1_out = c1[mk]
    d2_out = d2_m[mk]
    id_match = np.arange(len(c1))[mk]

    return c1_out, d2_out, id_match


def t_string(db_time):
    time_val = Time(db_time / 3600.0 / 24.0, format='mjd', scale='utc')
    time_val.format = 'iso'
    return "{}".format(time_val)


def my_grep(file_name, txt):
    lines = open(file_name, 'r').readlines()
    p = False
    for li in lines:
        q = True
        for t in txt:
            q = q and bool(re.search(t, li))
        p = p or q
    return p


def get_input(file_name, key):
    lines = open(file_name, 'r').readlines()
    lines = [li.strip() for li in lines]
    p = None
    for li in lines:
        if li.startswith(key):
            p = li.split('=')[1]
    return p


def find_parset(survey, inx):
    fn = survey.survey_files.file_name
    htmp = str(fn('imaging_parset', inx))
    possible = sorted(glob.glob(str(htmp)))
    parfile = possible[-1]
    return parfile
