#!/usr/bin/env python3
""" Grid holography data """
import sys
import numpy as np
import copy
import pkg_resources

from askap.footprint import Skypos
from aces.beamset.mapset import MapSet
from scipy.interpolate import Rbf
import aces.beamset.beamfactory as bf
import logging
from aces.holography import holo_filenames as hf
from aces.askapdata.schedblock import SchedulingBlock
import string

log = logging.getLogger(__name__)
from astropy.coordinates import SkyCoord, Angle, EarthLocation, AltAz
from astropy.time import Time
from astropy import units as u
from astropy.utils.iers import conf

conf.auto_max_age = None

# Catch annoying warnings
np.seterr(divide="ignore", invalid="ignore")


def get_antenna_locations(location_file):
    """Will parse a file the describes the location of the ASKAP antennas. This partticular files
    is newline delimited, with a separate line describing their wgs84 and itrf positions. This
    file returns their wgs84 position as an antenna ordered list of XYZ positions. 

    :param location_file: Path to 'antenna_positions_itrf.txt' file (packaged with aces.holography submodule. )
    :return: list of XYZ antenna positions, ordered by antenna number
    """
    lines = open(location_file, 'r').readlines()
    lines = [li.strip() for li in lines]
    aa = []
    a_loc = []
    for li in lines:
        if 'wgs84' in li:
            d = li.split('.')
            a = int(d[2][3:])
            i = li.index('[')
            d = li[i + 1:-1].split(',')
            lon = float(d[0])
            lat = float(d[1])
            # hgt = float(d[2])

            ASKAP_longitude = Angle(lon, unit=u.deg)
            ASKAP_latitude = Angle(lat, unit=u.deg)
            a_loc.append(EarthLocation(lat=ASKAP_latitude, lon=ASKAP_longitude))
            aa.append(a)

    list1, a_locs = zip(*sorted(zip(aa, a_loc)))

    return a_locs


def select_obs_radec(sbid):
    """
    Read pointing data extracted from ms tables, locate one point per grid point
    and return az,el for ref ant (az0, el0) az,el for another ant (aza,ela),
    RA,Dec for each, and the time (UTC).
    
    :param sbid: The sbid of the observation being processed
    :return: The RA and Dec positions the beams were pointed towards, and the times int UTC they were there
    """
    pointing = np.load("SB%d_beam00.pointing" % sbid, allow_pickle=True, encoding='bytes')
    time = np.load("SB%d_beam00.time" % sbid, allow_pickle=True, encoding='bytes')
    ra = pointing[:, :, 0]
    dec = pointing[:, :, 1]
    ij = ra.shape[0] // 36
    ra = ra.reshape(ij, 36)
    dec = dec.reshape(ij, 36)
    ant = 0
    tim = time.reshape(ij, 36)[:, ant]
    # Get one value for Time, RA, Dec from each scan
    wh = np.where(np.diff(dec[:, ant]) < -1.)[0]
    dw = 2
    #  return coordinate arrays with shapes [36, nx*nx]
    ra_s = ra[wh + dw].transpose()
    dec_s = dec[wh + dw].transpose()
    tim_s = tim[wh + dw]
    return ra_s, dec_s, tim_s


def dipa_to_lm(d, pa):
    """
    Given a distance, position_angle offset relative to a sky position,
    return the equivalent (l,m)

    :param d: distance
    :param pa:position_angle
    :return: rectangular offset - orthographic proejction

    """
    #
    x = np.sin(d) * np.sin(pa)
    y = np.sin(d) * np.cos(pa)
    return x, y


def get_true_azel(ra, dec, tim, ant_loc):
    """
    Given a sequence of celestial coordinates (ra, dec) and times, and the observer location,
    calculate the topcentric coordinates of each. Coordinates should be for J2000. Times should be UTC.
    The routine uses astropy procedures.
    :param ra: Sequence of right ascensions in radians
    :param dec: Sequence of declinations in radians
    :param tim: Sequence of times in seconds of MJD
    :param ant_loc: observer's location, geocentric in metres
    :return:
    """
    azt, elt = [], []
    for r, d, t in zip(ra, dec, tim):
        sc = SkyCoord(Angle(r, unit=u.rad), Angle(d, unit=u.rad))
        start_time = Time(t / 60.0 / 60.0 / 24.0, format='mjd', scale='utc', location=ant_loc)
        altaz = sc.transform_to(AltAz(obstime=start_time, location=ant_loc))
        azt.append(altaz.az.rad)
        elt.append(altaz.alt.rad)
    return np.array(azt), np.array(elt)


