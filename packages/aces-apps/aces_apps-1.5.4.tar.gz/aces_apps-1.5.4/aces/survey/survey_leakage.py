#!/usr/bin/env python

import numpy as np

from astropy.io import fits
from astropy.table import Table
from astropy.coordinates import SkyCoord
from astropy import units as u
from astropy.wcs import WCS
from astropy.stats import sigma_clip

KEEP_COLUMNS = {
    "ra_deg_cont": "StokesI_RA",
    "dec_deg_cont": "StokesI_DEC",
    "flux_peak": "StokesI_flux_peak",
    "flux_int": "StokesI_flux_int",
    "rms_image": "StokesI_image_rms",
    "component_id": "Component_ID"
}

class StokesData():
    """Class to extract and hold Stokes Q, U, or V leakage data."""
    def __init__(self, catalogue_i, image_p,
        ra_key="ra",
        dec_key="dec",
        multiplier=1.):
        """
        Parameters
        ----------
        catalogue_i : str
            Filename for Stokes I catalogue. Normally the Selavy catalogue.
        image_p : str
            Filename for Stokes Q, U, or V image.
        ra_key : str, optional
            Name of RA key in catalogue. [Default 'ra']
        dec_key : str, optional
            Name of dec. key in catalogue. [Default 'dec']
        multiplier : float, optional
            Value to multiply catalogue flux densities by. Note for Selavy this should
            be set to 1e-3 as Selavy by default reports in mJy. [Default 1.0]

        """

        if catalogue_i.lower().endswith(".fits"):
            table_format = "fits"
        elif catalogue_i.lower().endswith(".vot") or catalogue_i.lower().endswith(".xml"):
            table_format = "votable"
        else:
            table_format = None

        self.catalogue_i = Table.read(catalogue_i, format=table_format)
        self.image_p = fits.open(image_p)
        self.header = self.image_p[0].header
        self.wcs = WCS(self.header).celestial
        self.data = np.squeeze(self.image_p[0].data)
        self.multiplier = multiplier
        abs_clipped = sigma_clip(np.abs(self.data), 
            sigma=5, 
            maxiters=3, 
            masked=False, 
            axis=(0, 1)
        )
        self.data_clipped = self.data.copy()
        self.data_clipped[np.isnan(abs_clipped)] = np.nan
        self.noise = np.nanstd(self.data_clipped)
        print("Stokes V sigma-clipped map stddev.: {}".format(
            self.noise
        ))
        try:
            self.coords = SkyCoord(
                ra=self.catalogue_i[ra_key]*u.deg,
                dec=self.catalogue_i[dec_key]*u.deg
            )
        except Exception:
            self.coords = SkyCoord(
                ra=self.catalogue_i[ra_key],
                dec=self.catalogue_i[dec_key]
            )


    def get_isolated(self, zone=0.0055):
        """Get isolated sources. A clipped version of the original catalogue is made.
        
        Parameters
        ----------
        zone : float, optional
            Sources within `zone` of each other are excluded, in degrees. [Default 0.0055]
            
        """
        idx, seps, _ = self.coords.match_to_catalog_sky(self.coords, 
            nthneighbor=2
        )
        isolated = np.where(seps.value > zone)[0]
        print("Isolated fraction: {}".format(
            len(isolated) / len(self.catalogue_i) 
        ))
        self.catalogue_i = self.catalogue_i[isolated]
        self.coords = self.coords[isolated]


    def get_compact(self, 
        ratio=(0.83, 1.2), 
        int_flux="int_flux",
        peak_flux="peak_flux"
        ):
        """Get compact sources. A clipped version of the catalogue is made.
        
        Parameters
        ----------
        ratio : tuple, float, optional
            Tuple of minimum and maximum flux density ratios. [Default (0.83, 1.2)]
        int_flux : str, optional    
            Column name for integrated/total flux density in Stokes I catalogue. [Default 'int_flux']
        peak_flux : str, optional
            Column name for peak flux in Stokes I catalogue. [Default 'peak_flux']

        
            """
        self.peak_flux = peak_flux
        self.int_flux = int_flux
        over_cond = self.catalogue_i[int_flux] / self.catalogue_i[peak_flux] > ratio[0]
        under_cond = self.catalogue_i[int_flux] / self.catalogue_i[peak_flux] < ratio[1]
        compact = np.where(over_cond & under_cond)[0]
        self.catalogue_i = self.catalogue_i[compact]
        self.coords = self.coords[compact]


    def get_xycoords(self):
        """Get sources coordinates in pixel x, y coordinates."""
        self.x, self.y = self.wcs.all_world2pix(self.coords.ra, self.coords.dec, 0)
        self.x = self.x.astype(int)
        self.y = self.y.astype(int)


    def get_leakage(self, 
        local_rms="local_rms", 
        sigma=0, 
        search_box=1,
        noise_box=20):
        """Get leakage from polarization image.
        
        Parameters
        ----------
        local_rms : str, optional
            Column name for image rms. [Default 'local_rms']
        sigma : int, optional
            Minimum Stokes I SNR required. [Default 10]
        search_box : int, optional
            Look for peak Stokes Q/U/V in expanded box around Stokes I position. 
            [Default 1]
        noise_box : int, optional
            Use for noise calculations and reject sources <= `noise_box` of a NaN pixel, 
            likely image edge. [Default 20]

        """
        self.local_rms = local_rms
        self.sigma = sigma

        p_over_i = []
        pols = []
        rmses = []

        for i in range(len(self.coords)):

            try:

                if np.isnan(
                    self.data[
                        self.y[i]-noise_box:self.y[i]+noise_box, 
                        self.x[i]-noise_box:self.x[i]+noise_box
                    ].flatten()).any():
                    raise ValueError

                cutout = self.data[
                    self.y[i]-search_box:self.y[i]+search_box, 
                    self.x[i]-search_box:self.x[i]+search_box
                ].flatten()
                cutout_noise = self.data_clipped[
                    self.y[i]-noise_box:self.y[i]+noise_box, 
                    self.x[i]-noise_box:self.x[i]+noise_box
                ].flatten()
                pol = cutout[np.nanargmax(np.abs(cutout))]
                rms = np.nanstd(cutout_noise)
            except (IndexError, ValueError):
                pol = np.nan 
                rms = np.nan

            if self.catalogue_i[self.peak_flux][i] / self.catalogue_i[local_rms][i] > sigma:
                pi = pol / (self.catalogue_i[self.peak_flux][i] * self.multiplier)
            else:
                pi = np.nan

            p_over_i.append(pi)
            pols.append(pol)
            rmses.append(rms)

        self.pols = np.asarray(pols) / self.multiplier
        self.p_over_i = np.asarray(p_over_i)
        self.rms = np.asarray(rmses) / self.multiplier


    def get_table_leakage(self, outname=None, remove_cols=True, prefix="",
        pol="v"):
        """Add leakage columns to a table, clip NaNs, writeout?
        
        Parameters
        ----------
        outname : str, optional
            Output filename. If supplied a .csv file is written. [Default None]
        remove_cols : bool, optional
            Remove all columns from the subject catalogue that do not belong to the KEEP_COLUMNs set. [Default True]
        prefic : str, optional
            If this prefix exists for the name of a column, it is ignored when deciding whether to remove columns. [Default ""]
        """
        
        polname = "Stokes{}".format(pol.upper())

        if remove_cols:
            catalogue_columns = self.catalogue_i.columns.copy()
            for col in catalogue_columns:
                if col.replace(prefix, "") not in KEEP_COLUMNS.keys():
                    self.catalogue_i.remove_column(col)
                else:
                    self.catalogue_i[col].name = KEEP_COLUMNS[col.replace(prefix, "")] 
        
        self.catalogue_i.add_columns(
            cols=[self.x, self.y, self.p_over_i, self.pols, self.rms],
            names=[
                "StokesI_x", 
                "StokesI_y", 
                polname + "_leakage",
                polname + "_flux_peak", 
                polname + "_image_rms"
            ],
        )
        self.catalogue_i = self.catalogue_i[np.where(np.isfinite(self.catalogue_i[polname + "_leakage"]))[0]]
        

        if outname is not None:
            self.catalogue_i.write(outname, format="ascii", delimiter=",", overwrite=True)
