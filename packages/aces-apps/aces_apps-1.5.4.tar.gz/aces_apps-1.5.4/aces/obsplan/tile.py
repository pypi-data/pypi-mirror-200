#!/usr/bin/env python
"""
 Routines to support tiling the spherical sky.

"""

import numpy as np

from numpy import pi, sin, cos, arctan2
from numpy import linalg
import math

from askap.footprint import Skypos
from aces.obsplan.config import ACESConfig

ster_to_sqdeg = (180.0 / pi) ** 2
twopi = 2.0 * pi

overlay_format = {'ds9': "polygon {:9f} {:9f}, {:9f} {:9f}, {:9f} {:9f}, {:9f} {:9f}\n",
                  'kvis': "CLINES {:9f} {:9f}, {:9f} {:9f}, {:9f} {:9f}, {:9f} {:9f}, {:9f} {:9f}\n"}

overlay_label_format = {'ds9': "text {:f} {:f} {}\n",
                        'kvis': "TEXT {:f} {:f} {}\n"}


def prefix(word, pfx):
    """
    Add a prefix to a word, unless it is already present.
    :param word: The string to be prefixed
    :param pfx: The prefix
    :return: The prefixed word.
    """
    if word.startswith(pfx):
        return word
    else:
        return pfx + word


class Tile(object):
    """
    The Tile object represents a single tile, uniquely defined within a set by location on the celestial
    sphere, and position angle. All tiles share parameters that are set in the initialise class method that must
    be called before any Tile object can be created.
    
    :param ident: Integer identifier
    :type ident: int
    :param lon: tile position in longitude (radians)
    :type lon: float
    :param lat: tile position in latitude (radians)
    :type lat: float
    :param posang:  tile position angle (degrees)
    :type posang: float

    """
    n_pole = {'J2000': Skypos(0.0, pi / 2.),
              'GALAC': Skypos('12:51:26.279', '27:07:42.07'),
              'MAGEL': Skypos('12:34:00.000', '-07:30:00.00')}

    l0 = {'J2000': 0.0,
          'GALAC': 122.9320,
          'MAGEL': 122.7242}

    euler_zxz = {'J2000': np.array([n_pole['J2000'].ra, n_pole['J2000'].dec, pi]),
                 'GALAC': np.array([n_pole['GALAC'].ra, n_pole['GALAC'].dec, l0['GALAC'] * pi / 180.]),
                 'MAGEL': np.array([n_pole['MAGEL'].ra, n_pole['MAGEL'].dec, l0['MAGEL'] * pi / 180.])}

    origin = Skypos(0.0, 0.0)
    quadrant_select = np.array([[1.0, 1.0], [1.0, -1.0], [-1.0, -1.0], [-1.0, 1.0]])

    trans_matrices = {}
    centre_matrix = None
    label = ""
    bf_pa = 0.0
    coord = 'J2000'
    footprint = None
    fp_factory = None

    # In production code the following need to come from the proper place.
    # -26d 58m 59.99s
    MRO_latitude = np.radians(-(26.0 + 59. / 60))
    za_limit = np.radians(75.0)
    northern_limit = MRO_latitude + za_limit

    @classmethod
    def initialise(cls, origin, label, footprint, bf_pa, coord='J2000'):
        """
        Initialise the class variables for all subsequent creations of Tile objects.
        :param origin: Centre of tile sphere in given coordinates as Skypos
        :type origin: Skypos
        :param label: Label for tiling; used in names of all related product files
        :type label: string
        :param footprint: Footprint object used for this tiling
        :type footprint: Footprint
        :param bf_pa: beam-forming position angle (degrees)
        :type bf_pa: float
        :param coord: Name of coordinates of tiling ('J2000', 'GALAC', 'MAGEL')
        :type coord string

        """
        cls.origin = origin
        cls.label = label
        cls.footprint = footprint
        cls.bf_pa = bf_pa
        cls.coord = coord

        lon, lat = cls.origin.ra, cls.origin.dec
        ca, sa = np.cos(lon), np.sin(lon)
        cb, sb = np.cos(lat), np.sin(lat)
        Tile.centre_matrix = np.array([[ca * cb, -sa, -ca * sb], [sa * cb, ca, -sa * sb], [sb, 0.0, cb]])
        for k, v in cls.euler_zxz.items():
            cls.trans_matrices[k] = rotmat(v)
        cls.trans_matrices['MAGEL'] = np.dot(cls.trans_matrices['GALAC'], cls.trans_matrices['MAGEL'])

        aces_cfg = ACESConfig()
        cls.fp_factory = aces_cfg.footprint_factory

    def __init__(self, ident, lon, lat, posang):
        """
        Initialise a Tile object. The input positions are in the coordinate frame declared in the class
        initialisation routine.
        :param ident: Integer identifier
        :param lon: tile position in longitude (radians)
        :param lat: tile position in latitude (radians)
        :param posang:  tile position angle (degrees)
        """
        if Tile.footprint is None:
            print("FAIL - no init done yet")
        self.ident = ident
        self.lon_r = lon
        self.lat_r = lat
        self.native_posang = posang
        self.long = np.degrees(lon)
        self.lat = np.degrees(lat)

        coord = Tile.coord
        self.skypos = Skypos(self.lon_r, self.lat_r)
        if coord not in Tile.euler_zxz.keys():
            print('unknown coord')
        trans_matrix = np.dot(Tile.trans_matrices[coord], Tile.centre_matrix)
        n_pole = Tile.n_pole['J2000']
        n_pole = transform(n_pole, trans_matrix)
        self.native = transform(self.skypos, Tile.centre_matrix)
        self.j2000 = transform(self.skypos, trans_matrix)
        self.posang_r = self.j2000.d_pa(n_pole)[1] + np.radians(self.native_posang)

        self.ra_r = self.j2000.ra
        self.dec_r = self.j2000.dec
        self.ra = np.degrees(self.ra_r)
        self.dec = np.degrees(self.dec_r)
        self.posang = np.degrees(self.posang_r)
        self.name = self._make_name()
        self.full_name = Tile.label + '_' + self.name
        self.corners = self._get_corners()
        self.corners_deg = np.degrees(np.array([(p.ra, p.dec) for p in self.corners]))

        name = prefix(Tile.footprint.name, 'ak:')
        p = Tile.footprint.pitch_scale
        angle = self.posang_r

        self.footprint = Tile.fp_factory.make_footprint(name, p, angle=angle)
        self.footprint.set_refpos([self.ra_r, self.dec_r])
        self.interleaves = self.footprint.get_interleaves()
        self.interleaves_pa = self.footprint.get_interleave_pa()

    def __str__(self):
        """

        :return: A formatted string giving tile id, celestial position and position angle
        """
        s = "{:d} {:f} {:f} {:f}".format(self.ident, self.ra, self.dec, self.posang)
        return s

    def check_accessible(self):
        """
        This function is trivial: it checks for tile positions beyond ASKAP's northern limit. But
        could be extended to incorporate additional position constraints.
        :return: Whether a tile at this position is accessible by ASKAP.
        """
        ret = (self.dec_r < Tile.northern_limit)

        return ret

    def get_overlay(self, kind="ds9"):
        """
        Returns a string suitable for overlaying the tile outline on sky maps. Supported kinds are ds9
        (works with aladin) and kvis. The string can be written to a file to be presented to  image display program.
        :param kind: "ds9" or "kvis"
        :return: A formatted string describing the tile outline in the requested format.
        """
        ret = overlay_format[kind]
        c = self.corners_deg
        wlim = 8.0 / np.cos(self.dec_r)
        for cj in c:
            ci = cj.copy()
            if ci[0] - self.ra > wlim:
                ci[0] = 0.0
            if self.ra - ci[0] > wlim:
                ci[0] = 359.99

        rets = ret.format(c[0, 0], c[0, 1], c[1, 0], c[1, 1], c[2, 0], c[2, 1], c[3, 0], c[3, 1], c[0, 0], c[0, 1])
        return rets

    def get_overlay_label(self, label, kind='ds9'):
        """
        Returns a string suitable for overlaying the given label on sky maps and the current tile position. Supported
        kinds are ds9 (works with aladin) and kvis. The string can be written to a file to be presented to  image
        display program.

        :param label: The label
        :param kind:  "ds9" or "kvis"
        :return: A formatted string giving label and its position in correct format
        """
        ret = overlay_label_format[kind]
        rw, rm = self._get_ra_mid_wid()
        ra = rm + rw / 4.
        rets = ret.format(ra, self.dec, label)
        return rets

    def get_footprint_cmd(self, kind='ds9'):
        """
        Returns a command line string that will execute the footprint-plan.py script that produces plots and
        overlays of the beam positions within a footprint. For example:

        footprint-plan.py -n ak:square_6x6 -p 0.9 -r 141.382178,-37.100000 -o 141-37 -f kvis -w 0.9
        :return: The command line string.
        """
        # footprint-plan.py -n ak:square_6x6 -p 0.9 -r 141.382178,-37.100000 -o 141-37 -f kvis -w 0.9
        ret = "footprint-plan.py -n {} -p {:.2f} -a {:f} -r {:f},{:f} -o {} -f {} -w {:.2f}\n"
        fp = self.footprint
        rets = ret.format('ak:' + fp.name, np.degrees(fp.pitch_scale), self.posang, self.ra, self.dec, self.full_name,
                          kind, np.degrees(fp.pitch_scale))
        return rets

    def get_parset_entry(self, with_interleave=True):
        """
        Returns the parset entries for observing this tile, and optionally, the interleaved positions.  The entry keys
        are
        * common.target.src%d.field_direction
        * common.target.src%d.field_name
        * common.target.src%d.pol_axis
        The "%d" formatting code is replaced by the tile identifier number elsewhere.
        
        :param with_interleave:
        :return: A list of strings, each of the form <key> = <value>
        """
        # interim to get us going
        ret_abc = {'A': []}
        rets = ret_abc['A']
        ras = self.j2000.get_ras()
        decs = self.j2000.get_decs()
        ret = "common.target.src%d.field_direction = [{}, {}, J2000]"
        rets.append(ret.format(ras, decs))
        ret = "common.target.src%d.field_name = {}"
        full_name = self.full_name
        if with_interleave:
            full_name += 'A'
        rets.append(ret.format(full_name))
        ret = "common.target.src%d.pol_axis = [pa_fixed, {:.4f}]"
        val = self._set_posang_deg()
        rets.append(ret.format(val))
        if with_interleave:
            for label, i_pos, pa in zip(['B', 'C', 'D'], self.interleaves, self.interleaves_pa):
                ret_abc[label] = []
                rets = ret_abc[label]
                ras = i_pos.get_ras()
                decs = i_pos.get_decs()
                ret = "common.target.src%d.field_direction = [{}, {}, J2000]"
                rets.append(ret.format(ras, decs))
                ret = "common.target.src%d.field_name = {}"
                rets.append(ret.format(self.full_name + label))
                ret = "common.target.src%d.pol_axis = [pa_fixed, {:.4f}]"
                val = self._set_posang_deg() + pa * 180.0 / pi
                rets.append(ret.format(val))

        return ret_abc

    def get_corners(self):
        """
        Returns the sky coordinates in the J2000 celestial coordinate frame of each corner for this tile.
        :return: ndarray of Skypos objects holding the four corner coordinates.
        """
        cs = np.array(self.corners)
        return cs

    def get_poly(self):
        """
        Returns the sky coordinates in the J2000 celestial coordinate frame of each corner for this tile.
        :return: list of Skypos objects holding the four corner coordinates.
        """
        p0 = Skypos(self.ra_r, self.dec_r)
        dx, dy = np.diag(np.array(self.footprint.get_tile_offsets()))
        diag = np.sqrt(dx ** 2 + dy ** 2) * 0.5
        theta1 = np.arctan2(dx, dy)
        thetas = np.array([theta1, pi - theta1, pi + theta1, 2.0 * pi - theta1]) + self.posang_r
        pj = [p0.offset([diag, th]) for th in thetas]
        return pj

    def get_poly_native(self):
        """
        Returns the sky coordinates in the user-specified tiling coordinate frame of each corner for this tile.
        :return: list of Skypos objects holding the four corner coordinates.
        """
        p0 = Skypos(self.lon_r, self.lat_r)
        dx, dy = np.diag(np.array(self.footprint.get_tile_offsets()))
        diag = np.sqrt(dx ** 2 + dy ** 2) * 0.5
        theta1 = np.arctan2(dx, dy)
        thetas = np.array([theta1, pi - theta1, pi + theta1, 2.0 * pi - theta1]) + np.radians(self.native_posang)
        pj = [p0.offset([diag, th]) for th in thetas]
        return pj

    def get_interleaved_tile(self, quadrant=0):
        """
        Returns a tile that is offset from the current tile by half the tile spacing in both cardinal directions.
        The sign of each offset is determined by the value of quadrant. This form of interleaving differs from the
        standard "beam interleaving" in which the interleaved position is offset from the original by a fraction of a
        beam spacing so as to place the new beam positions in the sensitivity minima of the original tile position.
        The offset returned by this procedure is intended to smooth sensitivity variations that are dependent on axial
        distance, independent of beam position.  For all-sky tilings, it is of limited use as the set of interleaved
        tiles do not as neatly tile the sky.
        :param quadrant:
        :return: A new Tile object offset froom the current tile.
        """
        v12 = np.array(self.footprint.tile_offsets)
        v = (v12[0] + v12[1]) * 0.5 * Tile.quadrant_select[quadrant]

        dpa = [np.sqrt(v[0] ** 2 + v[1] ** 2), np.arctan2(v[0], v[1])]
        dpa[1] += self.footprint.pa
        pos0 = self.footprint.refpos
        pos1 = pos0.offset(dpa)
        dra = ang_unwrap(pos1.ra - pos0.ra, pi)
        pa = self.footprint.pa + dra * np.sin(pos1.dec)
        rt = Tile(0, pos1.ra, pos1.dec, pa * 180.0 / pi)
        return rt

    def _set_posang_deg(self):
        """
        Return the required antenna position angle, which differs from the tile position angle by the position angle
        used at beam forming.
        :return: Antenna position angle (degrees).
        """
        val = ang_unwrap(self.posang - Tile.bf_pa, 180.0)
        return val

    def _make_name(self):
        """
        Construct a string name of form hhmm+/-dd

        :return: tile name
        """

        lon = np.degrees(self.native.ra)
        lat = np.degrees(self.native.dec)
        coord = Tile.coord
        if coord == 'J2000':
            rh = int(lon / 15.)
            rm = int(lon * 4. - rh * 60)
            ds = "{:+05.1f}".format(lat)
            ret = "{:02d}{:02d}{}".format(rh, rm, ds[:3])
        elif coord == 'GALAC':
            ll = int(lon)
            bb = "{:+05.1f}".format(lat)
            ret = "G{:03d}{}".format(ll, bb[:3])
        elif coord == 'MAGEL':
            ll = int(lon)
            bb = "{:+05.1f}".format(lat)
            ret = "M{:03d}{}".format(ll, bb[:3])
        else:
            rh = int(lon / 15.)
            rm = int(lon * 4. - rh * 60)
            ds = "{:+05.1f}".format(lat)
            ret = "{:02d}{:02d}{}".format(rh, rm, ds[:3])
        return ret

    def _get_corners(self):
        """
        Calculate and return the sky coodinates of the tile corners.
        :return: a list containing a Skypos object for each corner.
        """
        return self.get_poly()

    def _get_ra_mid_wid(self):
        """
        Needed to help with tiles that straddle 0 hours
        :return:
        """
        ra0, ra1 = self.corners_deg[0, 0], self.corners_deg[3, 0]
        ra_wid = ra0 - ra1
        ra_mid = (ra0 + ra1) / 2.
        if ra0 < ra1:
            ra_wid = 360. + ra_wid
            ra_mid += 180.
        return ra_mid, ra_wid