def get_obs_grid(az, el, refant):
    """

    :param az:
    :param el:
    :return:
    """
    # Construct positions for reference source, and boresight over all cycles
    arr = np.array
    ae_ants = arr([[Skypos(a, e) for a, e in zip(ai, ei)] for ai, ei in zip(az, el)])
    print('ae_ants shape ', ae_ants.shape)

    # compute bs position relative to ref in az-el frame
    # and 'x' and 'y' components x is horizontal, y is vertical
    # These, (bsx, bsy) over all cycles should fall on a square grid
    ae_ref = ae_ants[refant]
    bs_dpa = arr([[ref.d_pa(bs) for ref, bs in zip(ae_ref, ae_ant)] for ae_ant in ae_ants])
    sb_dpa = arr([[bs.d_pa(ref) for ref, bs in zip(ae_ref, ae_ant)] for ae_ant in ae_ants])
    sbx, sby = dipa_to_lm(sb_dpa[:, :, 0], sb_dpa[:, :, 1])

    return -sbx, -sby


def grid_corr(data, mapset, refant, ant_loc):
    """
    Regrids the sampled data onto the intended grid on the sky.
    The input data should be in its native form (not subjected to sky_transform)

    :param data: Holography complex voltages in mapset formatted array
    :param mapset: mapset object holding this dataset
    :param refant: Reference antenna; if None, retrieved from SB database
    :param ant_loc Antenna locations
    :return: regridded data
    """

    sbid = mapset.metadata['holographySBID']
    # Select an antenna that was used, but not the refant
    # The commanded pointing for all test antennas should be the same.
    antennas = [a - 1 for a in mapset.metadata['antennas']]

    ra, dec, tim = select_obs_radec(sbid)

    log.info("Got pointing data")
    n = len(ra)
    if np.sqrt(n) % 1.0 != 0.0:
        log.warning('Grid not square? Has {:d} points'.format(n))
        data_i = None
        return data_i

    az_true, el_true = np.zeros(ra.shape), np.zeros(ra.shape)
    for a in antennas:
        ae = get_true_azel(ra[a], dec[a], tim, ant_loc[a])
        az_true[a], el_true[a] = ae

    # Construct  the intended sampling grid
    nx = mapset.payloadShape[0]
    x0, x1 = mapset.metadata['xAxis'][0], mapset.metadata['xAxis'][-1]
    y0, y1 = mapset.metadata['yAxis'][0], mapset.metadata['yAxis'][-1]
    xh = np.linspace(x0, x1, nx)
    yh = np.linspace(y0, y1, nx)
    # Note that we need to reverse (transpose) x and y here to align our grid points with the
    # sequence of measurement points.
    yg, xg = np.meshgrid(xh, yh)

    sbx, sby = get_obs_grid(az_true, el_true, refant)

    sh = data.shape
    Q = np.product(sh[2:5])
    sh2 = [sh[1], Q, sh[-2], sh[-1]]

    data = data.reshape(sh2)
    data_i = np.zeros(sh2, dtype=complex)

    # Skip reference antenna
    ants = [a for a in range(sh2[0]) if a != refant]
    for ant in ants:
        for j in range(sh2[1]):
            im = data[ant, j]
            if np.isnan(im.sum()):
                pass
            else:
                interp_func = Rbf(sbx[ant], sby[ant], im, function='cubic', smooth=0)
                im_gr = interp_func(xg, yg)
                data_i[ant, j] = im_gr
    
    data_i = data_i.reshape(sh)

    return data_i


