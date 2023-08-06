# Script  for analysing 1934-638 cal observations to compute SEFD.
# David McConnell
# 2015 Apr ...
# 2018 Feb 6  to new aces package
#
from __future__ import print_function
from __future__ import print_function
from aces.sefd import sefd__cc as se
import os
import warnings

import askap.parset.parset as ps


# This should be submitted to the batch system via scripts/sefdProcessing.sh

def set_warn_filters():
    warnings.resetwarnings()
    filters = [{'action': 'ignore',  'message': 'converting a masked element to nan.',
                'category': UserWarning}]
    for f in filters:
        warnings.filterwarnings(**f)


#
# ---------------------------------------
# start execution here
#

set_warn_filters()

# Set default inputs:
inp = ps.ParameterSet('SEFD_defaults.parset').to_dict()

# get any override inputs:
# Get inputs:
if 'INPUTS' in os.environ.keys():
    inp_file = os.environ['INPUTS']
else:
    inp_file = 'SEFD_inputs.parset'
inc = ps.ParameterSet(inp_file).to_dict()


ODIR = os.getcwd()

# assert isinstance(inp, dict)
inp.update(inc)

sbid = inp['sbid']
if 'SLURM_ARRAY_TASK_ID' in os.environ.keys():
    beams = [int(os.environ['SLURM_ARRAY_TASK_ID'])]
else:
    beams = inp['beams']
scan = inp['scan']
start = inp['start']
dnt = inp['nTimAvg']
nct = inp['nTimCells']

ch0 = inp['chan0']
dch = inp['nChanAvg']
ncF = inp['nFrqCells']

doDecompose = inp['decompose']

outfile_base = os.path.join(ODIR, inp['outfile_base'])

print("Beams = {}".format(beams))
for beam in beams:
    fname = outfile_base % (sbid, beam)
    if scan >= 0:
        sc = scan
    else:
        sc = beam
    if sbid == 2024:
        # special case for SBID 2024 in which the fist beam is absent.
        sc = beam + 1
        print('Processing 2024 with beam %d, scan %d' % (beam, sc))

    # TODO
    # - potential delayed start for first scan. Review after TOS FR implemented.
    # if sc == 0:
    #     start += 15
    d = se.SEFD(sbid, file_name=None, beam=beam, dch=dch, ch0=ch0, ncf=ncF, scan=sc, dnt=dnt, nstart=start, nct=nct)
    d.summary()
    d.calc_sefd()
    if doDecompose:
        d.decompose(what="SEFD")
        d.decompose(what="SCALE")
        # d.decompose(what="RAWAMPL")
        # d.plot_A(fname)
    d.save_pickle(fname)