def ang_unwrap(x, semi):
    """
    Find the angle equivalent to x in the range [-semi, semi] where
    semi is the half-turn angle in the same units as x. Mostly, semi will be either 180 or pi.
    :param x: Given angle
    :param semi: Half-turn angle in same angular units as x
    :return: Angle equivalent to x in range [-semi, semi]
    """
    return (x + semi) % (2.0 * semi) - semi


def vec_skp(vec):
    """
    Return a Skypos object given the direction as a 3-vector
    :param vec: The given direction
    :return: Direction as Skypos object
    """
    r, d = xyz_rd(vec)
    return Skypos(r, d)


def xyz_rd(v):
    """
    Convert a 3-vector direction to (longitude, latitude) pair.
    :param v: Given direction as 3-vector
    :return: (longitude, latitude) pair (radians)
    """
    x, y, z = v
    b2 = math.asin(z)
    b1 = (2.0 * math.pi + math.atan2(y, x)) % (2.0 * math.pi)
    return b1, b2


def get_gc_pole(p1, p2):
    """
    Find the pole of the great circle that passes through p1, p2.
    :param p1: Skypos object
    :param p2: Skypos object
    :return: A Skypos object giving the direction of one of the poles of the great circle passing
    though the two input positions.
    """
    v1 = p1.get_vec()
    v2 = p2.get_vec()
    v3 = np.cross(v1, v2)
    x, y, z = v3 / (np.sqrt((v3 ** 2).sum()))
    b2 = np.arcsin(z)
    b1 = (twopi + np.arctan2(y, x)) % twopi
    return Skypos(b1, b2)

