#!/usr/bin/env python
from __future__ import print_function
import numpy as np
import ephem
import math
import sys
from collections import OrderedDict

def build_fixed_body(ra, dec):
    new_body = ephem.FixedBody()
    new_body._ra = ra
    new_body._dec = dec
    return new_body

def conv_angle(hms):
    parts = hms.split(':')
    if len(parts) != 3:
        raise RuntimeError("unsupported coordinate string {}".format(hms))
    if parts[0].find('-') != -1:
        return float(parts[0]) - float(parts[1]) / 60. - float(parts[2]) / 3600.
    else:
        return float(parts[0]) + float(parts[1]) / 60. + float(parts[2]) / 3600.


def parallactic_angle(lat, HA, dec):
    taneta = np.sin(HA) / (np.cos(dec) * np.tan(lat) - np.sin(dec) * np.cos(HA))
    return math.degrees(np.arctan(taneta))


def print_info(src, site):
    src.compute(site)

    print ("RA  = {}".format(src.a_ra))
    print ("DEC = {}".format(src.a_dec))

    print ("RA  = {:f} degrees".format(conv_angle(str(src.a_ra)) * 15))
    print ("DEC = {:f} degrees".format(conv_angle(str(src.a_dec))))

    print ("El  = {:.1f} degrees".format(math.degrees(float(src.alt)), ))
    print ("Az  = {:.1f} degrees".format(math.degrees(float(src.az)), ))

    ls = site.sidereal_time()
    ha = ls - src.ra

    print ("HA  = {:.1f} degrees".format(math.degrees(float(ha))))

    print ("PA  = {:.1f} degrees".format(parallactic_angle(float(site.lat), float(ha), float(src.a_dec))))

    rt = site.next_rising(src, start=site.date)

    print ("Next Rise = {} UT".format(rt))

    # Be careful! Asking for a transit seems to alter the observer time
    original_date = site.date
    mt = site.next_transit(src,start=original_date)
    print ("Next Transit = {} UT".format(mt))
    site.date = original_date

    st = site.next_setting(src, start=site.date)

    print ("Next Set = {} UT\n".format(st))


mro = ephem.Observer()
mro.lon = ephem.degrees('116.6314')
mro.lat = ephem.degrees('-26.697')
mro.elevation = 360.0
# mro.date = ephem.now()
# mro.date = ephem.Date("2014/06/17 04:16:00.00")
mro.horizon = ephem.degrees('15.3')
mro.pressure = 0


targets = OrderedDict()

targets['PKS0407-658'] = build_fixed_body('04:08:20.4', '-65:45:9,14.4')
targets['Taurus A'] = build_fixed_body('05:34:31.971', '22:00:52.06')
targets['Vela Pulsar'] = build_fixed_body('08:35:20.6', '-45:10:34.9')
targets['3C273'] = build_fixed_body('12:29:06.6997', '2:03:08.598')
targets['M87 (Virgo A)'] = build_fixed_body('12:30:49.43', '12:23:28.1')
targets['Centaurus A'] = build_fixed_body('13:25:31.0', '-42:59:36.0')
targets['Galactic Centre'] = build_fixed_body('17:45:40.04', '-29:00:28.07')
targets['B1934-638'] = build_fixed_body('19:39:25.02', '-63:42:45.63')
# noinspection PyUnresolvedReferences
targets['Sun'] = ephem.Sun()

if len(sys.argv) == 3:
    targets['~ Command Line Target ~'] = build_fixed_body(sys.argv[1], sys.argv[2])

print ("Current Time = {} UT, {} LMST\n".format(mro.date, mro.sidereal_time()))

for body in targets:
    print ("---- {} ----".format(body))
    print_info(targets[body], mro)

print("Current Time = {} UT, {} LMST\n".format(mro.date, mro.sidereal_time()))
