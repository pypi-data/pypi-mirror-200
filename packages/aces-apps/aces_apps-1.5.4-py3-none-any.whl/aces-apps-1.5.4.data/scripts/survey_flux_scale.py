# --- Import packages ----
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import sys
# from tqdm import tqdm
from glob import glob
import os
from astropy.io import fits, ascii
from astropy.table import Table, vstack, hstack, Column, join, unique
from astropy.coordinates import SkyCoord
from astropy import units as u
from astropy.wcs import WCS
from matplotlib import cm
import argparse
from astropy.io.votable import parse_single_table
from astropy.utils.exceptions import AstropyWarning
import warnings

warnings.simplefilter('ignore', category=AstropyWarning)


def args_init():
    parser = argparse.ArgumentParser(description='Compare Fluxes')
    parser.add_argument('--sfile', type=str, help='Settings File')
    parser.add_argument('--file', type=str, help='Components File to Compare')
    parser.add_argument('--comp', type=str, help='Comparison Survey Name (SUMSS or NVSS)')
    return parser


# --- Define Astrometric matched ---

def ast(ra1, dec1, ra2, dec2, radius, nneigh):
    '''Matches two catalogues within a certain angular separation
    - Uses input of ra/dec in degrees and radius in arcsec
    - Output match has best matches for catalogue 1 and may have sources that
        are matched to the same source in catalogue 2
    - Returns matched (within radius) skycoord array and distances'''

    c1 = SkyCoord(ra=ra1 * u.degree, dec=dec1 * u.degree)
    c2 = SkyCoord(ra=ra2 * u.degree, dec=dec2 * u.degree)

    id_m, d2_m, d3_m = c1.match_to_catalog_sky(c2, nthneighbor=nneigh)

    c1_out = c1[d2_m.value <= radius / 3600.]
    c2_out = c2[id_m[d2_m.value <= radius / 3600.]]
    d2_out = d2_m.value[d2_m.value <= radius / 3600.]

    id_match_1 = np.arange(len(c1))[d2_m.value <= radius / 3600.]
    id_match_2 = id_m[d2_m.value <= radius / 3600.]

    return c1_out, c2_out, d2_out, id_match_1, id_match_2


def ast_self(ra1, dec1, radius, type):
    '''Matches the same catalogues within a certain angular separation
    - Uses input of ra/dec in degrees and radius in arcsec
    - if type==gt then only keep those sources with matches father away,
    - if lt then chooses nearby matches'''

    c1 = SkyCoord(ra=ra1 * u.degree, dec=dec1 * u.degree)

    id_m, d2_m, d3_m = c1.match_to_catalog_sky(c1, nthneighbor=2)
    if type == 'lt':
        c1_out = c1[d2_m.value <= radius / 3600.]
        d2_out = d2_m[d2_m.value <= radius / 3600.]
        id_match = np.arange(len(c1))[d2_m.value <= radius / 3600.]
    elif type == 'gt':
        c1_out = c1[d2_m.value >= radius / 3600.]
        d2_out = d2_m[d2_m.value >= radius / 3600.]
        id_match = np.arange(len(c1))[d2_m.value >= radius / 3600.]

    return c1_out, d2_out, id_match


