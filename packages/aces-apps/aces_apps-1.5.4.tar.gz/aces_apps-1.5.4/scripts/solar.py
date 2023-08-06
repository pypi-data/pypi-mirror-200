#!/usr/bin/env python
"""
This gives graphical views of the Sun's position relative to that of the given source.
"""
import numpy as np
import matplotlib.pylab as plt
from matplotlib.patches import Polygon

from askap.footprint import Skypos
from askap.coordinates import parse_direction

import argparse as ap
import sys
import datetime

# get_ipython().magic(u'matplotlib inline')


import ephem

HELP_START = """This presents a plot of source availability and susceptibility to solar interference
as a function of day-of-year and time of day.

V 30Nov2018
"""
catalogue = {
    "NGC253": "00:47:33.0  ,-25:17:18.0",
    "B0407-658": "04:08:20.380,-65:45:09.1",
    "3C138": "05:21:09.887,+16:38:22.1",
    "B0637-752": "06:35:46.508,-75:16:16.8",
    "VirgoA": "12:30:49.4  ,+12:23:28.0",
    "3C286": "13:31:08.287,+30:30:32.0",
    "apus": "15:56:58.8  ,-79:14:03.6",
    "1830-211": "18:33:39.92 ,-21:03:39.9",
    "B1934-638": "19:39:25.026,-63:42:45.6",
    "TaurusA": "05:34:31.94, +22:00:52.2"}

DEFAULT_SUN_LIMITS = [0.0, 4.0, 40.0, 90.0, 130.0]

explanation = "\n" + HELP_START + "\n\nRecognised sources\n"
for k in catalogue.keys():
    explanation += "{}\n".format(k)

announce = "\nsolar.py\n"


def arg_init():
    """Define the interprestation of command line arguments.
    """
    parser = ap.ArgumentParser(prog='solar',
                               formatter_class=ap.RawDescriptionHelpFormatter,
                               description=HELP_START,
                               epilog='See -x for more explanation and recognsed source list.')
    parser.add_argument('source', nargs="?", help="Source name")
    parser.add_argument('-p', '--position', metavar="'RA,Dec'", default=[0.0, 0.0], action=Celpos)
    parser.add_argument('-a', '--angle_limit', type=float, default=20.0, help="Solar angle limit [%(default).1f] (degrees) ")
    # parser.add_argument('-i', '--interactive', action='store_true')
    parser.add_argument('-l', '--label', action='store_true', help="Label solar boundaries")
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-x', '--explain', action='store_true', help="Give an expanded explanation")
    return parser


