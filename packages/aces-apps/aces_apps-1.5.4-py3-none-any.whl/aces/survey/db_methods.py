#!/usr/bin/env python
from astropy.coordinates import SkyCoord, Longitude, Latitude
from astropy import units as u
from astropy.time import Time


def deg_to_hms(a):
    # Expect
    c = Longitude(a / 15., unit=u.hour)
    return c.to_string()


def deg_to_dms(a):
    # Expect
    c = Latitude(a, unit=u.deg)
    return c.to_string()


def str_to_mjdsec(a):
    time_val = Time(a.replace('T', ' '))
    time_val.format = 'mjd'
    return time_val.value * 3600.0 * 24.0


def deg_to_asec(a):
    return a * 3600.0


def to_gall(*args):
    sc = SkyCoord(args[0], args[1], frame='icrs', unit="deg")
    return sc.galactic.l.degree


def to_galb(*args):
    sc = SkyCoord(args[0], args[1], frame='icrs', unit="deg")
    return sc.galactic.b.degree


def list0(arg):
    # Expect something like '[item1, item2, item3]'
    content = arg.replace('[', '').replace(']', '').split(',')
    return content[0]


def list1(arg):
    # Expect something like '[item1, item2, item3]'
    content = arg.replace('[', '').replace(']', '').split(',')
    return content[1]