def offsets_all(cat_file, comp_survey, settings):
    kw = {}
    for i in range(len(settings['Name'])):
        if settings['Type'][i] == 's':
            kw['%s' % settings['Name'][i]] = settings['Value'][i]
        if settings['Type'][i] == 'f':
            kw['%s' % settings['Name'][i]] = float(settings['Value'][i])
        if settings['Type'][i] == 'i':
            kw['%s' % settings['Name'][i]] = int(settings['Value'][i])

    racs_ra_col = kw['racs_ra_col']
    racs_dec_col = kw['racs_dec_col']
    racs_pflux_col = kw['racs_pflux_col']
    racs_comp_id_col = kw['racs_comp_id_col']
    racs_tflux_col = kw['racs_tflux_col']
    racs_pflux_col = kw['racs_pflux_col']
    racs_rms_col = kw['racs_rms_col']
    racs_maj_col = kw['racs_maj_col']
    snr_ratio_cut = kw['snr_ratio_cut']
    flux_int_peak_min = kw['flux_int_peak_min']
    flux_int_peak_max = kw['flux_int_peak_max']
    flux_rat = kw['flux_rat']
    isolated_radius = kw['isolated_radius']
    match_radius = kw['match_radius']
    freq_racs = kw['freq_racs']
    alpha = kw['alpha']
    folder_comp = kw['folder_comp']

    # --- Open RACS Catalogue ---
    print("Open RACS Catalogue - ", cat_file, sep=" ")
    racs = Table(parse_single_table(cat_file).array)
    print("{:d} entries in RACS".format(len(racs)))
    offsets_all = Table()

    # --- Open Comparison survey ---
    print("Open Comparison Catalogue")
    dat_comp = Table(fits.getdata(str(settings['Value'][int(
        np.where(settings['Name'] == comp_survey + '_f')[0])]), ext=1))
    freq_dat_comp = float(settings['Value'][int(np.where(
        settings['Name'] == 'freq_' + comp_survey)[0])])
    dat_comp_ra_col = str(settings['Value'][int(np.where(
        settings['Name'] == comp_survey + '_ra_col')[0])])
    dat_comp_dec_col = str(settings['Value'][int(np.where(
        settings['Name'] == comp_survey + '_dec_col')[0])])
    dat_comp_tflux_col = str(settings['Value'][int(np.where(
        settings['Name'] == comp_survey + '_tflux_col')[0])])
    flux_ratio_comp = float(settings['Value'][int(np.where(
        settings['Name'] == comp_survey + '_flux_ratio')[0])])
    print("{:d} entries in {}".format(len(dat_comp), comp_survey))
    # --- Ensure isolated Catalogues ---
    # --- Comparison Catalogue ---
    print("Find isolated sources in Comparison Catalogue")
    c_comp_iso, d_comp, id_comp = ast_self(dat_comp[dat_comp_ra_col],
                                           dat_comp[dat_comp_dec_col], isolated_radius, 'gt')
    dat_comp_iso = dat_comp[id_comp]

    # --- RACS Catalogue ---
    print("Find isolated sources in RACS Catalogue")
    c_racs_comp_iso, d_racs_comp, id_racs_comp = ast_self(racs['col_' + racs_ra_col],
                                                          racs['col_' + racs_dec_col], isolated_radius, 'gt')
    racs_iso = racs[id_racs_comp]

    # --- Impose Other Cuts ---
    print("Impose Other Cuts on Sources")
    racs_iso = racs_iso[(racs_iso['col_' + racs_pflux_col] / racs_iso['col_' + racs_rms_col] >= snr_ratio_cut)
                        & (racs_iso['col_' + racs_tflux_col] / racs_iso['col_' + racs_pflux_col] >= flux_int_peak_min)
                        & (racs_iso['col_' + racs_tflux_col] / racs_iso['col_' + racs_pflux_col] <= flux_int_peak_max)
                        & (racs_iso['col_' + racs_tflux_col] >= flux_rat)]
    print("{:d} entries in RACS".format(len(racs_iso)))
    # --- Match two surveys ---
    print("Match Two Surveys")
    c_racs_c, c_r_comp, d2_r_c, id_racs_c, id_r_comp = ast(racs_iso['col_' + racs_ra_col],
                                                           racs_iso['col_' + racs_dec_col],
                                                           dat_comp_iso[dat_comp_ra_col],
                                                           dat_comp_iso[dat_comp_dec_col], match_radius, 1)
    print(c_racs_c.info())
    # --- Define Output matches ---
    print("Find Flux Ratios")
    tf_comp = dat_comp_iso[dat_comp_tflux_col][id_r_comp] * np.power(freq_dat_comp / freq_racs, alpha) * flux_ratio_comp
    tf_comp_orig = dat_comp_iso[dat_comp_tflux_col][id_r_comp] * flux_ratio_comp
    tf_racs = racs_iso['col_' + racs_tflux_col][id_racs_c]

    flux_rat_comp = tf_racs / tf_comp
    flux_rat_comp_orig = tf_racs / tf_comp_orig

    # --- Flux Ratio RACS/Comp ---
    print("Output Catalogue with Comparison")
    offsets_all['Component_ID'] = racs_iso['col_' + racs_comp_id_col][id_racs_c]
    offsets_all['RA'] = racs_iso['col_' + racs_ra_col][id_racs_c]
    offsets_all['DEC'] = racs_iso['col_' + racs_dec_col][id_racs_c]
    offsets_all['RACS_flux'] = tf_racs
    offsets_all['RA_comp'] = dat_comp_iso[dat_comp_ra_col][id_r_comp]
    offsets_all['DEC_comp'] = dat_comp_iso[dat_comp_dec_col][id_r_comp]
    offsets_all['Comp_flux'] = tf_comp_orig
    offsets_all['Flux_Ratio_AlphaCorr'] = flux_rat_comp
    offsets_all['Flux_Ratio_NOAlphaCorr'] = flux_rat_comp_orig

    offsets_all.write(folder_comp + '/Offsets_all_' + cat_file[:-4] + '.fits', overwrite=True)
    print("Median Offset (with alpha corr): ", np.median(flux_rat_comp), "+",
          np.percentile(flux_rat_comp, 84) - np.median(flux_rat_comp), "-",
          np.median(flux_rat_comp) - np.percentile(flux_rat_comp, 16), sep=" ")
    print("Median Offset (without alpha corr): ", np.median(flux_rat_comp_orig), "+",
          np.percentile(flux_rat_comp_orig, 84) - np.median(flux_rat_comp_orig), "-",
          np.median(flux_rat_comp_orig) - np.percentile(flux_rat_comp_orig, 16), sep=" ")


def main():
    args = args_init().parse_args()

    # ---- Load in Settings file ----
    settings_file = args.sfile
    settings = ascii.read(settings_file, format='commented_header')

    offsets_all(args.file, args.comp, settings)


if __name__ == "__main__":
    sys.exit(main())