# TODO remove the following routine, and others, that exist in sphere_plotting.py
def get_gc_intersect(s1, s2):
    """
    Given two great circles, specified by their poles, find the two intersection points.
    :param s1: Pole of first great circle as Skypos object
    :param s2: Pole of second great circle as Skypos object
    :return: A list of the two Skypos objects representing the two intersection points.
    """
    cp1, sp1 = cos(pi / 2 - s1.dec), sin(pi / 2 - s1.dec)
    ca1, sa1 = cos(s1.ra), sin(s1.ra)
    cp2, sp2 = cos(pi / 2 - s2.dec), sin(pi / 2 - s2.dec)
    ca2, sa2 = cos(s2.ra), sin(s2.ra)

    v = -sp1 * ca1 * sa2 + sp1 * sa1 * ca2
    u = sp1 * ca1 * cp2 * ca2 + sp1 * sa1 * cp2 * sa2 - cp1 * sp2
    alpha = arctan2(v, u)
    t = alpha - pi / 2.
    st2, ct2 = sin(t), cos(t)
    M = np.array([[cp1 * ca1, cp1 * sa1, -sp1], [-sa1, ca1, 0.], [sp1 * ca1, sp1 * sa1, cp1]])
    Mt = np.array(np.matrix(M).T)
    xyz = np.array([cp2 * ca2 * ct2 - sa2 * st2, cp2 * sa2 * ct2 + ca2 * st2, -sp2 * ct2])
    x, y, z = np.dot(M, xyz)
    vec = np.dot(Mt, [x, y, z])
    rd = xyz_rd(vec)

    return Skypos(rd[0], rd[1]), Skypos(rd[0] + pi, -rd[1])

# TODO Consider introducing a new module "Spherical_geometry" to take routines such as the following, and
# others in speherical_plotting.
def refpos_to_euler(lon, lat):
    # Computes the Euler angles used by class Tile to generate rotation matrix
    # lon, lat in radians
    if lat < 0.0:
        eu = np.array([lon, pi / 2 + lat, 0.0])
    else:
        eu = np.array([lon + pi, pi / 2 - lat, 0.0])
    return eu


def get_nlon_tiles(tile_pitch, beam_pitch, lon_span, lat):
    dec_t = lat - np.sign(lat) * (tile_pitch[1] / 2 - beam_pitch / 2)
    p0 = Skypos(0.0, dec_t)
    p1 = p0.offset([tile_pitch[0] / 2, pi / 2.])
    alpha = 2 * (p1.ra - p0.ra)
    ntiles = lon_span // alpha + 1

    return ntiles, alpha


