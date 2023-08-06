#!/usr/bin/env python
import argparse as ap
import glob
import os
import re
import subprocess
import sys
import time
from pathlib import Path

import aces.racs.survey_utils as sut
import numpy as np
from aces import racs
from aces.racs.racs_survey import ASKAP_Survey_factory

from astropy.io import fits
from astropy.time import Time

# from askap.parset import ParameterSet, extract

NOFORMAT = '{noformat}\n'

debug = False

queue_max = 7000
queue_per_field = 60
queue_extra = 50
queue_sleep = 200

explanation = """
This is a post-processing pipeline for RACS
--------------------------------------------------------------

"""
# slurm scripts
copy_script = """#!/bin/bash
#SBATCH --export=NONE
#SBATCH --output=/group/askap/mcc381/logs/%j-copy.out
#SBATCH --error=/group/askap/mcc381/logs/%j-copy.err
#SBATCH --account=askap
#SBATCH --clusters=galaxy
#SBATCH --mail-user=david.mcconnell@csiro.au
#SBATCH --mail-type=FAIL
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --job-name=copy
#SBATCH --partition=workq
#SBATCH --time=00:05:00

source /home/mcc381/racs_init.sh

# Expects: pre-sh, csb, field
pre_sh="{0}"
csb="{1:d}"
field="{2}"

origin="/group/askap/chale/RACS/Common-Beam-Images/"
wildcard="*RACS_tes*cres.fits"
destdir=/askapbuffer/scott/mcc381/RACS/$csb/

$pre_sh
echo $origin$wildcard/$field to $destdir

cp --preserve=timestamps $origin$csb/$field/$wildcard $destdir$field

"""

fcor_script = """#!/bin/bash -l
#SBATCH --cluster=galaxy
#SBATCH --partition=workq
#SBATCH --account=askap
#SBATCH --mail-user=david.mcconnell@csiro.au
#SBATCH --mail-type=FAIL
#SBATCH --time=00:28:00
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1
#SBATCH --job-name=racsfluxcorrt
#SBATCH --export=NONE
#SBATCH --output=racs_flux_corr.out
source /home/mcc381/racs_init.sh

# Expects pre_sh, working_dir, file_name
pre_sh="{0}"
wd="{1}"
filename="{2}"

$pre_sh

cd $wd
echo $PWD

srun --export=ALL racs_flux_corr.py -c $RACS/fcorr.taylor.0.20200623_1441.fits -l $filename > $RACS/racs_flux_corr_${3}.out
"""

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
#SBATCH --time=02:00:00
#SBATCH --nodes=2
#SBATCH --job-name=selavy
#SBATCH --no-requeue
#SBATCH --export=NONE
#SBATCH --mail-user=david.mcconnell@csiro.au
#SBATCH --mail-type=FAIL
#SBATCH --account=askap
#SBATCH -M galaxy
#SBATCH -p workq

source /home/mcc381/racs_init.sh

module load casa

{0}
cd $RACS/scripts/tmp
srun --export=ALL --ntasks=19 --ntasks-per-node=10 selavy -c {1} > $RACS/selavy_${2}.out

