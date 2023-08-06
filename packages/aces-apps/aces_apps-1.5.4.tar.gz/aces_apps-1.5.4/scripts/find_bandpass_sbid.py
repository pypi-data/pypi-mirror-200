#!/usr/bin/env python
from __future__ import print_function
import argparse
from datetime import timedelta
import dateutil.parser
from aces.askapdata.schedblock import SchedulingBlock as _SchedulingBlock, SB


class SchedulingBlock(_SchedulingBlock):
    def get_executive_times(self, trunc_microsecond=False):
        exec_obs_vars = self._service.getObsVariables(self.id, 'executive')
        times = [dateutil.parser.parse(v) for k, v in exec_obs_vars.items() if k in (
            'executive.start_time', 'executive.stop_time')]
        if trunc_microsecond:
            times = map(lambda td: td.replace(microsecond=0), times)
        return sorted(times)


ACTIVE_STATES = ['PROCESSING', 'PENDINGARCHIVE', 'COMPLETED', 'OBSERVED']
active_states_enums = [getattr(SB.ObsState, state) for state in ACTIVE_STATES]

parser = argparse.ArgumentParser(
    description='Find candidate SBIDs of bandpass observations for a given target SBID by searching for scheduling blocks with the same weights prefix.')
parser.add_argument(
    'sbid', type=int, help='SBID of science target observation.')
parser.add_argument('--search-days', type=int, default=3,
                    help='Number of days to search around target observation for bandpass observations. Default: 3.')
args = parser.parse_args()

# date window to look for bandpass SBIDs around target SBID
d_date = timedelta(days=args.search_days)

# create a SchedulingBlock object given the SBID of the science target
target_sb = SchedulingBlock(args.sbid)
sb_service = target_sb._service  # pick out the ICE service
target_weights = target_sb.get_weights_prefix()
target_start_time, target_end_time = target_sb.get_executive_times(
    trunc_microsecond=True)

# get all bandpass SBIDs
bandpass_sbids = sb_service.getByTemplate('Bandpass', -1)

# get all active SBIDs since around the target SBID date
search_start_time = target_start_time - d_date
search_end_time = target_start_time + d_date
active_sbids = sb_service.getByState(
    active_states_enums, search_start_time.isoformat(sep=' '))
exclude_active_sbids = sb_service.getByState(
    active_states_enums, search_end_time.isoformat(sep=' '))
active_sbids = set(active_sbids) - set(exclude_active_sbids)
active_bandpass_sbids = active_sbids & set(bandpass_sbids)

# get the weights file prefix for each active bandpass SBID and report any that match the target
bandpass_candidates = []
for bandpass_sbid in active_bandpass_sbids:
    sb = SchedulingBlock(bandpass_sbid)
    weights = sb.get_weights_prefix()
    if weights == target_weights:
        bp_start_time, bp_end_time = sb.get_executive_times(
            trunc_microsecond=True)
        bp_target_dtime = min(
            abs(target_start_time - bp_end_time), abs(target_end_time - bp_start_time))
        bandpass_candidates.append(
            {'sbid': bandpass_sbid, 'target_dtime': bp_target_dtime})

if len(bandpass_candidates) > 0:
    bandpass_candidates = sorted(
        bandpass_candidates, key=lambda d: d['target_dtime'])
    print('{:5s} {}'.format("SBID", "Min. time to target observation"))
    for bandpass_candidate in bandpass_candidates:
        print('{:5} {}'.format(
            bandpass_candidate['sbid'], bandpass_candidate['target_dtime']))
else:
    print('No matching bandpass observations found. Try widening the search period by increasing --search-days.')
