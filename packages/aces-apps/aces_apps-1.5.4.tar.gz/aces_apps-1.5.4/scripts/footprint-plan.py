#!/usr/bin/env python
from __future__ import print_function
import sys
import argparse as ap
import numpy as np
from math import pi
import ephem
from askap.footprint import Skypos
import time
import askap.footprint as fpm
from askap.parset import ParameterSet
from askap.footprint import logger
from askap.coordinates import parse_direction
from askap.footprint.footprint import dp_to_lm
from aces.obsplan import aladin
from aces.obsplan.config import ACESConfig
import matplotlib as mpl
mpl.use('Agg')  # this script is non-interactive and Qt5Agg not supported easily on galaxy
import matplotlib.pylab as plt  # noqa

explanation = """
Footprint.py

BETA forms up to nine beams.  Their arrangement on the sky, called the "footprint",
is arbitrary provided all lie with a six-degree circle.  This program allows the
defintion of footprints from standard patterns or from customised lists of each
beam position.

Beams are defined on the sky relative to the "boresight" - the direction of the
optical axis of the antenna.  The beam offset must be expressed in a way that is
independent of the actual boresight direction. Two methods are used:

  1. Polar: distance, position angle (D,PA) where the distance is the great-circle
     distance between the boresight and the offset beam, and the position angle is
     measured as usual from celestial north, counterclockwise looking at the sky,
     that is "through east".
  2. Rectangular: (l,m) are the offset coordintes after an orthographic projection
     referenced to the Boresight.

For each beam Footprint gives two kinds of output:
  1. A pointing direction for the boresight direction (command to the antenna) to
     place the specified reference direction in the beam.
  2. A position on the sky, given a reference position, that marks the beam's peak
     response.

These two differ by 180 degrees of position angle.  The natural way to refer to the
beam's offset is the second of these.  When calculating pointing required for forming
or calibrating a beam, the offset must be shifted by 180 deg in PA (or by negating (l,m)).

2015-03-11 Josh Marvil has pointed out that simply shifting the offset by 180 degrees
to place the offset beam on the desired point (cal source, or beam-forming source) is
not correct. This is because the footprint will rotate so as to keep its n-s axis aligned
north; that is the boresight beam keeps PA = 0. To correct this, we need to apply a small
feed rotation at the offset positions so that the offset beam maintains its position angle.

"""

"""
Set factor for spacing relative to lambda/D (at band centre)
Require that the response internal to the footprint does not fall below 50% at the top of the band.
For band 1, FWHM is 1.02*lambda/D (full illumination), HMR (radius) is 0.72deg. If the centroid to
vertex distance of an equliateral triangle is x, the triangle has sides root(3).x
Therefore we want a pitch in band 1 of 1.25 deg = 0.75 * lambda(midband)/D
"""
spacing_Factor = 0.75

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

band_freqs = {1: 917.5, 2: 1119.5, 3: 1375.5, 4: 1631.5}