def get_lon_span(lat, cap_radius, tile_pitch):
    if cap_radius < 0.0:
        span = 2.0 * pi
    else:
        abs_ddstep = tile_pitch[1] / 2.
        ddstep = np.copysign(abs_ddstep, lat)
        phi = lat - ddstep
        # print dec, dec_lim, delta, phi
        y2 = np.sin(cap_radius) ** 2 - np.sin(phi) ** 2

        if y2 > 0.0:
            y = np.sqrt(y2)
            span = 2.0 * np.arcsin(y / np.cos(phi))
            # ra_range = np.array([-dr, dr])
        else:
            # ra_range = np.array([0.0])
            span = tile_pitch[0]
    return span


def get_tiling(tile_pitch, beam_pitch, lat_range, cap_radius, expansion='symmetric', mode="squeeze"):
    # tile_pitch - tile spacing in radians (e-w, n-s)
    # beam_pitch - beam pitch in radians
    # lat_range the angular extend in latitude to be tiled - the range is expanded to cope
    # cap_radius - the angular radius of a cap (could ultimately be polar cap); this determines latitude-dependent long
    #              range to be tiled
    # print 'get_tiling: ', tile_pitch, beam_pitch, lat_range, cap_radius
    # D = 180.0/pi
    eps = 1.0e-4
    w, h = tile_pitch
    p = beam_pitch
    lat_span = np.diff(lat_range)[0]
    nd_tiles = lat_span // h
    if lat_span - nd_tiles * h > 1.0e-3:
        nd_tiles += 1
    if expansion == 'symmetric':
        la1 = (lat_range[0] + lat_range[1]) / 2 - nd_tiles / 2. * h
        la2 = la1 + nd_tiles * h
    else:
        la1 = lat_range[0]
        la2 = la1 + nd_tiles * h
    arr = np.arange(la1, la2 + eps, h)
    idx = (np.abs(arr - 0.0)).argmin()

    # start at band centred on lat = la1 + idx * h
    lat = arr[idx] - h / 2
    lon = 0.0
    if lat - h / 2 > 0.0:
        lon_s = []
        lat_s = []
    else:
        lon_s = []
        lat_s = [lat]
        while lat >= la1 + h / 2:
            lon_span = get_lon_span(lat, cap_radius, tile_pitch)
            ntiles, alpha = get_nlon_tiles(tile_pitch, p, lon_span, lat)
            if mode == "squeeze":
                alp1 = lon_span / ntiles
            else:
                alp1 = alpha
            end = alp1 * (ntiles / 2.0 - 0.5)
            lon_seq = list(np.arange(-end, end + eps, alp1))
            lon_s.append(lon_seq)

            ps1 = Skypos(lon, lat - h / 2)
            po1 = Skypos(lon, lat - h / 2 + pi / 2)
            po2 = Skypos(lon + alp1, lat - h / 2 + pi / 2)

            q = get_gc_intersect(po1, po2)
            i = np.abs(np.array([q[0].dec, q[1].dec]) - ps1.dec).argmin()
            lat = q[i].dec - h / 2

            lat_s.append(lat)
        j = lat_s.pop(-1)

    # return to the northern band, assume the correction is small:
    no_south = (len(lat_s) == 0)
    do_north = True

    if no_south:
        lat = arr[idx] + h / 2
    else:
        lat = lat_s[0] + h
        do_north = lat_s[0] + h / 2 + eps < la2

    if not do_north:
        lat_n = []
        lon_n = []
    else:
        lon_n = []
        lat_n = [lat]
        while lat <= la2 - h / 2:
            lon_span = get_lon_span(lat, cap_radius, tile_pitch)
            ntiles, alpha = get_nlon_tiles(tile_pitch, p, lon_span, lat)
            if mode == "squeeze":
                alp1 = lon_span / ntiles
            else:
                alp1 = alpha
            end = alp1 * (ntiles / 2.0 - 0.5)
            lon_seq = list(np.arange(-end, end + eps, alp1))
            lon_n.append(lon_seq)

            ps1 = Skypos(lon, lat + h / 2)
            po1 = Skypos(lon, lat + h / 2 - pi / 2)
            po2 = Skypos(lon + alp1, lat + h / 2 - pi / 2)

            q = get_gc_intersect(po1, po2)
            i = np.abs(np.array([q[0].dec, q[1].dec]) - ps1.dec).argmin()
            lat = q[i].dec + h / 2

            lat_n.append(lat)
        j = lat_n.pop(-1)

    lon_sequences = lon_s + lon_n
    latseq = np.concatenate([lat_s, lat_n])
    arr1inds = latseq.argsort()
    sorted_lat = latseq[arr1inds[::]]
    sorted_lon = [lon_sequences[j] for j in arr1inds[::]]
    la1, la2 = sorted_lat[0], sorted_lat[-1]
    la1 -= h / 2
    la2 += h / 2
    new_range = np.array([la1, la2])

    return sorted_lat, sorted_lon, new_range


def tile_dec_band(tile_pitches, beam_pitch, lat_range):
    # Computes the positions of tiles that cover the sky within the given declination range.
    # Series of declinations are chosen, and for each a series of tiles is spaced in RA with spacing
    # to the spacing nominated in tile_pitches.  To reduce gaps arising from sky curvature, RA tile
    # sequences are computed using the declination of tile edge closest the equator, rather than the
    # declination of the tile centre.
    # tile_pitches in radians - [ra_tile_pitch, dec_tile_pitch]
    # beam_pitch in radians
    # dec_range - Range of declinations to tile: in radians [dec_south, dec_north]
    # returns tile positions as a dictionary tile_positions:
    #  tile_positions[k] = (dec, ra_sequence) where
    #       k is the declination of the row in format +/- dd:mm
    #       dec is declination in decimal degrees
    #       ra_sequence is an ndarray of RAs in radians
    tile_area = rectangle_area(tile_pitches)
    cap_rad = -1.0
    latseq, lon_seq, new_range = get_tiling(tile_pitches, beam_pitch, lat_range, cap_rad)

    tile_positions = []
    for dec, lons in zip(latseq, lon_seq):
        tile_positions.append((dec, lons))

    ntiles = len(tile_positions)

    d1, d2 = new_range
    area_band = 2.0 * pi * (np.sin(d2) - np.sin(d1))
    area_tiles = ntiles * tile_area

    return tile_positions, area_band, area_tiles, new_range