class Celpos(ap.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed")
        super(Celpos, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):

        # print 'ACTION : %r %r %r' % (namespace, values, option_string)
        if values in catalogue.keys():
            a, b = parse_direction(catalogue[values])
            rp = [np.radians(a), np.radians(b)]
        else:
            a, b = parse_direction(values)
            rp = [np.radians(a), np.radians(b)]
        setattr(namespace, self.dest, rp)


class intList(ap.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        # print 'ACTION : %r %r %r' % (namespace, values, option_string)
        safe_dict = {'range': range}
        rp = eval(values, safe_dict)
        if isinstance(rp, int):
            rp = [rp]
        setattr(namespace, self.dest, rp)


"""
Generic functons for the MRO
"""


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


class Source_Obs(object):
    def __init__(self, src_name, src_pos):
        self.sun = ephem.Sun()
        self.src_name = src_name
        self.srcpos = Skypos(src_pos[0], src_pos[1])
        self.src = build_fixed_body(src_pos[0], src_pos[1])

        self.mro = observer()
        self.mro_s = observer(horizon='0.0')

        self.date = "2018/01/01 12:00:00"
        self.mro.date = "2018/01/01 12:00:00"
        self.mro_s.date = "2018/01/01 12:00:00"
        self.sunpos = 0.
        self.d, self.pa = 0.0, 0.0
        self.sun_rise = 0.0
        self.sun_set = 0.0
        self.src_rise = 0.0
        self.src_set = 0.0
        self.sun_alt = 0.0
        self.src_alt = 0.0
        self.circumpolar = False
        self.src.compute(self.mro)

    def set_date(self, date):
        edate = ephem.Date(date)
        self.date = edate
        self.mro.date = edate
        self.mro_s.date = edate
        self.sun.compute(edate)
        self.sunpos = Skypos(self.sun.ra, self.sun.dec)
        self.d, self.pa = self.sunpos.d_pa(self.srcpos)
        self.sun_rise = self.mro_s.next_rising(self.sun, start=self.date)
        self.sun_set = self.mro_s.next_setting(self.sun, start=self.date)
        try:
            self.src_rise = self.mro.next_rising(self.src, start=self.date)
            self.src_set = self.mro.next_setting(self.src, start=self.date)
        except (ephem.AlwaysUpError):
            self.circumpolar = True
            self.src_rise = None
            self.src_set = None

        self.sun_alt = self.sun.alt
        self.src_alt = self.src.alt


def unlink_wrap(dat, lims=None, thresh=0.95):
    """
    Iterate over contiguous regions of `dat` (i.e. where it does not
    jump from near one limit to the other).

    This function returns an iterator object that yields slice
    objects, which index the contiguous portions of `dat`.

    This function implicitly assumes that all points in `dat` fall
    within `lims`.

    """
    if lims is None:
        lims = [-np.pi, np.pi]
    jump = np.nonzero(np.abs(np.diff(dat)) > ((lims[1] - lims[0]) * thresh))[0]
    lasti = 0
    for ind in jump:
        yield slice(lasti, ind + 1)
        lasti = ind + 1
    yield slice(lasti, len(dat))


def get_rise_set(s_obs):
    so = s_obs

    # Start at the beginning of a year
    date = "2018/01/01 12:00:00"
    jan1 = ephem.Date(date)

    # define the states
    states = [(False, False), (False, True), (True, False), (True, True)]

    xdate = jan1
    so.set_date(xdate)

    # determine the initial state
    sun_up = so.sun_alt > 0.0
    src_up = so.src_alt > so.mro.horizon.real
    state = states.index((src_up, sun_up))

    # determine whether we have a circum-polar source
    circum_polar = s_obs.circumpolar

    # initialise the lists
    both_up = []
    sun_rise_time = []
    sun_set_time = []
    src_rise_time = []
    src_set_time = []
    doys = []
    sun_angle = []
    # define the returned dictionary of results
    ret = {"sunr": sun_rise_time, "suns": sun_set_time,
           "srcr": src_rise_time, "srcs": src_set_time,
           "both": both_up, "s_ang": sun_angle, "doy": doys}

    yesterday = -1
    both_up_i = np.array((0.0, 0.0))
    while xdate < jan1 + 365.:
        so.set_date(xdate)
        hu = so.sun_rise
        su = so.src_rise
        hd = so.sun_set
        sd = so.src_set
        if circum_polar:
            sd = hd + 1.0

        start = xdate + 1.0
        if not circum_polar:
            if state == 0:
                if hu < su:
                    state = 1
                    xdate = hu
                elif hu > su:
                    state = 2
                    xdate = su
                else:
                    state = 3
                    xdate = su
                    start = xdate
            #             both_up_i = np.array((0.0, 0.0))

            if state == 1:
                if hd < su:
                    state = 0
                    xdate = hd
                elif hd > su:
                    state = 3
                    xdate = su
                    start = xdate
                else:
                    state = 2
                    xdate = su
        #             both_up_i = np.array((0.0, 0.0))

        if state == 2:
            if hu < sd:
                state = 3
                xdate = hu
                start = xdate
            elif hu > sd:
                state = 0
                xdate = sd
            else:
                state = 1
                xdate = sd
        #             both_up_i = np.array((0.0, 0.0))

        if state == 3:
            if hd < sd:
                state = 2
                xdate = hd
            elif hd > sd:
                state = 1
                xdate = sd
            else:
                state = 0
                xdate = hd
            #             both_up.append(np.array((start, xdate)))
            #             sun_angle.append(so.d * 180.0/np.pi)

            both_up_i = np.array((start, xdate))
        sun_angle_i = so.d * 180.0 / np.pi

        if xdate - yesterday > 1.0:
            yesterday = xdate
            doys.append(xdate - jan1)
            sun_rise_time.append((hu * 24.0 - 4.0) % 24.0)
            sun_set_time.append((hd * 24.0 - 4.0) % 24.0)
            if circum_polar:
                src_rise_time.append(None)
                src_set_time.append(None)
            else:
                src_rise_time.append((su * 24.0 - 4.0) % 24.0)
                src_set_time.append((sd * 24.0 - 4.0) % 24.0)

            both_up.append(both_up_i)
            both_up_i = [0.0, 0.0]
            sun_angle.append(sun_angle_i)

    return ret


def get_polygons(data, **kwargs_poly):
    doy = data['doy']
    src_rise = data['srcr']
    src_set = data['srcs']

    rising = [x for x in unlink_wrap(src_rise, lims=[0.0, 24.0])]
    rise = [[src_rise[sl][0], doy[sl][0]] for sl in rising]
    rise += [[src_rise[sl][-1], doy[sl][-1]] for sl in rising]
    rise.sort(key=lambda r: r[1])
    setting = [x for x in unlink_wrap(src_set, lims=[0.0, 24.0])]
    sset = [[src_set[sl][0], doy[sl][0]] for sl in setting]
    sset += [[src_set[sl][-1], doy[sl][-1]] for sl in setting]
    sset.sort(key=lambda r: r[1])
    select = 0
    if rise[0][0] < sset[0][0]:
        lines = [rise, sset]
    else:
        lines = [sset, rise]
        select = 1

    polygons = []
    corners = [[0.0, 0.0], lines[0][0], lines[0][1]]
    polygons.append(Polygon(corners, closed=True, **kwargs_poly))

    corners = [lines[0][0], lines[1][0], lines[1][1], lines[0][1]]
    polygons.append(Polygon(corners, closed=True, **kwargs_poly))

    corners = [lines[1][0], [24.0, 0.0], lines[0][2], lines[0][3], [0.0, 365.0], lines[1][1]]
    polygons.append(Polygon(corners, closed=True, **kwargs_poly))

    corners = [lines[0][2], lines[1][2], lines[1][3], lines[0][3]]
    polygons.append(Polygon(corners, closed=True, **kwargs_poly))

    corners = [lines[1][2], [24.0, 365.0], lines[1][3]]
    polygons.append(Polygon(corners, closed=True, **kwargs_poly))
    return polygons[select::2]


def get_polygons_angrange_vis(data, angrng, **kwargs_poly):
    # Find the polygons that descibe the date/times of source visibility, and sun within
    # the given range of angles from the source AND above the physical horizon.
    doy = data['doy']
    src_rise = data['srcr']
    sun_rise = data['sunr']
    both_up = data["both"]
    sun_angle = data["s_ang"]

    polys = []
    cnrs_s, cnrs_e = [], []
    for d, bu, sa, sr, hr in zip(doy, both_up, sun_angle, src_rise, sun_rise):
        b, e = bu
        if angrng[0] < sa < angrng[1] and (b < e):
            b = (b % 1.0) * 24 - 4.0
            e = (e % 1.0) * 24 - 4.0
            if len(cnrs_s) > 1:
                if b - cnrs_s[-1][0] > 1.0:
                    # Need to start a new polygon here - todo
                    cnrs_s.sort(key=lambda x: x[1], reverse=True)
                    cnrs = cnrs_e + cnrs_s
                    polys.append(Polygon(cnrs, closed=True, **kwargs_poly))
                    cnrs_s = []
                    cnrs_e = []
            cnrs_s.append([b, d])
            cnrs_e.append([e, d])
        elif len(cnrs_s) > 0:
            # Now sort around the patch
            cnrs_s.sort(key=lambda x: x[1], reverse=True)
            cnrs = cnrs_e + cnrs_s
            polys.append(Polygon(cnrs, closed=True, **kwargs_poly))
            cnrs_s, cnrs_e = [], []

    if len(cnrs_s) > 0:
        cnrs_s.sort(key=lambda x: x[1], reverse=True)
        cnrs = cnrs_e + cnrs_s
        polys.append(Polygon(cnrs, closed=True, **kwargs_poly))
    return polys


def get_polygons_angrange(data, angrng, **kwargs_poly):
    # Find the polygons that descibe the date/times of source to sun angle being in
    # the given range of angles from the source AND above the physical horizon.
    # This differs from get_polygons_angrange_vis in that the source need not
    # be visible everywhere inside the polygon.
    doy = data['doy']
    sun_rise = data['sunr']
    sun_set = data['suns']
    both_up = data["both"]
    sun_angle = data["s_ang"]

    polys = []
    cnrs_s, cnrs_e = [], []
    for d, bu, sa, sr, ss in zip(doy, both_up, sun_angle, sun_rise, sun_set):
        b, e = sr, ss
        if angrng[0] < sa < angrng[1]:
            if len(cnrs_s) > 1:
                if b - cnrs_s[-1][0] > 1.0:
                    cnrs_s.sort(key=lambda x: x[1], reverse=True)
                    cnrs = cnrs_e + cnrs_s
                    polys.append(Polygon(cnrs, closed=True, **kwargs_poly))
                    cnrs_s = []
                    cnrs_e = []
            cnrs_s.append([b, d])
            cnrs_e.append([e, d])
        elif len(cnrs_s) > 0:
            # Now sort around the patch
            cnrs_s.sort(key=lambda x: x[1], reverse=True)
            cnrs = cnrs_e + cnrs_s
            polys.append(Polygon(cnrs, closed=True, **kwargs_poly))
            cnrs_s, cnrs_e = [], []

    if len(cnrs_s) > 0:
        cnrs_s.sort(key=lambda x: x[1], reverse=True)
        cnrs = cnrs_e + cnrs_s
        polys.append(Polygon(cnrs, closed=True, **kwargs_poly))
    return polys


def plot_vis_solar(s_obs, data, sun_limits=None, show_solar_labels=False):
    if sun_limits is None:
        sun_limits = DEFAULT_SUN_LIMITS
    sun_lims = sun_limits
    kw_axial = {'color': 'k'}
    kw_close = {'color': 'yellow'}
    kw_paf = {'color': 'r'}
    doys = data['doy']
    sun_angle = data['s_ang']
    sun_rise = data['sunr']
    sun_set = data['suns']
    src_rise = data['srcr']
    src_set = data['srcs']

    f, (ax1, ax2) = plt.subplots(1, 2, sharey='row', figsize=(8, 5))
    f.subplots_adjust(wspace=0.0)
    ax1_ut = ax1.twiny()
    ax1.set_xlim(0.0, 24.0)
    ax1_ut.set_xlim(0.0, 24.0)
    ax1.set_ylim(365.0, 0.0)

    kw = {'color': '0.9'}
    kw_lines = {'color': 'k', 'lw': 0.5}

    polys = get_polygons_angrange(data, sun_lims[3:], **kw_paf)
    for po in polys:
        ax1.add_patch(po)
        if show_solar_labels:
            ymin = po.xy[:, 1].min()
            ymax = po.xy[:, 1].max()
            start_of_year = datetime.datetime(datetime.datetime.now().year, 1, 1)
            ymin_datetime = start_of_year + datetime.timedelta(days=ymin)
            ymax_datetime = start_of_year + datetime.timedelta(days=ymax)

            ax1.axhline(ymin, linestyle='dashed', linewidth=1, **kw_paf)
            ax1.axhline(ymax, linestyle='dashed', linewidth=1, **kw_paf)
            ax2.axhline(ymin, linestyle='dashed', linewidth=1, **kw_paf)
            ax2.axhline(ymax, linestyle='dashed', linewidth=1, **kw_paf)
            ax2.text(185, ymin, ymin_datetime.strftime("%d %b"), verticalalignment="center")
            ax2.text(185, ymax, ymax_datetime.strftime("%d %b"), verticalalignment="center")

    polys = get_polygons_angrange(data, sun_lims[1:3], **kw_close)
    for po in polys:
        ax1.add_patch(po)

    polys = get_polygons_angrange(data, sun_lims[:2], **kw_axial)
    for po in polys:
        ax1.add_patch(po)

    # Unless the source is circum-polar, draw the availability

    if not s_obs.circumpolar:
        polys = get_polygons(data, **kw)
        for po in polys:
            ax1.add_patch(po)
        for slc in unlink_wrap(src_rise, lims=[0.0, 24.0]):
            ax1.plot(src_rise[slc], doys[slc],  **kw_lines)
        for slc in unlink_wrap(src_set, lims=[0.0, 24.0]):
            ax1.plot(src_set[slc], doys[slc],  **kw_lines)

    ax1.plot(sun_rise, doys, '0.7')
    ax1.plot(sun_set, doys, '0.7')

    mon1 = np.array([0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334])
    mon = ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D']
    mon15 = mon1 + 15
    for my, m in zip(mon15, mon):
        ax1.text(-1.5, my, m, va='center')
    ax1.set_xticks([0., 6., 12., 18.])
    ax1_ut.set_xticks([0., 6., 12., 18.])
    ax1_ut.set_xticklabels((np.array([0., 6., 12., 18.], dtype=int) - 8) % 24)
    ax1.set_yticks(mon1)
    ax1.set_yticklabels([])
    ax1.grid()
    ax1.set_xlabel('AWST (h)')
    ax1_ut.set_xlabel('UTC (h)')

    cnrs = [[sun_lims[0], 0.0], [sun_lims[1], 0.0], [sun_lims[1], 365.0], [sun_lims[0], 365.0]]
    poly = Polygon(cnrs, closed=True, **kw_axial)
    ax2.add_patch(poly)
    cnrs = [[sun_lims[1], 0.0], [sun_lims[2], 0.0], [sun_lims[2], 365.0], [sun_lims[1], 365.0]]
    poly = Polygon(cnrs, closed=True, **kw_close)
    ax2.add_patch(poly)
    cnrs = [[sun_lims[3], 0.0], [sun_lims[4], 0.0], [sun_lims[4], 365.0], [sun_lims[3], 365.0]]
    poly = Polygon(cnrs, closed=True, **kw_paf)
    ax2.add_patch(poly)
    ax2.plot(sun_angle, doys, **kw_lines)
    ax2.vlines([90., 130.], 0.0, 365.0, **kw_lines)
    ax2.set_xlim(0.0, 180.)
    ax2.grid()
    ax2.set_xlabel('Sun angle (degrees)')
    if s_obs.src_name is not None:
        f.suptitle('{} ({})'.format(s_obs.src_name, s_obs.srcpos), y=1)
    else:
        f.suptitle(s_obs.srcpos, y=1)

    return f


def main():
    # parse command line options
    print(announce)

    parser = arg_init()
    args = parser.parse_args()
    if args.explain:
        print(explanation)
        sys.exit(0)

    if args.verbose:
        print("ARGS = ", args)

    src_name = args.source
    if src_name in catalogue.keys():
        a, b = parse_direction(catalogue[src_name])
        rp = [np.radians(a), np.radians(b)]
        src_pos = rp
    else:
        if src_name is None:
            print("No source name entered")
        else:
            print("Source '{}' not recognised by this (see -x option for recognised source names).".format(src_name))
        src_pos = args.position
        print('Using {}'.format(src_pos))

    sun_limits = [a for a in DEFAULT_SUN_LIMITS]
    sun_limits[2] = args.angle_limit
    src_obs = Source_Obs(src_name, src_pos)
    print(src_obs.src_name, src_obs.srcpos)
    aspect_data = get_rise_set(src_obs)
    f = plot_vis_solar(src_obs, aspect_data, sun_limits, show_solar_labels=args.label)
    pfile = 'solar_{}.png'.format(src_obs.src_name)
    f.savefig(pfile, dpi=300)
    print("Written plot to {}".format(pfile))


if __name__ == "__main__":
    sys.exit(main())