def arg_init():
    aces_cfg = ACESConfig()
    beam_names = aces_cfg.footprint_factory.get_footprint_names()
    parser = ap.ArgumentParser(prog='footprint', formatter_class=ap.RawDescriptionHelpFormatter,
                               description='',
                               epilog='See -x for more explanation')
    parser.add_argument('inFile', nargs="?", help="Read offsets or absolute positions from INFILE")
    parser.add_argument('-n', dest='name', choices=beam_names, help="Name of footprint")
    parser.add_argument('-b', '--band', type=int, default=1, choices=[1, 2, 3, 4],
                        help="Band id used in creating parsets and determining beam spacing (override with --pitch); "
                             "default=1")
    parser.add_argument('-a', '--angle', dest='PA', default=0.0, type=float,
                        help="Position angle of footprint (degrees)")
    parser.add_argument('-d', '--dLM', dest='dLM', default=[0.0, 0.0], type=vec2, help="Bulk shift (l,m) (degrees)")
    parser.add_argument('-p', '--pitch', type=float, help="Beam spacing in degrees")
    parser.add_argument('-i', '--interval', type=float, default=60.0,
                        help="Dwell time on each offset position (seconds)")
    parser.add_argument('-s', '--sun', action='store_true', help="Produce parset for Solar beamforming obs")
    parser.add_argument('-T', '--taurus', action='store_true', help="Produce parset for beamforming on Taurus A")
    parser.add_argument('-V', '--virgo', action='store_true', help="Produce parset for beamforming on Virgo A")
    parser.add_argument('-B', '--b1934', action='store_true', help="Produce parset for beamforming on B1934-638")
    parser.add_argument('-c', '--cal', nargs='?', const='B1934-638',
                        help="Produce parset for beam calibration observations")
    parser.add_argument('-t', '--tos', action='store_true', default=False,
                        help="Print command string for TOS footprint tool")
    parser.add_argument('-o', '--overlay', metavar="oName", help="Generate overlay file with this name")
    parser.add_argument('-f', '--format', choices=["kvis", "ds9", "miriad", "png", "aladin_fov", "aladin_rgn", "casa"],
                        default='kvis', help="Format of overlay file")
    parser.add_argument('-w', '--fwhm', type=float, help="Beam FWHM used in overlay files (degrees)")
    parser.add_argument('-r', '--reference', metavar="'RA,Dec'", default=[0.0, 0.0], action=Celpos)
    parser.add_argument('-e', '--error', metavar="'Date,time'", help="Erroneous beam shift for date,time "
                                                                     "yyyy/mm/dd hh:mm:ss")
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-x', '--explain', action='store_true', help="Give an expanded explanation")
    return parser, aces_cfg