"""

askap_version = os.environ['ASKAPSOFT_RELEASE']

scripts = os.environ['RACS'] + '/scripts/tmp'


def arg_init():
    code_path = os.path.dirname(os.path.abspath(racs.__file__))
    print('Code path = ', code_path)
    parser = ap.ArgumentParser(prog='racs_post', formatter_class=ap.RawDescriptionHelpFormatter,
                               description='Launch various post-pipeline jobs',
                               epilog='See -x for more explanation')
    # noinspection PyTypeChecker
    parser.add_argument('cal_sbid', default=None, type=int, help='CAL_SBID of RACS calibrator to use; no default')
    parser.add_argument('-s', '--sbid', default=-1, type=int, help="SBID to use'")
    parser.add_argument('-f', '--field', default=None, help="Process ONLY this field")
    parser.add_argument('-a', '--account', default='askap', help="Account GALAXY will use; default=askap")
    parser.add_argument('-c', '--census', action='store_true', help="CHeck integrity of data products")
    parser.add_argument('-j', '--job-select', default='123', help="Select jobs (1 cp; 2 fcor; 3 selavy")
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-x', '--explain', action='store_true', help="give an expanded explanation")
    return parser


def t_string(db_time):
    time_val = Time(db_time / 3600.0 / 24.0, format='mjd', scale='utc')
    time_val.format = 'iso'
    return "{}".format(time_val)


def submit(batch, dep):
    if dep != '':
        dep = '-d afterok:{}'.format(dep)
        # dep = '-d afterok:{} --kill-on-invalid-dep=yes '.format(dep)
    cmd = "sbatch {} {}".format(dep, batch)
    print("> {}".format(cmd))
    if debug:
        return '99'
    else:
        response = subprocess.getoutput(cmd)
        jobid = re.findall('[0-9]+', response)[0]
        return jobid


def launch(slurm_script, seq, pre_sh, scr_dir, args, dep=''):
    """

    :param slurm_script: Blank script to be completed before submission
    :param seq: A unique tag (could be sequence number) do distinguish different slurm scripts
    :param pre_sh: Script to be run by slurm file before main task
    :param scr_dir: Directiotry to write slurm scriptt
    :param args: Arguments for script
    :param dep: Dependence for sbatch - a jobid of earlier job.
    :return:
    """
    script = slurm_script.format(pre_sh, *args)
    code = re.findall('job-name=[a-z]+',slurm_script)[0][9:]
    batch = '{}/{}_script_{}.slurm'.format(scr_dir, code, seq)
    slurm = open(batch, 'w')
    slurm.write(script)
    slurm.close()

    jobid = submit(batch, dep)

    return jobid


def gen_selavy(survey, db_row, pre_sh, scr_dir):
    r = db_row
    r_inx = r['INDEX']
    im = sut.get_product_name(survey, r_inx, 'mosaic_cres_fcor')

    sbid = r['SBID']
    fld = r['FIELD_NAME']
    tt1 = sut.get_product_name(survey, r_inx, 'mosaic_cres_fcor_tt1')
    txt = str(im).replace('fits', 'txt')
    txt = txt.replace('RACS_', 'RACS_test4_1.05_')
    txtp = Path(txt)
    # print(fld, sbid)
    lab = "{:d}-{}".format(sbid, fld)
    if txtp.exists():
        print('Selavy output already exists {}'.format(txtp))

    weightim = str(sut.get_product_name(survey, r_inx, 'weights_cres_fcor_tt0'))
    parset = "{}/selavy_{}.in".format(scr_dir, lab)
    slurm_in = "{}/selavy_{}.slurm".format(scr_dir, lab)
    fout1 = open(parset, "w")
    fout2 = open(slurm_in, "w")
    fout1.write(sel_in.format(im, sbid, fld, askap_version, tt1, txt, weightim))
    fout1.close()
    fout2.write(sel_slurm.format(pre_sh, parset, '{SLURM_JOB_ID}'))
    fout2.close()
    ret = slurm_in
    # i += 1
    # print('doing ', fld, sbid)
    return ret


def census(survey, cal_sbid, sbid, verbose=False):
        if verbose:
            print("census: csb = {:d}".format(cal_sbid))
        cens = get_census(cal_sbid, sbid, verbose)
        check_seq(survey, cal_sbid, sbid, cens, verbose=verbose)


def get_census(cal_sbid, sbid=-1, verbose=False):
    cwd = os.getcwd()
    csb_dir = "/askapbuffer/scott/mcc381/RACS/{}".format(cal_sbid)
    os.chdir(csb_dir)
    print(csb_dir)
    if sbid > 0:
        sbs = "SB{:d}*".format(sbid)
    else:
        sbs = "SB*"
    fil1 = glob.glob("{}/RACS_???????A/image.i*{}0.restored.cres.fcor.fits".format(csb_dir, sbs))
    fil2 = glob.glob("{}/RACS_???????A/image.i*{}0.restored.fcor.fits".format(csb_dir, sbs))
    fil3 = glob.glob("{}/RACS_???????A/image.i*{}0.restored.fcor.iqr.fits".format(csb_dir, sbs))
    fil4 = glob.glob("{}/RACS_???????A/*{}.cres.fcor.components.xml".format(csb_dir, sbs))
    fil5 = glob.glob("{}/valid*.fcor/*.png".format(csb_dir))

    files = fil1 + fil2 + fil3 + fil4 + fil5
    if verbose:
        print("cres.fcor  {:d}".format(len(fil1)))
        print("ored.fcor  {:d}".format(len(fil2)))
        print("      iqr  {:d}".format(len(fil3)))
        print("      xml  {:d}".format(len(fil4)))
        print("valid.png  {:d}".format(len(fil5)))
    print(fil5[:3])
    ret = {}
    for f in files:
        try:
            t = os.path.getmtime(f)
        except:
            t = 0.0
        # print(t, f)
        field = f.split('/')[6]
        if field.startswith('valid'):
            field = field.split('.')[4]
        print('field   ', field)
        if field in ret:
            ret[field].append((f, t))
        else:
            ret[field] = [(f, t)]


    os.chdir(cwd)
    return ret


def check_seq(survey, csb, sbid, file_items, verbose=False):
    # os.environ['SURVEY'] = '/Users/mcc381/askap/ASKAP_surveys/survey'
    aks = survey

    ta = aks.f_table
    mk = (ta['CAL_SBID'] == csb) & (ta['SELECT'] == 1)
    if sbid > 0:
        mk = mk & (ta['SBID'] == sbid)
    tab = ta[mk]
    flds = list(tab['FIELD_NAME'])
    targets = ['ed.fcor.fits', 'cres.fcor.fits', 'fcor.iqr.fits','cres.fcor.components.xml', 'valid.png']
    ntyp = len(targets)
    do_print = False
    for i, f in enumerate(flds):
        if f not in file_items:
            print("No files found for {}".format(f))
        else:
            files = [a[0] for a in file_items[f]]

            jtimes = [a[1] + 40587.0 * 86400. for a in file_items[f]]
            time0 = tab[i]['MOSAIC_TIME']
            index = tab[i]['INDEX']
            bo = np.array([a in b for b in files for a in targets])
            wh = np.where(bo == True)[0] % ntyp
            if len(files) == ntyp:
                if min(jtimes) < time0:
                    print('  {:d} {}({:d}) mosaic post-dates derivatives'.format(index, f, sbid))
                    do_print = True
                if jtimes[wh[0]] > jtimes[wh[2]]:
                    print('  {:d} {}({:d})    iqr pre-dates .fcor'.format(index, f, sbid))
                    do_print = True
                if jtimes[wh[3]] < jtimes[wh[1]]:
                    print('  {:d} {}({:d}) selavy pre-dates .fcor'.format(index, f, sbid))
                    do_print = True
                if jtimes[wh[4]] < jtimes[wh[2]]:
                    print('  {:d} {}({:d}) validation pre-dates .iqr'.format(index, f, sbid))
                    do_print = True
                if do_print:
                    td = t_string(time0)
                    print("{:.1f} {}  {:d} {:d}".format(time0, td, sbid, index))
                    for kk in range(ntyp):
                        k = wh[kk]
                        t = jtimes[k]
                        td = t_string(t)
                        print("{:.1f} {}  {}".format(t, td, files[k]))
                    print(' ')
                    do_print = False
            else:
                print("{:d}  {:d} {}  missing some file : n = {:d}".format(index, sbid, f, len(jtimes)))
                allf = ','.join(files)
                missed = [a in allf for a in targets]
                for t, m in zip(targets, missed):
                    if not m:
                        print("   Missing {}".format(t))
                if verbose:
                    for f, t in zip(files, jtimes):
                        td = t_string(t)
                        print(t, td, f, sbid)


def check_fits(fits_file_name):
    fits_file= fits.open(fits_file_name)
    fits_header = fits_file[0].header
    for k in fits_header.keys():
        if k == 'NAXIS':
            val = fits_header[k]
            if val != 4:
                print("NAXIS = {:d}  in {}".format(val, fits_file_name))


def check_lk(survey, csb, sb=-1, verbose=False):
    ta = survey.f_table
    root = survey.get_data_root()
    mk = ta['SELECT'] == 1
    sbs = [sb]
    if sb > 0:
        mk = mk & (ta['SBID'] == sb) & (ta['CAL_SBID'] == csb)
    else:
        mk = mk & (ta['CAL_SBID'] == csb)
    tab = ta[mk]
    if len(tab) == 0:
        print("Bad  CSB/SBID? CSB={:d} SB={:d}".format(csb,sb))
        return 1
    else:
        if sb < 0:
            sbs = sorted(list(set(tab['SBID'])))

    csb = tab['CAL_SBID'][0]
    for sb in sbs:
        mks = tab['SBID'] == sb
        tabs = tab[mks]
        flds = sorted(list(tabs['FIELD_NAME']))
        if verbose:
            print("cal_sbid = {:d}".format(csb))
            print("sbid     = {:d}".format(sb))
            print("flds[0   = {}".format(flds[0]))

        rm_text = []
        start_txt = []
        for f in flds:
            f = f.replace('RACS_','RACS_test4_1.05_')
            lk_chk = '{}/{}/{}/Checkfiles/LEAKAGE_APPLIED_F??_B??'.format(root, csb, f)
            ch_f = glob.glob(lk_chk)
            ch_beams = [int(re.findall('_B[0-9]{2}', a)[0][2:]) for a in ch_f]
            lk_ms = '{}/{}/{}/scienceData_*.beam??_averaged_cal.leakage.ms'.format(root, csb, f)
            ms_f = glob.glob(lk_ms)
            ms_beams = [int(re.findall('\.beam[0-9]{2}', a)[0][5:]) for a in ms_f]
            if verbose:
                print("{}  {:2d} {:2d}".format(f, len(ch_f), len(ms_f)))

            dif = sorted(list(set(ch_beams).difference(set(ms_beams))))
            missing = sorted(list(set(range(36)).difference(set(ms_beams))))
            if len(missing) > 0:
                print("  Missing {}".format(','.join(["{:d}".format(a) for a in missing])))
                for ib in missing:
                    rm_text.append("rm -rf {}/split_chan/beam-{:02d}/*".format(f, ib))
                if '/' in f:
                    fld = f.split('/')[-1]
                else:
                    fld = f
                start_txt.append('\nstart_pipeline.py {:d} {:d} -f {} -p racs_pipeline_app_leakage.parset -s -i'.format(csb, sb, fld))

            if len(dif) > 0:
                print("  Diff    {}".format(','.join(["{:d}".format(a) for a in dif])))

        if len(rm_text) > 0:
            file_name = scripts+'/rm.SB{:d}.sh'.format(sb)
            fout = open(file_name, 'w')
            for t in rm_text:
                fout.write(t+'\n')
            fout.close()
            print('rm commands written to {}'.format(file_name))
        else:
            if sb > 0:
                print("All leakage ms files present for SB {:d}.".format(sb))
            else:
                print("All leakage ms files present for CSB {:d}.".format(csb))

        if len(start_txt) > 0:
            file_name = scripts+'/start.SB{:d}.sh'.format(sb)
            fout = open(file_name, 'w')
            for t in start_txt:
                fout.write(t+'\n')
            fout.close()
            print('start_racs commands written to {}'.format(file_name))


def run_postpipe(survey, csb, sbid, field, flags):
    scripts = os.environ['RACS']+'/scripts/tmp'

    ta = survey.f_table
    mk = (ta['CAL_SBID'] == csb) & (ta['SELECT'] == 1)
    if sbid > 0:
        mk = mk & (ta['SBID'] == sbid)
    tab = ta[mk]
    if len(tab) == 0:
        print("Incompatible CSB={:d} and SB={:d}".format(csb, sbid))
        return 1

    flds = list(tab['FIELD_NAME'])
    if field is not None:
        if field in flds:
            inx = flds.index(field)
            rows = [tab[inx]]
        else:
            print("Field {} not found".format(field))
            return 1
    else:
        rows = tab

    for i, row in enumerate(rows):
        r_inx = row['INDEX']
        script_date = time.strftime("%Y%m%d-%H%M%S")
        seq = "{}-{:03d}".format(script_date, i)
        field = row['FIELD_NAME']
        raw_field = field.replace('RACS_', 'RACS_test4_1.05_')

        # Do copy from chale/RACS/Common...
        cp_job = ''
        if flags[0]:
            pre_sh = "source {}/null.sh".format(scripts)
            cp_args = [csb, raw_field]
            cp_job = launch(copy_script, seq, pre_sh, scripts, cp_args)
            print("cp job num = {}".format(cp_job))

        # Do racs_fluxcorr
        fcor_job = ''
        if flags[1]:
            pre_sh = "source {}/null.sh".format(scripts)
            fil = sut.get_product_name(survey, r_inx, which='mosaic_cres_fcor')
            cres_name = fil.name.replace('.fcor','').replace('RACS_','RACS_test4_1.05_')
            fc_args = ["$RACS/{}/{}/".format(csb, raw_field), cres_name, '{SLURM_JOB_ID}']
            fcor_job = launch(fcor_script, seq, pre_sh, scripts, fc_args, cp_job)
            print("fcor job num = {}".format(fcor_job))

        # Do selavy
        sela_job = ''
        if flags[2]:
            pre_sh = "python {}/symlink.py {:d}".format(scripts, csb)
            batch = gen_selavy(survey, row, pre_sh, scripts)
            sela_job = submit(batch, fcor_job)
            print("selavy job num = {}".format(sela_job))


def main():

    survey = ASKAP_Survey_factory()

    args = arg_init().parse_args()

    verbose = args.verbose
    if verbose:
        print(args)

    csb = args.cal_sbid
    sbid = args.sbid
    field = args.field
    sflags = args.job_select

    if args.census:
        print('Checking mode')
        print('Checking images and selavy files:')
        census(survey, csb, sbid, verbose)
        print('\nChecking leakage measurement sets')
        check_lk(survey, csb, sbid, verbose)
    else:
        flags = ["{:d}".format(i) in sflags for i in [1, 2, 3]]
        run_postpipe(survey, csb, sbid, field, flags)


if __name__ == "__main__":
    sys.exit(main())