def tile_polar_cap(tile_pitches, beam_pitch, dec_lim):
    # generate tile positions over a polar cap
    # tile_pitches - the two dimensions of a tile
    # beam_pitch
    # dec_limit
    j_origin = Skypos(0.0, 0.0)
    scp = -pi / 2
    ncp = +pi / 2
    if dec_lim > 0.0:
        pol_cap = rotate_orig_to_pole(ncp)
        pol_cap_rad = pi / 2. - dec_lim
    else:
        pol_cap = rotate_orig_to_pole(scp)
        pol_cap_rad = pi / 2. + dec_lim

    # First we generate a region of tiles about the origin (long, lat) = (0., 0.) of a set of coordinates.
    # Once generated these are rotated into place over the pole.
    # Some of the variable names here relate to the preliminary coordinates: lat_range relates to this first step
    lat_range = [-pol_cap_rad, +pol_cap_rad]
    latseq, lon_seq, new_range = get_tiling(tile_pitches, beam_pitch, lat_range, pol_cap_rad, mode="expand")

    tile_positions = []
    for lat, lon in zip(latseq, lon_seq):
        tile_positions.append((lat, lon))

    # latseq, d_olap, new_range = tile_dec_segment(tile_pitches, lat_range, expansion="symmetric")
    w, h = tile_pitches
    pol_tile_positions = []
    area = 0.0

    for lat, lons in zip(latseq, lon_seq):
        dtheta = lons[-1] - lons[0] + w
        area += dtheta * (np.sin(lat + h / 2.) - np.sin(lat - h / 2.))
        for lon in lons:
            lon_a = (lon + 2.0 * pi) % (2.0 * pi)
            pe = Skypos(lon_a, lat)
            p = transform(pe, pol_cap)
            p_posang = p.d_pa(j_origin)[1] * 180.0 / pi
            pos = np.array([p.ra, p.dec, p_posang])
            pol_tile_positions.append(pos)

    ntiles = len(pol_tile_positions)
    tile_area = rectangle_area(tile_pitches)
    area_tiles = ntiles * tile_area
    # TODO compute cap area properly
    # Area of polar cap is just 2π * cosδ.
    area_cap = twopi * np.cos(dec_lim)

    return pol_tile_positions, area_cap, area_tiles


def tile_pol_to_pol(tile_pitches, beam_pitch, dec_range, do_north=False):
    # Generate tile positions for the whole sphere, given
    #  tile_pitches - tile spacing (horizontal, vertical) in radians
    #  beam_pitch - beam spacing in each tile, in radians
    #
    #  dec_range - southern and north boundaries of central zone with polar zones
    dec_tiles, band_area, area_tiles, new_dec_range = tile_dec_band(tile_pitches, beam_pitch, dec_range)
    spol = tile_polar_cap(tile_pitches, beam_pitch, new_dec_range[0])
    spol_tile_positions, spol_area, spol_area_tiles = spol
    declim = new_dec_range[1]
    if do_north:
        npol = tile_polar_cap(tile_pitches, beam_pitch, new_dec_range[1])
        npol_tile_positions, npol_area, npol_area_tiles = npol
        declim = +pi / 2
    else:
        npol_tile_positions, npol_area, npol_area_tiles = [], 0.0, 0.0

    all_tiles = []
    posang = 0.0
    for p in spol_tile_positions:
        all_tiles.append(p)

    for v in dec_tiles:
        dec, raseq = v
        for ra in raseq:
            p = [float(ra), float(dec), posang]
            all_tiles.append(p)

    for p in npol_tile_positions:
        all_tiles.append(p)

    idents = range(len(all_tiles))
    tile_area = rectangle_area(tile_pitches)
    total_area = 2.0 * pi * (np.sin(declim) + 1.0)
    ntiles = len(all_tiles)
    area_tiles = ntiles * tile_area
    tiles = np.array([Tile(i, p[0], p[1], p[2]) for i, p in zip(idents, all_tiles)])
    access = [~ti.check_accessible() for ti in tiles]
    tiles = np.ma.masked_array(tiles, mask=access)

    tiling = {'tiles': tiles.compressed(),
              'area_survey': total_area * ster_to_sqdeg,
              'area_tiles': area_tiles * ster_to_sqdeg,
              'lat_limits': new_dec_range}
    return tiling


# find centroid of vertices
# shift polygon to (0,0) at centroid
# find long/lat extent
# tile that rectangle
# shift back to original place
# mask
def rectangle_area(tile_pitches):
    area = 4.0 * np.arcsin(np.tan(tile_pitches[0] / 2.) * np.tan(tile_pitches[1] / 2.0))
    return area


def polygon_area(poly):
    """
    Returns the area of a spherical polygon in steradians
    :param (ndarray) Array of polygon vertices of type Skypos
    """
    n = len(poly)
    jj = np.arange(0, n)
    jjp = (jj + 1) % n
    jjm = (jj - 1 + n) % n
    pa1 = np.array([poly[j].d_pa(poly[jp])[1] for j, jp in zip(jj, jjp)])
    pa2 = np.array([poly[j].d_pa(poly[jm])[1] for j, jm in zip(jj, jjm)])
    ang = (pa2 - pa1 + twopi) % twopi
    area = ang.sum() - (n - 2) * pi
    if area > 2.0 * pi:
        area = 4.0 * pi - area
    return area


def find_centroid_mass(poly):
    vecs = np.array([v.get_vec() for v in poly])
    vc = vecs.mean(axis=0)
    lon = (np.arctan2(vc[1], vc[0]) + 2.0 * np.pi) % (2.0 * np.pi)
    lat = np.arctan2(vc[2], np.sqrt(vc[0] ** 2 + vc[1] ** 2))
    centroid = Skypos(lon, lat)
    return centroid


def find_centroid_kh(poly):
    # Find a position representative of the polygon, and its "position angle"
    # this is done in three stages:
    # 1. Convert the spherical polygon vertices into cartesian coordinates
    # 2. Find the convex hull of the points
    # 3. Find the ellipse that best fits the hull
    # range of distances in 3D to the polygon vertices.
    # Not a smart algorithm. Could use proper function minimisation.

    cent = find_centroid_mass(poly)
    #     print('centroid_pa ',cent)
    dpa = [cent.d_pa(v) for v in poly]
    points = np.zeros([len(dpa), 2])
    points[:, 0] = np.array([d[0] * np.sin(d[1]) for d in dpa])
    points[:, 1] = np.array([d[0] * np.cos(d[1]) for d in dpa])
    # points now 2d cartesian, from lon,lat input and "centre"
    et = EllipsoidTool()
    (center, radii, rotation) = et.get_min_vol_ellipse(points, .001)

    xc, yc = center
    d, pa = np.sqrt(xc ** 2 + yc ** 2), np.arctan2(xc, yc)
    ecent = cent.offset([d, pa])
    erot = np.arctan2(rotation[0, 1], rotation[0, 0])

    xe = np.array([radii[0] * np.cos(phi) for phi in np.linspace(0.0, twopi, 40)])
    ye = np.array([radii[1] * np.sin(phi) for phi in np.linspace(0.0, twopi, 40)])
    for i in range(len(xe)):
        xe[i], ye[i] = np.dot([xe[i], ye[i]], rotation) + center
    # [xe,ye] now locus of circiumscribed ellipse of 2d cartesian points

    # convert back to lon,lat points on sphere, using original "centre"
    ds = [np.sqrt(a ** 2 + b ** 2) for a, b in zip(xe, ye)]
    pas = [np.arctan2(a, b) for a, b in zip(xe, ye)]
    fitell = [cent.offset([d, pa]) for d, pa in zip(ds, pas)]

    return ecent, erot, fitell


