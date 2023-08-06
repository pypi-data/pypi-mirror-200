#!/usr/bin/env python

# Script  for analysing 1934-638 cal observations to compute SEFD.
# David McConnell
# 2015 Apr ...
# 2018 Feb 6  to new aces package
#
import sys
import os
import warnings
import logging

import askap.parset.parset as ps

from aces.sefd import sefd__cc as se

logger = logging.getLogger(__name__)

# This should be submitted to the batch system via scripts/sefdProcessing.sh

def set_warn_filters():
    warnings.resetwarnings()
    filters = [{'action': 'ignore',  'message': 'converting a masked element to nan.',
                'category': UserWarning}]
    for f in filters:
        warnings.filterwarnings(**f)


version = "2019JUN05"


#
# ---------------------------------------
# start execution here
#
def main(mset_id: int=None):
    logging.info("sefdProcessing version {}".format(version))

    set_warn_filters()

    # Set default inputs:
    inp = ps.ParameterSet('SEFD_defaults.parset').to_dict()

    # get any override inputs:
    # Get inputs:
    if 'INFILE' in os.environ.keys():
        infile_name = os.environ['INFILE']
    else:
        infile_name = None

    if 'INPUTS' in os.environ.keys():
        inp_file = os.environ['INPUTS']
    else:
        inp_file = 'SEFD_inputs.parset'
    inc = ps.ParameterSet(inp_file).to_dict()

    ODIR = os.getcwd()

    # assert isinstance(inp, dict)
    inp.update(inc)

    sbid = inp['sbid']
    if mset_id is None:
        logger.info("No mset_id specified. Attempting to derive. ")
        if 'SLURM_ARRAY_TASK_ID' in os.environ.keys():
            mset_id = int(os.environ['SLURM_ARRAY_TASK_ID'])
        elif 'mset_id' in inp:
            mset_id = inp['mset_id']
        else:
            mset_id = inp['beams'][0]
        
    scan = inp['scan']
    start = inp['start']
    dnt = inp['nTimAvg']
    nct = inp['nTimCells']

    ch0 = inp['chan0']
    dch = inp['nChanAvg']
    ncF = inp['nFrqCells']

    doDecompose = inp['decompose']
    diff = inp['difference']
    uvmin = inp['uvmin']

    outfile_base = os.path.join(ODIR, inp['outfile_base'])

    logger.info("MeasurementSet index = {}".format(mset_id))

    fname = outfile_base.format(sbid, mset_id)

    # TODO
    # - potential delayed start for first scan. Review after TOS FR implemented.
    # if sc == 0:
    #     start += 15
    d = se.SEFD(sbid, file_name=infile_name, mset_inx=mset_id,
                dch=dch, ch0=ch0, ncf=ncF, scan=scan, dnt=dnt,
                nstart=start, nct=nct,
                uvmin=uvmin)
    d.summary()
    d.calc_sefd(difference=diff)
    if doDecompose:
        d.decompose(what="SEFD")
        d.decompose(what="SCALE")
        # d.decompose(what="RAWAMPL")
        # d.plot_A(fname)
    # d.save_pickle(fname)
    d.save_hdf5(fname, per_ant=doDecompose)
    logger.info("Written output to {}".format(fname))


if __name__ == "__main__":
    fmt = '%(asctime)s %(levelname)s  %(name)s %(message)s'
    logging.basicConfig(format=fmt, level=logging.DEBUG)
    sys.exit(main())
