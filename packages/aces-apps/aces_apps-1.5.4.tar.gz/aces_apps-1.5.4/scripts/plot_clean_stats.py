#!/usr/bin/env python
from __future__ import print_function
import argparse
import matplotlib.pyplot as plt
from aces.cleanlog.clean_parser import parse_clean_log


parser = argparse.ArgumentParser(description='Plot deconvolution data extracted from an ASKAPsoft imager log.')
parser.add_argument('log_file', help='Output log file from imager.')
parser.add_argument('--logscale', action='store_true', help='Plot the y-axis with a log scale.')
parser.add_argument('--save', help='Save the plot with the given filename instead of displaying interactively.')

args = parser.parse_args()
df = parse_clean_log(args.log_file)

fig, (ax_total, ax_peak) = plt.subplots(nrows=2, sharex=True, gridspec_kw=dict(hspace=0), figsize=(7, 9))
for major_cycle, data in df.groupby('major_cycle'):
    # noinspection PyUnresolvedReferences
    lines = ax_total.plot('iteration', 'total_flux', '.-', data=data, label=major_cycle,
                          color=plt.cm.tab20(major_cycle))
    # noinspection PyUnresolvedReferences
    ax_peak.plot('iteration', 'peak_resid', '.-', data=data, label='_', color=plt.cm.tab20(major_cycle))

XAXIS_TICK_PARAMS = dict(direction='inout', bottom=True, top=True)
ax_total.xaxis.set_tick_params(**XAXIS_TICK_PARAMS)
ax_peak.xaxis.set_tick_params(**XAXIS_TICK_PARAMS)

ax_peak.set_xlabel('Minor cycle iteration')
ax_peak.set_ylabel('Peak residual')
ax_total.set_ylabel('Total flux')
# fig.tight_layout()
fig.legend(loc='right', bbox_to_anchor=(1.02, 0.5), frameon=False, title='Major cycle')

if args.logscale:
    ax_peak.set(yscale='log')

# print major cycle stop reasons
print('{:12s} {}'.format('Major cycle', 'Stop reason'))
for datetime, series in df.loc[~df.major_stop_reason.isna()].iterrows():
    print('{:<12d} {}'.format(series.major_cycle, series.major_stop_reason))

if args.save:
    fig.savefig(args.save, bbox_inches='tight')
else:
    plt.tight_layout(rect=[0, 0, 0.9, 1])
    plt.show()
