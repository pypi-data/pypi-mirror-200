#!/usr/bin/env python
import os
from pathlib import Path
from aces.survey.survey_class import ASKAP_Survey_factory

sel_in = """Selavy.image                                    = {}
Selavy.sbid                                     = {}
Selavy.sourceIdBase                             = {}
Selavy.imageHistory                             = ["Produced with ASKAPsoft version {}"]
Selavy.imagetype                                = fits
#
# These parameters define the measurement of spectral indices
Selavy.spectralTermsFromTaylor                  = true
Selavy.findSpectralTerms                        = [true, false]
Selavy.spectralTermImages                       = [{}, ]
Selavy.nsubx                                    = 6
Selavy.nsuby                                    = 3
Selavy.overlapx                                 = 0
Selavy.overlapy                                 = 0
#
Selavy.resultsFile                              = {}
#
# Detection threshold
Selavy.snrCut                                   = 5
Selavy.flagGrowth                               = true
Selavy.growthThreshold                          = 3
#
Selavy.VariableThreshold                        = true
Selavy.VariableThreshold.boxSize                = 50
Selavy.VariableThreshold.imagetype              = fits
Selavy.Weights.weightsImage                     = {}
Selavy.Weights.weightsCutoff                    = 0.04
#
Selavy.Fitter.doFit                             = true
Selavy.Fitter.fitTypes                          = [full]
Selavy.Fitter.numGaussFromGuess                 = true
Selavy.Fitter.maxReducedChisq                   = 10.
Selavy.Fitter.imagetype                         = fits
Selavy.Fitter.writeComponentMap                 = false
#
Selavy.threshSpatial                            = 5
Selavy.flagAdjacent                             = true
#
Selavy.minPix                                   = 3
Selavy.minVoxels                                = 3
Selavy.minChannels                              = 1
Selavy.sortingParam                             = -pflux
#
# Precision of values
# Selavy.precFlux                                 = 5
# Selavy.precSize                                 = 4
# Selavy.precShape                                = 4
# Selavy.precPos                                  = 6
# Selavy.precSolidangle                           = 4
# Selavy.precSNR                                  = 4
# Not performing RM Synthesis for this case
Selavy.RMSynthesis                              = false"""

sel_slurm = """#!/bin/bash -l 
#SBATCH --time=04:00:00
#SBATCH --nodes=2
#SBATCH --job-name=selavy
#SBATCH --no-requeue
#SBATCH --export=NONE
#SBATCH --mail-user=david.mcconnell@csiro.au
#SBATCH --mail-type=FAIL
#SBATCH --account=askap
#SBATCH -M galaxy
#SBATCH -p workq

module load askapsoft
module load casa

srun --export=ALL --ntasks=19 --ntasks-per-node=10 selavy -c {}

"""


def gen_selavy(survey, irow, slurm_name, in_name):
    r = survey.f_table[irow]
    fn = survey.survey_files.file_name
    im = fn('mosaic_image_convolved', irow)
    # im = sut.get_product_name(survey, irow, 'mosaic_cres_fcor')
    if r['CAL_SBID'] > 0 and im.exists():
        sbid = r['SBID']
        fld = r['FIELD_NAME']
        # tt1 = sut.get_product_name(survey, irow, 'mosaic_cres_fcor_tt1')
        tt1 = fn('mosaic_image_convolved', irow, taylor=1)
        txt = str(im).replace('fits', 'txt')
        txt = txt.replace('RACS_', 'RACS_test4_1.05_')
        txtp = Path(txt)
        # print(fld, sbid)
        lab = "_{:d}-{}".format(sbid, fld)
        if txtp.exists():
            print('Selavy output already exists {}'.format(txtp))

        # weightim = str(sut.get_product_name(survey, irow, 'weights_cres_fcor_tt0'))
        weightim = str(fn('mosaic_weights', irow))
        parset = in_name
        slurm_in = slurm_name
        fout1 = open(parset, "w")
        fout2 = open(slurm_in, "w")
        fout1.write(sel_in.format(im, sbid, fld, askap_version, tt1, txt, weightim))
        fout1.close()
        fout2.write(sel_slurm.format(parset))
        fout2.close()
        # i += 1
        # print('doing ', fld, sbid)
    else:
        print("{} not found".format(str(im)))


askap_version = os.environ['ASKAPSOFT_RELEASE']

epoch = 0
survey = ASKAP_Survey_factory(epoch=epoch, verbose=False)
root = survey.get_data_root()

tab = survey.f_table

for irow, r in enumerate(tab):
    sbid = r['SBID']
    fld = r['FIELD_NAME']
    lab = "_{:d}-{}".format(sbid, fld)
    slurm_name = "selavy_fluxcorr_mosaic{}.slurm".format(lab)
    in_name = "selavy_in_fluxcorr_mosaic{}.in".format(lab)
    gen_selavy(survey, irow, slurm_name, in_name)

print("outputs written to current directory {}".format(os.getcwd()))