def raw_to_grid(raw_file_name, beam, refant, ant_loc):
    """
    Reads holography data in hdf5 MapSet format. Performs operations on the
    data hyper-cube:
    * interpolates data onto regular grid
    * saves gridded data for the given beam in hdf5 MapSet format
    
    :param raw_file_name: (str) Name of hdf5 holography data file
    :param beam: (int) Beam number to process (0-based)
    :param refant: (int) Antenna number to use for grid reference (0-based)
    :param ant_loc Antenna locations
    """
    # Load holography data: mso.data in ndarray
    mso = bf.load_beamset_class(raw_file_name)
    if mso.metadata['holographySBID'] == 21613:
        products_e = np.array(mso.data)[:, :, beam:beam + 1, :, :, ::-1, :].transpose()
        log.info("Got data for beam {:d} (21613)".format(beam))

        products = grid_corr(products_e, mso, refant, ant_loc)[:, :, :, :, :, ::-1, :].transpose()
    else:
        products_e = np.array(mso.data)[:, :, beam:beam + 1]
        log.info("Got data for beam {:d}".format(beam))

        products = grid_corr(products_e, mso, refant, ant_loc)

    del products_e
    # products = grid_corr(products_e, mso)
    flags_xy = np.array(mso.flags)[:, :, beam:beam + 1]
    if flags_xy.ndim == 7:
        flags = flags_xy.all(axis=(-2, -1))
    else:
        flags = flags_xy

    del flags_xy

    log.debug(f'Flag shape: {flags.shape}')

    log.info("Grid corrected")

    md = copy.deepcopy(mso.metadata)
    md['beams'] = np.array([beam + 1])
    mso_grid = MapSet(metadata=md,
                      data=products,
                      flags=flags,
                      filename=None
                      )
    del products, flags, mso
    mso_grid.add_to_history('Resampled onto grid')

    return mso_grid


def main(sbid,
         beam,
         holo_dir='.',
         refant=None,
         ):
    """Main script

    :param sbid: SBID
    :type sbid: int
    :param beam: beam number
    :type beam: int
    :param holo_dir: directory holding holograophy data
    :type holo_dir: str
    :param refant: (int) Antenna number to use for grid reference (0-based)
    """
    
    log.info(f"Starting grid_holography on SBID {sbid:d}")
    # Clean up dir
    if holo_dir[-1] == '/':
        holo_dir = holo_dir[:-1]

    if refant is None:
        sb = SchedulingBlock(sbid)
        ak_ref = int(''.join(filter(lambda char: char in string.digits,
                                    sb.get_parameters()['holography.ref_antenna'])))
        refant = ak_ref - 1  # 0-based
        log.info("Automatically selecting antenna AK{:02d} to use for grid definition".format(refant))

    location_file = pkg_resources.resource_filename("aces.holography", "antenna_positions_itrf.txt")
    log.info(f"Loading {location_file=}")
    
    antenna_locations = get_antenna_locations(location_file)

    in_name = hf.find_holo_file(holo_dir, pol='xxyy', sbid=sbid, kind='hdf5')

    mso_grid = raw_to_grid(in_name, beam, refant, antenna_locations)
    log.debug(f'Flag shape: {mso_grid.flags.shape}')
    # out_name = f'{holo_dir}/{sbid:d}_Holo_grid_{beam:02d}.hdf5'
    kind = f'grid.beam{beam:02d}.hdf5'
    out_name = f'{holo_dir}/{hf.make_file_name(mso_grid, kind=kind)}'

    mso_grid.write_to_hdf5(out_name)
    del mso_grid

    log.info("All finished")


def cli():
    import argparse
    """
    Command line interface
    """

    # Help string to be shown using the -h option
    descStr = """
    Clean holography data
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
        '-b',
        dest='beam',
        type=int,
        default=None,
        help='Beam to process. No default')

    parser.add_argument(
        '-d',
        dest='holo_dir',
        type=str,
        default='.',
        help='Directory containing holography data [./].')

    parser.add_argument(
        '-a',
        '--refant',
        type=int,
        default=None,
        help='Antenna to use for grid reference - specify to override [ref. ant. + 1].'
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
         beam=args.beam,
         holo_dir=args.holo_dir,
         refant=args.refant
         )


if __name__ == "__main__":
    sys.exit(cli())