def rotate_to_orig(poly, centroid, rot=0.0, forward=True):
    shifted = []
    psh = poly.shape
    if forward:
        for p in poly.flat:
            q = p.rotate_z(-centroid.ra)
            r = q.rotate_y(-centroid.dec)
            s = r.rotate_x(-rot)
            shifted.append(s)
    else:
        for p in poly.flat:
            s = p.rotate_x(rot)
            r = s.rotate_y(centroid.dec)
            q = r.rotate_z(centroid.ra)
            shifted.append(q)

    return np.array(shifted).reshape(psh)


def make_box(poly):
    verts = np.array([[p.ra, p.dec] for p in poly])
    lons = (verts[:, 0] + np.pi) % (2.0 * np.pi) - np.pi
    lats = verts[:, 1]
    box = [min(lons), max(lons), min(lats), max(lats)]
    lat_lims = get_lat_lims(box)
    box[2] = lat_lims[0]
    box[3] = lat_lims[1]
    return box


def get_lat_lims(box):
    ret = []
    for i in [2, 3]:
        p1 = Skypos(box[0], box[i])
        p2 = Skypos(box[1], box[i])
        gp = get_gc_pole(p1, p2)
        gpm = Skypos(((box[1] + box[0]) / 2.0 + pi / 2.0), 0.0)
        pint = get_gc_intersect(gp, gpm)
        if i == 2:
            ret.append(min(pint[0].dec, pint[1].dec))
        else:
            ret.append(max(pint[0].dec, pint[1].dec))

    return ret