class Celpos(ap.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed")
        super(Celpos, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):

        logger.debug('ACTION : %r %r %r' % (namespace, values, option_string))
        if values in catalogue.keys():
            # noinspection PyTypeChecker
            a, b = parse_direction(catalogue[values])
            rp = [np.radians(a), np.radians(b)]
        else:
            a, b = parse_direction(values)
            rp = [np.radians(a), np.radians(b)]
        setattr(namespace, self.dest, rp)


def vec2(s):
    vec = map(float, s.split(','))
    return vec


def write_aladin_footprint(fp, fpname, fwhm, out_filename):
    nbeams = fp.n_beams

    afp = aladin.AladinFootprint(fpname, 'ASKAP', 'PAF-%d' % nbeams, fpname, 'CSIRO')
    afp.add_square('Handles', 5000, 5000)
    fwhm_arcsec = fwhm * 3600.
    radius_arcsec = fwhm_arcsec / 2.
    aoffsets = np.degrees(fp.offsetsRect) * 3600.
    # print 'Aladin footprint using interlave', fp.get_interleaves()[0]
    # fpb = fp.get_interleaved_footprint(0)
    # boffsets = np.degrees(fpb.offsetsRect) * 3600.

    for i in range(fp.n_beams):
        afp.add_circle('Beam%dA' % i, aoffsets[i, 0], aoffsets[i, 1], radius_arcsec)

    #    for i in range(fp.n_beams):
    #        afp.add_circle('Beam%dB'%i, boffsets[i, 0], boffsets[i, 1], radius_arcsec)

    afp.writeto(out_filename)


def write_overlay_file(filename, overlays):
    """Write the overlay strings to a file.
    
    Arguments:
        filename {str} -- Filename to which the overlays strings will be written.
        overlays {list} -- List of overlay strings to write to `filename`. A new line character
            will be inserted between each element.
    """
    with open(filename, 'w') as overlay_file:
        for overlay in overlays:
            print(overlay, file=overlay_file)


def main():
    # parse command line options

    parser, aces_cfg = arg_init()
    fp_factory = aces_cfg.footprint_factory
    args = parser.parse_args()
    if args.explain:
        print(explanation)
        sys.exit(0)
    if args.error:
        beam_date = args.error
        print("Providing beam offset for beams formed on %s" % beam_date)
        # noinspection PyUnresolvedReferences
        sun = ephem.Sun()
        d = ephem.Date(beam_date)
        sun.compute(d)
        s1 = Skypos(sun.ra, sun.dec)
        s2 = Skypos(sun.a_ra, sun.a_dec)
        print('s1 = ', s1)
        print('s2 = ', s2)
        dpa = s1.d_pa(s2)
        dlm = dp_to_lm(dpa)
        print(" Offset %6.2f arcmin at PA %6.1f deg" % (dpa[0] * 180 / pi * 60, dpa[1] * 180 / pi))
        print(" Offsets l = %6.2f, m = %6.2f arcmin" % (dlm[0] * 180 / pi * 60, dlm[1] * 180 / pi * 60))
        sys.exit(0)
    if args.verbose:
        print("ARGS = ", args)

    preamble = ["          Date : %s" % (time.strftime("%Y-%m-%d"))]

    lambda_on_d = 300.0 / band_freqs[args.band] / 12.0 * 180 / pi
    std_pitch = np.degrees(fpm.Footprint.standard_pitch(band_freqs[args.band]))
    if args.pitch is None:
        pitch = std_pitch
    else:
        pitch = args.pitch
    if args.fwhm is None:
        fwhm = 1.02 * lambda_on_d
    else:
        fwhm = args.fwhm
    if args.inFile is not None:
        parset = ParameterSet(args.inFile)
        fp = fpm.from_parset(parset, np.radians(pitch), np.radians(args.PA))
        preamble.append("Custom footprint from %s" % args.inFile)
        logger.info("Custom footprint from %s" % args.inFile)
    elif args.name is not None:
        lm_bore = np.array(args.dLM) * pi / 180
        fp = fp_factory.make_footprint(args.name, pitch * pi / 180, args.PA * pi / 180, lm_boresight=lm_bore)
        preamble.append("          Band : %s" % args.band)
        preamble.append("     Footprint : %s" % args.name)
        preamble.append("         Pitch : %5.2f degrees" % pitch)
        preamble.append("Position angle : %5.2f degrees" % args.PA)
    else:
        fp = None

    for p in preamble:
        print(p)

    if fp is None:
        print("Nothing to do. Try -h")
        sys.exit(0)
    else:
        ref_pos = args.reference

        if args.verbose:
            print('refPos = ', ref_pos)
        fp.set_refpos(ref_pos)
        if True:
            dpas = np.array(fp.offsetsPolar) * 180 / pi
            lms = np.array(fp.offsetsRect) * 180 / pi
            # print fp.positions[0]
            print()
            print("Beam       (D,PA)           (l,m)            RA         Dec")
            for i in range(fp.n_beams):
                dp = dpas[i]
                lm = lms[i]
                ra, dec = fp.positions[i].get_ras(), fp.positions[i].get_decs()
                print(" %d   (%5.3f %7.2f)  (%6.3f %6.3f)  %s,%s" % (i, dp[0], dp[1], lm[0], lm[1], ra, dec))
            print()
            print("Inter-leaving centres, with associated PA adjustments:")
            for p, a in zip(fp.get_interleaves(), fp.get_interleave_pa()):
                ra, dec = p.get_ras(), p.get_decs()
                print("  %s,%s  %7.2f deg" % (ra, dec, a * 180 / pi))

        if args.tos:
            print(fp.to_parset())

        if args.overlay:
            radius = fwhm / 2.0
            if args.format == 'miriad':
                overlay_filename = "%s.olay" % args.overlay
                overlays = []
                for i, position in enumerate(fp.positions):
                    overlay = "ocircle absdeg absdeg {label} yes {ra:9.5f} {dec:9.5f} {radius:6.3f}".format(
                        ra=position.ra * 180 / pi,
                        dec=position.dec * 180 / pi,
                        radius=radius,
                        label=i
                    )
                    overlays.append(overlay)
                for i, position in enumerate(fp.get_interleaves()):
                    overlay = "star absdeg absdeg {label} yes {ra:9.5f} {dec:9.5f} {radius:6.3f}".format(
                        ra=position.ra * 180 / pi,
                        dec=position.dec * 180 / pi,
                        radius=radius / 10,
                        label=i
                    )
                    overlays.append(overlay)
                write_overlay_file(overlay_filename, overlays)
            elif args.format == 'kvis':
                overlay_filename = "%s.ann" % args.overlay
                overlays = ["colour white"]
                for i, position in enumerate(fp.positions):
                    overlay = "circle W {ra:9.5f} {dec:9.5f} {radius:6.3f}".format(
                        ra=position.ra * 180 / pi,
                        dec=position.dec * 180 / pi,
                        radius=radius
                    )
                    overlays.append(overlay)
                    overlay = "text W {ra:9.5f} {dec:9.5f} {label}".format(
                        ra=position.ra * 180 / pi,
                        dec=position.dec * 180 / pi,
                        label=i
                    )
                    overlays.append(overlay)
                for i, position in enumerate(fp.get_interleaves()):
                    overlay = "cross W {ra:9.5f} {dec:9.5f} {radius:6.3f} {radius:6.3f}".format(
                        ra=position.ra * 180 / pi,
                        dec=position.dec * 180 / pi,
                        radius=radius / 10
                    )
                    overlays.append(overlay)
                    overlay = "text W {ra:9.5f} {dec:9.5f} {label}".format(
                        ra=position.ra * 180 / pi,
                        dec=position.dec * 180 / pi,
                        label=i
                    )
                    overlays.append(overlay)
                write_overlay_file(overlay_filename, overlays)
            elif args.format == 'ds9':
                overlay_filename = "%s.reg" % args.overlay
                overlays = ["global color=white", "fk5"]
                for i, position in enumerate(fp.positions):
                    overlay = "ellipse({ra},{dec},{major:.2f}d,{minor:.2f}d,{pa:d}d)".format(
                        ra=position.get_ras(),
                        dec=position.get_decs(),
                        major=radius,
                        minor=radius,
                        pa=0
                    )
                    overlays.append(overlay)
                    overlay = "text({ra},{dec}) # text={{{text}}}".format(
                        ra=position.get_ras(),
                        dec=position.get_decs(),
                        text=i
                    )
                    overlays.append(overlay)
                write_overlay_file(overlay_filename, overlays)
            elif args.format == 'casa':
                overlay_filename = "%s.crtf" % args.overlay
                overlays = ["#CRTF", "global coord=J2000, color=white"]
                for i, position in enumerate(fp.positions):
                    overlay = "ellipse[[{ra}, {dec}], [{major:.2f}deg, {minor:.2f}deg], " \
                              "{pa:d}deg], label='{label}'".format(
                                ra=position.get_ras(),
                                # casa expects sexigesimal dec strings in format dd.mm.ss.sss
                                dec=position.get_decs().replace(':', '.'),
                                major=radius,
                                minor=radius,
                                pa=0,
                                label=i)
                    overlays.append(overlay)
                write_overlay_file(overlay_filename, overlays)
            elif args.format == 'png':
                overlay_filename = "%s.png" % args.overlay
                plt.ioff()
                plt.clf()
                plt.gcf().add_axes([0.15, 0.15, 0.7, 0.7], aspect="equal")
                for i in range(fp.n_beams):
                    x0, y0 = fp.offsetsRect[i] * 180 / np.pi
                    # x0 is sign reversed here because we are often using the overlay on RA/DEC plots in the
                    # southern hemisphere.  We should document this better so that we understand what the overlay
                    # is supposed to represent and what the coordinates are.
                    x0 *= -1.0
                    x, y = make_circle(radius, x0, y0)
                    plt.plot(x, y, '-k', lw=0.6)
                    plt.grid()
                    plt.text(x0, y0, "%d" % i, va='center', ha='center', color='b')
                for i, p in enumerate(fp.interOffsRect):
                    x0, y0 = p * 180 / np.pi
                    x0 *= -1.0
                    r0 = np.sqrt(x0 * x0 + y0 * y0)
                    if r0 > 0.0:
                        plt.plot([x0], [y0], 'ok', ms=3.0)
                        plt.plot([x0], [y0], 'o', mec='k', mfc='none', ms=6.0)
                        hw, hl = 0.1, 0.1
                        hlf = hl / r0
                        plt.arrow(0.0, 0.0, x0*(1.0-hlf), y0*(1.0-hlf), head_width=hw, head_length=hl)
                plt.plot([0.0], [0.0], '+k')
                rmax = fp.offsetsPolar[:, 0].max() * 180 / np.pi + radius
                plt.xlim(-rmax * 1.02, rmax * 1.02)
                plt.ylim(-rmax * 1.02, rmax * 1.02)
                plt.title("'%s' pitch=%4.3f$^\circ$ angle=%4.0f$^\circ$" % (fp.name, pitch, args.PA))
                plt.savefig(overlay_filename, dpi=350, transparent=True)

            elif args.format == 'aladin_fov':
                overlay_filename = "%s.vot" % args.overlay
                fpname = 'ASKAP-%dbm-%s-%s' % (fp.n_beams, fp.name, pitch)
                write_aladin_footprint(fp, fpname, fwhm, overlay_filename)

            elif args.format == 'aladin_rgn':
                overlay_filename = "%s.txt" % args.overlay
                overlays = ["Object\tCont_Flag\tRAJ2000\tDEJ2000\tX\tY\tLabel_Flag\tInfo"]
                for i, position in enumerate(fp.positions):
                    overlay = "phot\t.\t{ra:.6f}\t{dec:.6f}\t0.0\t0.0\ttrue\t{overlay} {label:02d}|{radius:.3f}".format(
                        ra=position.ra * 180 / pi,
                        dec=position.dec * 180 / pi,
                        radius=radius,
                        overlay=args.overlay,
                        label=i
                    )
                    overlays.append(overlay)
                write_overlay_file(overlay_filename, overlays)
            else:
                raise ValueError('Invalid overlay format: {}'.format(args.format))

            print("%s written in %s format." % (overlay_filename, args.format))

        if args.sun:
            delta_time = args.interval / 60.0
            now = ephem.now()
            now_time = ephem.Date(now)
            # sun = ephem.Sun()
            # sun.compute(oTime)
            # correction 2014Sep18 to use a_ra, a_dec rather than ra,dec
            # rp = [sun.a_ra,sun.a_dec]
            # fp.setRefpos(rp)
            fp.useSunRef(delta_time)
            posns = fp.get_positions(reverse=True)
            pa_corr = fp.get_pa_corr() * 180 / pi
            obtime = ephem.date(now_time)
            write_parset("sun.parset", "ACM", args.band, posns, pa_corr, obtime, "Sun", preamble, args.interval)
            print("Boresight pointings:")
            for i in range(fp.n_beams):
                ra, dec = posns[i].get_ras(), posns[i].get_decs()
                print("  Beam %d %s,%s  %5.1f" % (i, ra, dec, pa_corr[i]))

        if args.taurus:
            cal = 'TaurusA'
            print("\nReference %s at %s" % (cal, catalogue[cal]))
            a, b = parse_direction(catalogue[cal])
            rp = [np.radians(a), np.radians(b)]
            fp.set_refpos(rp)
            posns = fp.get_positions(reverse=True)
            pa_corr = fp.get_pa_corr() * 180 / pi
            obtime = ephem.now()
            write_parset("taurus.parset", "ACM", args.band, posns, pa_corr, obtime, "Taurus", preamble, args.interval)
            print("Boresight pointings:")
            for i in range(fp.n_beams):
                ra, dec = posns[i].get_ras(), posns[i].get_decs()
                print("  Beam %d %s,%s  %5.1f" % (i, ra, dec, pa_corr[i]))

        # todo: this should be merged with taurus option
        if args.virgo:
            cal = 'VirgoA'
            print("\nReference %s at %s" % (cal, catalogue[cal]))
            a, b = parse_direction(catalogue[cal])
            rp = [np.radians(a), np.radians(b)]
            fp.set_refpos(rp)
            posns = fp.get_positions(reverse=True)
            pa_corr = fp.get_pa_corr() * 180 / pi
            obtime = ephem.now()
            write_parset("virgo.parset", "ACM", args.band, posns, pa_corr, obtime, "VirgoA", preamble, args.interval)
            print("Boresight pointings:")
            for i in range(fp.n_beams):
                ra, dec = posns[i].get_ras(), posns[i].get_decs()
                print("  Beam %d %s,%s  %5.1f" % (i, ra, dec, pa_corr[i]))

        # todo: this should be merged with taurus and virgo options
        if args.b1934:
            cal = 'B1934-638'
            print("\nReference %s at %s" % (cal, catalogue[cal]))
            a, b = parse_direction(catalogue[cal])
            rp = [np.radians(a), np.radians(b)]
            fp.set_refpos(rp)
            posns = fp.get_positions(reverse=True)
            pa_corr = fp.get_pa_corr() * 180 / pi
            obtime = ephem.now()
            write_parset("b1934.parset", "ACM", args.band, posns, pa_corr, obtime, "B1934-638", preamble, args.interval)
            print("Boresight pointings:")
            for i in range(fp.n_beams):
                ra, dec = posns[i].get_ras(), posns[i].get_decs()
                print("  Beam %d %s,%s  %5.1f" % (i, ra, dec, pa_corr[i]))

        if args.cal:
            cal = args.cal
            if cal in catalogue.keys():
                print("\nCalibrator %s at %s" % (cal, catalogue[cal]))
                a, b = parse_direction(catalogue[cal])
                rp = [np.radians(a), np.radians(b)]
            else:
                a, b = parse_direction(cal)
                rp = [np.radians(a), np.radians(b)]
                print("\nCalibrator at %s,%s" % (a, b))
            ref_pos = rp
            fp.set_refpos(ref_pos)
            posns = fp.get_positions(reverse=True)
            pa_corr = fp.get_pa_corr() * 180 / pi
            for i in range(fp.n_beams):
                ra, dec = posns[i].get_ras(), posns[i].get_decs()
                print("   Beam %d   %s,%s  %8.4f" % (i, ra, dec, pa_corr[i]))
            write_parset("%s.parset" % args.cal, "CAL", args.band, posns, pa_corr, "", args.cal, preamble,
                         args.interval, [a, b])

    print("Done")


def write_parset(name, obs_type, band, positions, pos_angles, obs_time, field_name, preamble, duration, point_pos=None):
    # name : Name of parset file
    # ObType: "ACM" for sun measurements with ACMs, "CAL" for calibration of each beam.
    # band : 1, 2, 3 or 4
    # positions : sky positions for each boresight pointing
    # pAngles : position angles for each pointing
    # fieldName : used to label each field (_beam%d appended to this)
    # duration : integration in seconds.
    if point_pos is None:
        point_pos = []
    # PAF measuremnt on SUN with ACMs
    blank_pos = positions[0].offset([15.0 * pi / 180, pi])

    if obs_type not in ["ACM", "CAL"]:
        raise(ValueError, "Incorrect obs_type into write_parset : %s" % obs_type)
    if obs_type == "ACM":
        print("            Reference position %s" % (positions[0]))
        print("Blank sky observation position %s\n" % blank_pos)
        enable_cp = "false"
        op = "formation"
    else:
        enable_cp = "true"
        op = "calibration"
    fo = open(name, 'w')
    fo.write("# Written by footprint.py for beam %s\n" % op)
    for pr in preamble:
        fo.write("# %s\n" % pr)
    if obs_type == "ACM":
        time_advice = "Reference source position computed for %s (UTC)" % obs_time
        print(time_advice)
        fo.write("# %s\n" % time_advice)
    fo.write("common.enable_cp = %s\n" % enable_cp)
    fo.write("common.enable_datacapture = true\n")
    fo.write("datacapture.acm_frequency_index = 0\n")
    fo.write("common.target.src%s.duration = %d\n" % ("%d", duration))
    fo.write("common.target.src%s.pol_axis = [pa_fixed, 0.0]\n" % "%d")
    fo.write("common.target.src%s.sky_frequency = %6.1f\n" % ("%d", band_freqs[band]))
    fo.write("common.target.src%d.beam_weights = \n")
    k = 0
    t = []
    if obs_type == "ACM":
        fo.write("common.target.src1.field_name = blank\n")
        fo.write("common.target.src1.duration = %d\n" % duration)
        r, d = [blank_pos.get_ras(), blank_pos.get_decs()]
        fo.write("common.target.src1.field_direction = [%s,%s,J2000]\n" % (r, d))
        t = ['src1']
        k = 1
    elif obs_type == "CAL":
        if point_pos is not []:
            r, d = point_pos[0], point_pos[1]
        else:
            r, d = [positions[0].get_ras(), positions[0].get_decs()]
        fo.write("common.target.src%s.phase_direction = [%s,%s,J2000]\n" % ('%d', r, d))
        t = []
        k = 0
    fo.write("\n")
    for p, pa in zip(positions, pos_angles):
        r, d = [p.get_ras(), p.get_decs()]
        fo.write("common.target.src%d.field_name = %s_beam%d\n" % (1 + k, field_name, k))
        fo.write("common.target.src%d.field_direction = [%s,%s,J2000]\n" % (1 + k, r, d))
        fo.write("common.target.src%s.pol_axis = [pa_fixed, %8.4f]\n" % (1 + k, pa))
        t.append("src%d" % (1 + k))
        k += 1
    t = ",".join(t)
    fo.write("common.targets = [%s]\n" % t)
    fo.close()


def make_circle(rad, x0, y0):
    th = np.arange(0, 361, 1) * np.pi / 180
    x = x0 + rad * np.cos(th)
    y = y0 + rad * np.sin(th)
    return x, y


if __name__ == "__main__":
    sys.exit(main())
'''
common.enable_cp =false
common.target.src%d.duration = 120
common.target.src%d.pol_axis = [pa_fixed, 0.0]
common.target.src%d.sky_frequency = 1375.5

common.target.src1.field_name = beam1
common.target.src1.field_direction = [07:20:49.2, 22:08:09.9, J2000]
common.target.src2.field_name = beam2
common.target.src2.field_direction = [07:22:59.5, 23:00:04.3, J2000]
common.target.src3.field_name = beam3
common.target.src3.field_direction = [07:25:08.3, 22:07:57.1, J2000]
common.target.src4.field_name = beam4
common.target.src4.field_direction = [07:22:57.9, 21:16:09.5, J2000]
common.target.src5.field_name = beam5
common.target.src5.field_direction = [07:18:40.4, 21:16:09.5, J2000]
common.target.src6.field_name = beam6
common.target.src6.field_direction = [07:16:30.1, 22:07:57.1, J2000]
common.target.src7.field_name = beam7
common.target.src7.field_direction = [07:18:38.8, 23:00:04.3, J2000]
common.target.src8.field_name = beam8
common.target.src8.field_direction = [07:27:15.5, 21:15:44.0, J2000]
common.target.src9.field_name = beam9
common.target.src9.field_direction = [07:14:18.1, 22:59:38.3, J2000]
common.target.src10.field_name = blank
common.target.src10.field_direction = [06:20:00.0, 22:00:00.0, J2000]
common.target.src10.duration = 300
common.targets = [src10,src1,src2,src3,src4,src5,src6,src7,src8,src9]
'''
