#!/usr/bin/env python3
import sys
from aces.askapdata.schedblock import SchedulingBlock
from aces.obsplan.config import ACESConfig
from astropy.coordinates import SkyCoord
from astropy import units as u
import numpy as np

aces_cfg = ACESConfig()
fp_factory = aces_cfg.footprint_factory


def main(mySBID, outfile=None, field=-1):
    sb = SchedulingBlock(mySBID)
    name = sb.get_footprint_name()
    pitch = sb.get_footprint_pitch()
    rot = sb.get_footprint_rotation()
    params = sb.get_parameters()

    fp = fp_factory.make_footprint(
            f"ak:{name}",
            np.deg2rad(pitch),
            np.deg2rad(rot - 45),
            )

    targets = params["common.targets"][1:-1].split(",")
    target = targets[field].replace(' ', '')
    field_direction = params[f'common.target.{target}.field_direction'].strip('][').strip(' ').split(',')

    field_coord = SkyCoord(field_direction[0], field_direction[1], unit=(u.hourangle, u.deg))
    fp.set_refpos([field_coord.ra.rad, field_coord.dec.rad])
    dpas = np.degrees(np.array(fp.offsetsPolar))
    lms = np.degrees(np.array(fp.offsetsRect))
    # print()
    # print("Beam       (D,PA)           (l,m)            RA         Dec")
    for i in range(fp.n_beams):
        dp = dpas[i]
        lm = lms[i]
        ra, dec = fp.positions[i].get_ras(), fp.positions[i].get_decs()
        # print(" %d   (%5.3f %7.2f)  (%6.3f %6.3f)  %s,%s" % (i, dp[0], dp[1], lm[0], lm[1], ra, dec))
        print(f"{i:2d}  ({lm[0]:6.3f} {lm[1]:6.3f})  {ra},{dec}")

    if outfile is not None:
        with open(outfile, 'w+') as f:
            for i in range(fp.n_beams):
                dp = dpas[i]
                lm = lms[i]
                ra, dec = fp.positions[i].get_ras(), fp.positions[i].get_decs()
                # print(" %d   (%5.3f %7.2f)  (%6.3f %6.3f)  %s,%s" % (i, dp[0], dp[1], lm[0], lm[1], ra, dec))
                print(f"{i:2d}  ({lm[0]:6.3f} {lm[1]:6.3f})  {ra},{dec}", file=f)

def cli():
    descStr = """
    Get the footprint for a given SBID
    """
    import argparse

    # Parse the command field_directionline options
    parser = argparse.ArgumentParser(
        description=descStr, formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "sbid",
        metavar="sbid",
        type=int,
        help="SBID of observation.",
    )
    parser.add_argument(
        "--file",
        type=str,
        help="Optionally save to output file.",
    )
    parser.add_argument(
        "--field",
        type=int,
        default=-1,
        help="Optionally specify field index [defaults to -1].",
    )
    args = parser.parse_args()

    main(
        mySBID=args.sbid,
        outfile=args.file,
        field=args.field,
    )


if __name__ == "__main__":
    sys.exit(cli())
