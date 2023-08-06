#!/usr/bin/env python
from aces.askapdata.schedblock import SchedulingBlock as _SchedulingBlock
import askap.interfaces.schedblock as SB  # noqa

from astropy.time import Time


def bsect(x, z):
    """
    Find position in array x of value z; assumes x sorted in increasing order.
    Returns j such that x[j] <= z < x[j+1]
    """
    n = len(x)
    if n == 0:
        return 0
    j1 = 0
    j2 = n
    j = j1

    while (j2 - j1) > 1:
        j = (j1 + j2) // 2
        if x[j] == z:
            break
        if x[j] > z:
            j2 = j
        else:
            j1 = j
        if x[j] > z:
            j = j - 1
    return j


verbose = True
obs_program = "AS110"
epoch = "RACS_"
epoch_name = "racs_epoch_2"
start_date = "2020-12-20 00:00:00"

sb = _SchedulingBlock(20147)
sb_service = sb._service

ACTIVE_STATES = ['PROCESSING', 'PENDINGARCHIVE', 'COMPLETED', 'OBSERVED']
active_states_enums = [getattr(SB.ObsState, state) for state in ACTIVE_STATES]

# Get all SBIDs for this project since given date
sbids = sb_service.getByObsProgram(obs_program, start_date)
print("Found {:d} SBIDS".format(len(sbids)))
sbids.sort()

# Sort into science and bandpass observations, rejecting ERRORED, RETIRED etc,
sci_sbids = []
cal_sbids = []
for sbid in sbids:
    state = str(sb_service.getState(sbid))
    if state in ACTIVE_STATES:
        alias = sb_service.getAlias(sbid)
        if alias.find(epoch) == 0:
            sci_sbids.append(sbid)
        elif alias.find("Bandpass") == 0:
            cal_sbids.append(sbid)
        else:
            print("Odd alias at {:d} {}".format(sbid, alias))
    elif verbose:
        print("{:d}  {}  {}".format(sbid, state, sb_service.getAlias(sbid)))
print("Found the following CAL_SBIDs for %s : " % epoch)
print(cal_sbids)

# For each science obs, find best CAL obs, match with field name and write out
print("Extracting parsets ...")
general_target = "src%d"
ids = []
fields = []
sbids = []
vast_params = {}
fout_map = open("%s_mapping.csv" % (epoch_name), "wt")
fout_map.write("cal_sbid,sbid,field\n")
for sbid in sci_sbids:
    if verbose:
        print("SBID: %s" % sbid)
    sb = _SchedulingBlock(sbid)

    sb_params = sb.get_parameters()
    sb_vars = sb.get_variables()
    st_start = sb_vars['executive.start_time']

    j = bsect(cal_sbids, sbid)
    if verbose:
        print("j = {:d}".format(j))
    if j == len(cal_sbids) - 1:
        sbid_cal = cal_sbids[j]
    else:
        sbc0 = _SchedulingBlock(cal_sbids[j])
        sbc1 = _SchedulingBlock(cal_sbids[j + 1])

        sbc0_vars = sbc0.get_variables()
        sbc1_vars = sbc1.get_variables()
        c_start0 = sbc0_vars['executive.start_time']
        c_start1 = sbc1_vars['executive.start_time']
        tc0 = Time(c_start0, format='iso', scale='utc')
        tc1 = Time(c_start1, format='iso', scale='utc')
        ts = Time(st_start, format='iso', scale='utc')
        if (ts - tc0) < (tc1 - ts):
            sbid_cal = cal_sbids[j]
        else:
            sbid_cal = cal_sbids[j + 1]

    keys = list(sb_params.keys())
    keys.sort()

    # Find all targets from this SB's parset
    targets = sb_params["common.targets"][1:-1].split(",")
    # targets.append(general_target)
    # print("Targets: ",targets)
    for targ in targets:
        k = "common.target.{}.field_name".format(targ)
        fout_map.write("{:d},{:d},{}\n".format(sbid_cal, sbid, sb_params[k]))

fout_map.close()

print("Done.")