def get_centres(pitch, extent):
    # Given a width (pitch) and extent, return the centres of segments of the
    # given width that span the extent.
    n = int((extent[1] - extent[0]) // pitch) + 1
    if n == 1:
        centres = [(extent[0] + extent[1]) / 2.0]
    else:
        centres = np.linspace(extent[0] + pitch / 2, extent[1] - pitch / 2, n, endpoint=True)
    return centres


def tile_polygon(tile_pitches, polygon, force_symmetry=False):
    """Computes sky positions and position angles for all positions in a
    quasi-rectangular grid and any interleaving points for each grid position.
    centre   Skypos (ra,dec) of grid centre
    angle    position angle of rectangle (radians)
    dela     "horizontal" grid spacing (radians)
    deld     "vertical" grid spacing (radians)
    nx,ny    number of points horizontally, vertically
    iofs     is a list of pairs, each pair an intereaving offset in polar (d,pa) (radians)
    long_shift Shifts the area along the "horizontal" great circle (radians)"""

    polygon = np.array(polygon)
    cent, rot, junk = find_centroid_kh(polygon)

    if force_symmetry:
        cent = Skypos(cent.ra, 0.0)
        rot = 0.0

    rpoly = rotate_to_orig(polygon, cent, rot=rot)
    box = make_box(rpoly)
    # If, after the transformation from planar to spherical the bounding ellipse has
    # changed its axial ratio to make it more extenmsive in the latitude direction,
    # add pi2 to its angle.
    if box[1] - box[0] < box[3] - box[2]:
        rot += pi / 2.0
        rpoly = rotate_to_orig(polygon, cent, rot=rot)
        box = make_box(rpoly)

    # Construct the grid given the centre, extent, and number of grid
    #  increments.

    # Mark out RA and Dec increments, centred on (0,0)  - on the equator of
    # a sphere.

    pole = np.array([Skypos("00:00:00", "+90:00:00")])
    if force_symmetry:
        extent = box
        lat = max(abs(box[2]), abs(box[3]))
        extent[2:] = -lat, lat
    else:
        extent = box

    # construct the grid of pointings, centred at (0.0,0.0)
    dela, deld = tile_pitches

    gra = get_centres(dela, extent[:2])
    gde = get_centres(deld, extent[2:])
    nx = len(gra)
    ny = len(gde)

    # compute sky positions for each grid point; rotate the grid, compute
    # offsets and apply to the requested survey centre position
    gs = np.array([[Skypos(r, d) for r in gra] for d in gde])
    ss = rotate_to_orig(gs, cent, rot=rot, forward=False)

    shifted_pole = rotate_to_orig(pole, cent, rot=rot, forward=False)[0]

    # and use for determining tile position angles in the final grid.
    ss_pa = [[si.d_pa(shifted_pole)[1] for si in sj] for sj in ss]
    rss = np.array([ss])
    rss_pa = np.degrees(np.array([ss_pa]))
    tilpos = [[r.ra, r.dec, pa] for r, pa in zip(rss.flat, rss_pa.flat)]
    min_lat = min([r.dec for r in rss.flat])
    max_lat = max([r.dec for r in rss.flat])
    idents = range(len(tilpos))
    tile_area = rectangle_area(tile_pitches)
    area_tiles = nx * ny * tile_area
    total_area = polygon_area(polygon)
    tiles = np.ma.array([Tile(i, p[0], p[1], p[2]) for i, p in zip(idents, tilpos)])
    access = [~ti.check_accessible() for ti in tiles]
    tiles = np.ma.masked_array(tiles, mask=access)
    tiling = {'tiles': tiles.compressed(),
              'area_survey': total_area * ster_to_sqdeg,
              'area_tiles': area_tiles * ster_to_sqdeg,
              'lat_limits': [min_lat, max_lat]}

    return tiling


def mask_tiles(tilpos, tile_pitches, polygons):
    """
    Take a set of tile positions and sizes and return a mask array of the same size with values set False for all tiles
    within any of the given polygons.  The test for position relative to the polygons is based on the method of Bevis
    and Chatelain, with added steps to allow for polygon sides traversing a tile but with neither the tile centre or its
    corners falling within the polygon.

    :param tilpos: ndarray of shape [num_tiles, 3] giving tile locations and position angles (radians)
    :param tile_pitches: length rectangular tile sides (radians)
    :param polygons: list of polygons, each an ndarray of vertices as Skypos objects.
    :return: ndarray of booleans shape [num_tiles]
    """
    pnt_x = Skypos(1.0, pi / 2. - 0.02)
    # start with all tiles excluded
    tmask = np.array([True] * len(tilpos))
    for poly in polygons:
        nv = len(poly)
        pol = SphericalPolygon(poly, pnt_x)
        if pol.nv > 2:
            for i, tp in enumerate(tilpos):
                #
                tc = tp.get_poly_native()
                #                 (Skypos(tp[0], tp[1]), tile_pitches, np.radians(tp[2]))
                #                 tc.append(Skypos(tp[0], tp[1]))
                for t in tc:
                    pla, plo = [t.dec, t.ra]
                    loc = pol.get_location(pla, plo)
                    if loc == 0:
                        tmask[i] = False
                # if the centre or no corner lie in the polygon, check whether any vertex of the polygon lies within
                # the tile or any side of the tile intersects the polygon.
                if tmask[i]:
                    tile_pol = SphericalPolygon(tc, pnt_x)
                    # look for vertices inside tile
                    for k in range(nv):
                        pla, plo = [poly[k].dec, poly[k].ra]
                        loc_v = tile_pol.get_location(pla, plo)
                        if loc_v == 0:
                            tmask[i] = False
                            break

                if tmask[i]:
                    # look for intersections of tile and polygon
                    for j in range(4):
                        p1, p2 = tc[j], tc[(j + 1) % 4]
                        s1 = get_gc_pole(p1, p2)
                        dp12 = p1.d_pa(p2)[0]
                        for k in range(nv):
                            q1, q2 = poly[k], poly[(k + 1) % nv]
                            s2 = get_gc_pole(q1, q2)
                            dq12 = q1.d_pa(q2)[0]
                            pint = get_gc_intersect(s1, s2)
                            nearest = np.argsort([pin.d_pa(p1)[0] for pin in pint])[0]
                            between_p = (dp12 > pint[nearest].d_pa(p1)[0]) and (dp12 > pint[nearest].d_pa(p2)[0])
                            between_q = (dq12 > pint[nearest].d_pa(q1)[0]) and (dq12 > pint[nearest].d_pa(q2)[0])
                            if between_p and between_q:
                                tmask[i] = False
                                break

                        if not tmask[i]:
                            break

    return tmask


"""
Bevis and Chatelain method
"""


class SphericalPolygon(object):
    """
    This class performs operations on polygons defined on the unit sphere. It includes an implementation of
    the Bevis and Chatelain method for determining whether a point on the unit
    sphere lies inside a polygon on that surface.  The concept of "inside" is solidified by defining
    the input point (xlon,xlat) to be "outside" the polygon.
    Find a reference to the method at
    https://www.researchgate.net/publication/227017249_Locating_a_point_on_a_spherical_surface_relative_to_a_spherical_polygon
    Other methods exist, some claiming to be much more computationally efficient. For the application here, polygons
    with relatively few vertices are envisaged (10s or 100s), so computation time is not a serious concern.
    Other potential sources for this function are astropy.regions (seems immature at this time (2021November) and
    pyregion, which claims to parse ds9 region files and do some region computation, but does not suit this application.

    This method has the advantage of resorting to the fundamental geometric mathematics and will not suffer from updates
    in any external package.
    """

    def __init__(self, polygon, external):
        """

        :param polygon: Set of polygon vertices, each a Skypos object
        :type polygon: ndarray
        :param external: A Skypos point known to be outside the polygon.
        :type external: Skypos
        """
        maxnv = 200
        nv = len(polygon)
        if nv > maxnv:
            print("Polygon has too many vertices")
        self.poly = polygon
        self.ext = external
        self.poly_vecs = np.array([p.get_vec() for p in self.poly])
        self.vlat = [v.dec for v in polygon]
        self.vlon = [v.ra for v in polygon]
        self.xlon = external.ra
        self.xlat = external.dec
        self.ibndry = 1
        self.nv = nv
        self.tlonv = [self.transform_lon(self.xlat, self.xlon, vla, vlo) for vla, vlo in zip(self.vlat, self.vlon)]
        # need to check for identical vertices here.
        # need to check for identical values of tlonv here.
        # Set number of vertices to zero if polygon malformed.
        for i in range(nv):
            ip = i - 1
            if self.vlat[i] == self.vlat[ip] and self.vlon[i] == self.vlon[ip]:
                print('Polygon malformed: vertices {:d} and {:d} are not distinct'.format(i, ip))
                self.nv = 0
            if self.tlonv[i] == self.tlonv[ip]:
                print('Polygon malformed: vertices {:d} and {:d} lie on same great circle as X'.format(i, ip))
                print('nv = ', nv)
                for j in range(nv):
                    print(self.poly[j], self.tlonv[j])
                exit()
                self.nv = 0

            if self.vlat[i] == -self.vlat[ip]:
                delo = self.vlon[i] - self.vlon[ip]
                if delo > pi:
                    delo -= twopi
                if delo < -pi:
                    delo -= twopi
                if abs(delo) == pi:
                    print("Polygon malformed: vertices {:d}, {:d} antipodal".format(i, ip))
                    self.nv = 0

    def get_location(self, plat, plon):
        if self.nv == 0:
            print("Error: polygon malformed")
            return None
        if plat == -self.xlat:
            delo = plon - self.xlon
            if delo > pi:
                delo -= twopi
            if delo < -pi:
                delo += twopi
            if abs(delo) == pi:
                print("P antipodal to X")
                location = 3
                return location
        location = 0
        icross = 0
        if plat == self.xlat and plon == self.xlon:
            location = 1
            return location

        for i in range(self.nv):
            tlonP = self.transform_lon(self.xlat, self.xlon, plat, plon)
            vAlat = self.vlat[i]
            vAlon = self.vlon[i]
            tlonA = self.tlonv[i]
            if i < self.nv - 1:
                vBlat = self.vlat[i + 1]
                vBlon = self.vlon[i + 1]
                tlonB = self.tlonv[i + 1]
            else:
                vBlat = self.vlat[0]
                vBlon = self.vlon[0]
                tlonB = self.tlonv[0]
            strike = 0
            if tlonP == tlonA:
                strike = 1

            else:
                rAB = self.east_or_west(tlonA, tlonB)
                rAP = self.east_or_west(tlonA, tlonP)
                rPB = self.east_or_west(tlonP, tlonB)

                if rAP == rAB and rPB == rAB:
                    # here P is between vertices vA, vB, so do some more checking
                    strike = 1
            if strike == 1:
                if plat == vAlat and plon == vAlon:
                    location = 2
                    return location
                tlonX = self.transform_lon(vAlat, vAlon, self.xlat, self.xlon)
                tlonB = self.transform_lon(vAlat, vAlon, vBlat, vBlon)
                tlonP = self.transform_lon(vAlat, vAlon, plat, plon)

                if tlonP == tlonB:
                    location = 2
                    return location
                else:
                    rBX = self.east_or_west(tlonB, tlonX)
                    rBP = self.east_or_west(tlonB, tlonP)
                    if rBX == -rBP:
                        icross += 1

        if icross % 2 == 0:
            location = 1
        return location

    @staticmethod
    def east_or_west(clon, dlon):
        # clon (degrees) starting longitude
        # dlon (degrees) finishing longitude
        # returns -1, 0, 1 for west, neither, east
        ret = 0
        delo = dlon - clon
        if delo > pi:
            delo -= twopi
        if delo < -pi:
            delo += twopi
        if abs(delo) == pi or delo == 0.0:
            ret = 0
        elif delo > 0.0:
            ret = -1
        elif delo < 0.0:
            ret = +1
        return ret

    @staticmethod
    def transform_lon(plat, plon, qlat, qlon):
        # Transforms P and Q so that P is on the NP. Returns longitude of transformed Q
        # degrees
        if plat == pi / 2.0:
            tranlon = qlon
        else:
            t = np.sin(qlon - plon) * np.cos(qlat)
            b = np.sin(qlat) * np.cos(plat) - np.cos(qlat) * np.sin(plat) * np.cos(qlon - plon)
            tranlon = np.arctan2(t, b)
        return tranlon


class EllipsoidTool:
    """Some stuff for playing with ellipsoids"""

    def __init__(self): pass

    def get_min_vol_ellipse(self, P=None, tolerance=0.01):
        """ Find the minimum volume ellipsoid which holds all the points

        Based on work by Nima Moshtagh
        http://www.mathworks.com/matlabcentral/fileexchange/9542
        and also by looking at:
        http://cctbx.sourceforge.net/current/python/scitbx.math.minimum_covering_ellipsoid.html
        Which is based on the first reference anyway!

        Here, P is a numpy array of N dimensional points like this:
        .. code-block::
        
          P = [[x,y,z,...], <-- one point per line
               [x,y,z,...],
               [x,y,z,...]]

        Returns:
        (center, radii, rotation)

        """
        (N, d) = np.shape(P)
        d = float(d)

        # Q will be our working array
        Q = np.vstack([np.copy(P.T), np.ones(N)])
        QT = Q.T

        # initializations
        err = 1.0 + tolerance
        u = (1.0 / N) * np.ones(N)

        # Khachiyan Algorithm
        while err > tolerance:
            V = np.dot(Q, np.dot(np.diag(u), QT))
            M = np.diag(np.dot(QT, np.dot(linalg.inv(V), Q)))  # M the diagonal vector of an NxN matrix
            j = np.argmax(M)
            maximum = M[j]
            step_size = (maximum - d - 1.0) / ((d + 1.0) * (maximum - 1.0))
            new_u = (1.0 - step_size) * u
            new_u[j] += step_size
            err = np.linalg.norm(new_u - u)
            u = new_u

        # center of the ellipse
        center = np.dot(P.T, u)

        # the A matrix for the ellipse
        A = linalg.inv(
            np.dot(P.T, np.dot(np.diag(u), P)) -
            np.array([[a * b for b in center] for a in center])
        ) / d

        # Get the values we'd like to return
        U, s, rotation = linalg.svd(A)
        radii = 1.0 / np.sqrt(s)

        return center, radii, rotation

    @staticmethod
    def get_ellipsoid_volume(radii):
        """Calculate the volume of the blob"""
        return 4. / 3. * np.pi * radii[0] * radii[1] * radii[2]


def get_polygons(poly_file):
    # Take various in puts:
    # 1. file with polygon per line : r1 d1, r2 d2, ..., rn dn
    #     with r,d in either decimal degrees or hms dms format.
    # 2. ds9 file with polygon per line: polygon r1 d1, r2 d2, ..., rn dn
    # 3. aladin drawing output

    # returns polygon vertices in degrees
    lines = open(poly_file, 'r', errors='replace').readlines()
    lines = [li.strip() for li in lines]
    lines = [li for li in lines if li]
    ds9, ala, unf = [False, False, False]
    ds9 = any([li.startswith('polygon') for li in lines])
    if not ds9:
        ala = any([li.startswith('line') for li in lines])
        if not ala:
            unf = True
    if ala:
        # Skip header and first vertex that is repeated
        data = [li.split() for li in lines[1:-1]]
        rad = np.array([float(a[2]) for a in data])
        decd = np.array([float(a[3]) for a in data])
        ra = np.radians((rad + 360.0) % 360.0)
        dec = np.radians(decd)
        poly = np.array([Skypos(r, d) for r, d in zip(ra, dec)])
        polygons = [poly]
    else:

        polygons = []
        for pd in lines:
            if ds9:
                pd = pd.replace('polygon', '')
            pq = []
            if ':' in pd:
                for pair in pd.split(','):
                    p, q = pair.split()
                    pq.append(Skypos(p, q))
            else:
                for pair in pd.split(','):
                    pp = pair.split()
                    if len(pp) == 2:
                        rd, dd = pp
                        ra = np.radians(float(rd) + 360.0) % 360.0
                        dec = np.radians(float(dd))
                        pq.append(Skypos(ra, dec))
            polygons.append(pq)

    return polygons


def rotate_orig_to_pole(pole):
    # Construct a matrix
    # pole is +/- pi/2
    sp = sin(pole)

    mat = np.array([[0, 0., -sp], [0., 1.0, 0.0], [sp, 0.0, 0.0]])
    # mat = np.dot(rx, np.dot(ry, rz))
    return mat


def rotmat(angs):
    # compute rotation matrix to convert vectors in S1 to S2 (two spherical coordinate systems)
    # angs are a0, d0, l0 in radians
    # a0,d0 is pole of S2 in coords of S1
    # l0 is longitude of S1 pole in S2
    a0, d0, l0 = angs
    a = np.array([-(l0 + pi / 2), d0 - pi / 2., a0 - pi / 2.])
    r1 = rotate_z(a[0])
    r2 = rotate_x(a[1])
    r3 = rotate_z(a[2])
    return np.dot(np.dot(r3, r2), r1)


def rotate_x(a):
    return np.array([[1., 0., 0.], [0., np.cos(a), -np.sin(a)], [0., np.sin(a), np.cos(a)]])


def rotate_z(a):
    return np.array([[np.cos(a), -np.sin(a), 0.], [np.sin(a), np.cos(a), 0.], [0., 0., 1.]])


def transform(p, mat):
    v = np.dot(mat, p.get_vec())
    return vec_skp(v)
