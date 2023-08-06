#!/usr/bin/env python
import sys
import os
import time
import argparse as ap
import subprocess
from pathlib import Path
from askap.parset import ParameterSet, merge

import glob
from aces import survey
from aces.survey.survey_class import ASKAP_Survey_factory

NOFORMAT = '{noformat}\n'

queue_max = 7000
queue_per_field = 60
queue_extra = 50
queue_sleep = 200

explanation = """
This launches the processASKAP pipeline
--------------------------------------------------------------
There are two possibilities:
i) Determine the bandpass calibration tables - use '-b CAL_SBID' without '-i' or '-n' switches.
    start_pipeline.py -b 20148
    start_pipeline.py -b 20148 20435 20892
    
ii) Image one or more fields specified either as '-i SBID' or '-n ROW_NUM' where the survey
    database row number is given. If the '-i' switch is used, also provide the bandpass SBID with '-b'.
    start_pipeline.py -i 20908 -b 20892
    start_pipeline.py -e 1 -n 412

    Inputs for processASKAP.sh are provided by a sequence of sources:
     i) All input variables have default values defined in
          https://www.atnf.csiro.au/computing/software/askapsoft/sdp/docs/current/pipelines/ControlParameters.html
    ii) These can be over-ridden with values passed to processAKSAP in a config file. This script compiles the config
        file from three sources:
        1. One of two parsets held in the aces repository: bandpass_default.parset and image_default.parset.
        2. The chosen defaults parset (depending on the requested operation) can be over-ridden or augmented by values
           in a local parset specified with the '-p' switch (default is pipeline.parset in working directory).
        3. Final additions are made by the script itself; these reflect other command-line arguments.

"""
archives = ['/askapbuffer/payne/askap-scheduling-blocks/',
            '/askapbuffer/scott/askap-scheduling-blocks/']

version = '20210222'


def arg_init():
    code_path = os.path.dirname(os.path.abspath(survey.__file__))
    print('Code path = ', code_path)
    parser = ap.ArgumentParser(prog='start_pipeline', formatter_class=ap.RawDescriptionHelpFormatter,
                               description='Launch the RACS calibration and imaging pipeline',
                               epilog='See -x for more explanation',
                               fromfile_prefix_chars='@')
    # noinspection PyTypeChecker
    # parser.add_argument('cal_sbid', default=None, type=int, help='SBID of calibrator to use; no default')
    # parser.add_argument('fld_sbid', default=None, type=int, help='SBID of observation to image; no default')
    parser.add_argument('-p', '--parset', default='pipeline.parset', type=str,
                        help="Parset for additional parameters for processASKAP.sh")
    parser.add_argument('-i', '--image_sbid', type=int, nargs='*', help='Declare science SBID(s)')
    parser.add_argument('-c', '--bandpass_sbid', type=int, nargs='*', help="Declare CAL SBID(s)")
    parser.add_argument('-f', '--field', default=None, help="Process ONLY this field")
    parser.add_argument('-e', '--epoch', default=0, type=int, help="Survey epoch")
    parser.add_argument('-n', '--numbers', type=int, nargs='*', help="Database row numbers to image")
    parser.add_argument('-b', '--bounds', type=int, metavar=["start", "stop"], nargs=2, help="Row number bounds")
    parser.add_argument('-B', '--beams', default=None, help="Process these beams")
    parser.add_argument('-a', '--account', default='askap', help="Account GALAXY will use; default=askap")
    parser.add_argument('-s', '--submit_job', action='store_true', help="submit job to GALAXY; default=false")
    parser.add_argument('-u', '--update_database', action='store_true',
        help='add a job to update the database after processing')
    parser.add_argument('-d', '--workdir', default=os.getcwd(), help="Current working directory")
    parser.add_argument('-m', '--modulefiles', default=os.path.join(code_path, 'loadaskap'),
                        help="modules required to run processASKAP.sh")
    parser.add_argument('-t', '--metadata', default=None,
                        help="Extra directory containing metadata from mslist")
    parser.add_argument('-o', '--original', action='store_true',
                        help="Select for original-style 'science-dir-inside-caldir'")
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-x', '--explain', action='store_true', help="give an expanded explanation")
    return parser


def check_runfiles_dir(workdir):
    # create directory for the processASKAP.sh run files
    rundir = workdir.joinpath('runfiles')
    if not rundir.exists():
        rundir.mkdir()
    return rundir


def check_sb_path(sb, work_path):
    sb_path = work_path.joinpath("{:d}".format(sb))
    if not sb_path.exists():
        sb_path.mkdir()
    return sb_path


def find_ms_dir(sb):
    # dir_sb = archives[0]
    dir_sb = None
    for ar in archives:
        s = Path(ar).joinpath(str(sb))
        if s.exists():
            ms_files = sorted(s.glob("*.ms"))
            if len(ms_files) > 0:
                dir_sb = ar
    return dir_sb


def check_queue():
    proc = subprocess.Popen(['squeue', '-h'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    tmp = str(proc.stdout.read()).split('\n')
    askap_jobs = [a for a in tmp if 'askap' in a]
    running_jobs = [a for a in askap_jobs if 'nid0' in a]
    num_nodes = [int(a.split()[-2]) for a in running_jobs]
    ret = {'N_total': len(askap_jobs),
           'N_running': len(running_jobs),
           'N_nodes': sum(num_nodes)}
    return ret


def wait_for_space(n_fields=12):
    slurm_max = queue_max
    wait_seconds = queue_sleep
    q_stats = check_queue()
    a = '  '.join(["{}: {}".format(k, v) for k, v in q_stats.items()])
    print(a)
    jobs_needed = n_fields * queue_per_field + queue_extra
    slurm_avail = slurm_max - q_stats['N_total']
    while slurm_avail < jobs_needed:
        print("Queue has {:d}  ({:d} available) Need {:d}   Waiting {:d} seconds".format(q_stats['N_total'],
                                                                                         slurm_avail, jobs_needed,
                                                                                         wait_seconds))
        time.sleep(wait_seconds)
        q_stats = check_queue()
        slurm_avail = slurm_max - q_stats['N_total']
        # a = '   '.join(["{}: {}".format(k, v) for k, v in q_stats.items()])
        # print(a)
    return


def get_final_jobid(joblist):
    lines = [li.strip() for li in open(joblist, 'r').readlines()]
    # for i, li in enumerate(lines):
    #     if "Job to create diagnostic" in li:
    #         break
    jobid = int(lines[-1].split()[0])
    return jobid


def p_grep(things, files):
    ret = None
    for f in files:
        fil = open(f, 'r').read()
        found = True
        for thing in things:
            found = found and (thing in fil)
            # print('thing, found : ', thing, found)
        # print(f, found, (things[0] in fil))
        # print(fil)
        if found:
            ret = f
            break

    return ret


def parset_to_config_file(ps, filename):
    s = ps.__str__()
    sc = s.replace(" = ", "=")
    f = open(filename, 'w')
    f.write(sc + '\n')
    f.close()


def save_config(parset, rundir, sb):
    run_date = time.strftime("%Y%m%d-%H%M%S")
    config_name = str(rundir.joinpath("config_{:d}_{}.parset".format(sb, run_date)))
    parset_to_config_file(parset, config_name)
    return config_name, run_date


def main():
    # start_pipeline launches a number of jobs depending on the number of fields in an SBID
    # BPCAL 110
    # imaging = nfields * 115
    # Cal = nfields * 220
    print("version {}".format(version))

    arg_parser = arg_init()
    args = arg_parser.parse_args()
    if args.explain:
        print(explanation)
        sys.exit()
    if args.verbose:
        print(args)

    code_path = Path(survey.__file__).parent
    work_path = Path(args.workdir)
    # print("work_path = ", str(work_path))
    epoch = args.epoch
    aks = ASKAP_Survey_factory(epoch=epoch)
    data_root = aks.get_data_root()
    # Get selection of data to process
    bandpass_sbid = args.bandpass_sbid
    image_sbid = args.image_sbid
    numbers = args.numbers
    bounds = args.bounds
    if bounds:
        numbers = range(bounds[0], bounds[1] + 1)
    do_bandpass, do_image, nothing, ambiguous = False, False, False, False
    combo = ''.join([str(bool(b))[0] for b in [bandpass_sbid, image_sbid, numbers]])
    # print('combo {}'.format(combo))
    if combo == 'TFF':
        do_bandpass = True
    elif (combo == 'TTF') or (combo == 'FFT'):
        do_image = True
    elif combo == 'FFF':
        nothing = True
    else:
        ambiguous = True

    if nothing:
        print("No input request. Nothing to do.")
        sys.exit()
    elif ambiguous:
        print("Ambigious input: give '-n' OR '-i' and '-b' OR just '-b' for determining bandpass.")
        sys.exit()

    print('modulefiles ', args.modulefiles)
    if os.path.exists(args.modulefiles):
        module_loader = args.modulefiles
        if args.verbose:
            print('  Using ASKAP module files located in : {}'.format(args.modulefiles))
    else:
        print("  ASKAP module load file {} does not exist. Exiting....check input".format(args.modulefiles))
        exit()

    if args.verbose:
        print("")
        print("  Executing Pipeline v.{} with the following : ".format(version))
        print("     working dir: {}".format(args.workdir))
        print("     survey parset: {}/{}".format(args.workdir, args.parset))
        print("     account    : {}".format(args.account))
        print("     submit job : {}".format(args.submit_job))
        print("")

    # ----------------------------- Build the processAKSAP config file (parset) ------------------------------------
    # Inputs for processASKAP.sh are provided by a sequence of sources:
    #  i) All input variables have default values defined in
    #       https://www.atnf.csiro.au/computing/software/askapsoft/sdp/docs/current/pipelines/ControlParameters.html
    # ii) These can be over-ridden with values passed to processAKSAP in a config file. This script compiles the config
    #     file from three sources:
    #     1. One of two parsets held in the aces repository: bandpass_default.parset and image_default.parset.
    #     2. The chosen defaults parset (depending on the requested operation) can be over-ridden or augmented by values
    #        in a local parset specified with the '-p' switch (default is pipeline.parset in working directory).
    #     3. Final additions are made by the script itself; these reflect other command-line arguments.
    #
    # The code below compiles the config file from the three sources listed above.

    # Ensure directory for config file exists
    rundir = check_runfiles_dir(work_path)

    if do_bandpass:
        default_parset = code_path.joinpath('bandpass_default.parset')
    elif do_image:
        default_parset = code_path.joinpath('image_default.parset')

    working_parset = work_path.joinpath(args.parset)

    if working_parset.exists():
        if args.verbose:
            print('  Using initial parset file : {}'.format(working_parset))
    else:
        print("  Local parset {} not found. Exiting...check input".format(working_parset))
        exit()

    ps_def = ParameterSet(str(default_parset))
    ps_wrk = ParameterSet(str(working_parset))
    parset = merge(ps_def, ps_wrk)
    parset.set_value('ACCOUNT', args.account)
    if not args.submit_job:
        parset.set_value('SUBMIT_JOBS', 'false')

    if do_bandpass:
        for sb in bandpass_sbid:
            print("Do bandpass on {:d}".format(sb))
            sb_path = check_sb_path(sb, work_path)
            parset.set_value('SB_1934', sb)
            parset.set_value('DIR_SB', find_ms_dir(sb))
            parset.set_value('DO_CONT_IMAGING', 'false')
            config_name, run_date = save_config(parset, rundir, sb)
            final_job_id = inner_loop(sb_path, config_name, run_date, module_loader)

    if do_image:
        if numbers:
            image_sbid, bandpass_sbid, field_names = [], [], []
            for inx in numbers:
                row = aks.get_row(inx)
                ssb, csb, fnm = row['SBID', 'CAL_SBID', 'FIELD_NAME']
                image_sbid.append(ssb)
                bandpass_sbid.append(csb)
                field_names.append(fnm)
            # Fix for field names in RACS-LOW only
            if epoch == 0:
                field_names = [a.replace('RACS_', 'RACS_test4_1.05_') if 'test4' not in a else a for a in field_names]
            field_names = ','.join(field_names)
            parset.set_value('FIELD_SELECTION_SCIENCE', field_names)

        if len(image_sbid) > 1 and len(bandpass_sbid) == 1:
            bandpass_sbid = [bandpass_sbid[0]] * len(image_sbid)
        for sb, csb in zip(image_sbid, bandpass_sbid):
            print("Image {:d} with cal {:d}".format(sb, csb))
            if args.original:
                sb_path = check_sb_path(csb, work_path)
            else:
                sb_path = check_sb_path(sb, work_path)
            dir_sb = find_ms_dir(sb)
            apply_leakage = parset.get_value('DO_APPLY_LEAKAGE')
            parset.set_value('SB_1934', csb)
            parset.set_value('SB_SCIENCE', sb)
            if dir_sb is None:
                parset.set_value("NUM_CHAN_SCIENCE", 288)
                gtmp_c = "{}/{}/metadata/mslist-20*.txt".format(data_root, csb)
                gtmp_i = "{}/{}/metadata/mslist-20*.txt".format(data_root, sb)
                if args.metadata is not None:
                    gtmp_t = f"{os.path.abspath(args.metadata)}/mslist-20*.txt"
                    print('gtmp_t = ', gtmp_t)
                    files = sorted(glob.glob(gtmp_c) + glob.glob(gtmp_i) + glob.glob(gtmp_t))
                else:
                    files = sorted(glob.glob(gtmp_c) + glob.glob(gtmp_i))

                print('gtmp_c = ', gtmp_c)
                print('files = ', files)
                # processASKAP looks in the mslist file for all the fields for the given sbid,
                # even if only one is requested.
                fields = aks.get_fields(sb)
                if args.field:
                    fields = [args.field]
                # Fix for field names in RACS-LOW only
                if epoch == 0:
                    fields = [a.replace('RACS_', 'RACS_test4_1.05_') if 'test4' not in a else a for a in fields]
                print('fields = ', fields)
                s_file = p_grep(fields, files)
                print('s_file = ', s_file)

                if s_file is None:
                    print("FATAL error - no metadata/mslist file found")
                    exit(1)
                parset.set_value("MS_METADATA", s_file)
            else:
                parset.set_value('DIR_SB', find_ms_dir(sb))
                print('ms_dir : ', find_ms_dir(sb))

            # User-defined calibration table names can be supplied in filenames.csv
            # Default should point towards most recent output from processASKAP.sh
            if "bp_table" in aks.survey_files.lookup.keys():
                bp_tab = aks.survey_files.cal_table_name("bp_table", csb)
            else:
                bp_tab = work_path.joinpath("{0:4}/BPCAL/calparameters.1934_bp.SB{0:d}.tab".format(csb))


            if "bp_leakage_table" in aks.survey_files.lookup.keys():
                lk_tab = aks.survey_files.cal_table_name("bp_leakage_table", csb)
            else:
                lk_tab = work_path.joinpath("{0:4}/BPCAL/calparameters.1934_bpleakage.SB{0:d}.tab".format(csb))

            lk_ok = apply_leakage and lk_tab.exists() or not apply_leakage
            if bp_tab.exists():
                parset.set_value('TABLE_BANDPASS', bp_tab)
                if lk_tab.exists():
                    parset.set_value('TABLE_LEAKAGE', lk_tab)
                parset.set_value('DO_1934_CAL', 'false')
                if args.field:
                    parset.set_value('FIELD_SELECTION_SCIENCE', args.field)
                if args.beams:
                    parset.set_value("BEAMLIST", args.beams)

                config_name, run_date = save_config(parset, rundir, sb)
                final_job_id = inner_loop(sb_path, config_name, run_date, module_loader)
                if final_job_id > 0 and args.update_database:

                    print("Chaining from job {}".format(final_job_id))
                    
                    sbatch_extras = ' --account={} '.format(args.account)
                    sbatch_extras += ' --output={}/survey_status_%j.out '.format(sb_path)

                    # Get user email from parset, or do not set the email if none is provided:
                    if 'EMAIL' in ps_wrk.keys():  # do not use a default - must be specified
                        sbatch_extras += ' --mail-user={} '.format(ps_wrk['EMAIL'])
                        if 'MAIL_TYPE' in ps_wrk.keys():
                            sbatch_extras += ' --mail-type={} '.format(ps_wrk['MAIL_TYPE'])
                        else:
                            sbatch_extras += ' --mail-type=FAIL '

                    ind = aks.select_indices([['SBID', '==', sb]])
                    ind_list = ' '.join(["{:d}".format(i) for i in ind])
                    cmd = 'sbatch -d afterok:' + \
                          str(final_job_id) + ' {} {}/survey_status.slurm {} {}'.format(
                            sbatch_extras, code_path, args.epoch, ind_list
                        )
                    print(cmd)
                    os.system(cmd)
                print("\n-----------    SBID {:d} processing launched ----------\n\n".format(sb))
            else:
                print("BP or LK table {} not found.\nSkipping\n".format(str(bp_tab)))


def inner_loop(sb_path, config_name, run_date, module_loader):
    """

    :type module_loader: object
    """
    survey_version = 0.2

    # ----------------------------- Set working directory ------------------------------------------------------
    start_dir = os.getcwd()

    os.chdir(sb_path)  # move into working SB directory
    cwd = os.getcwd()
    print("Setting wd to {}".format(cwd))

    # ----------------------- RUNNING processASKAP.sh -c askap_run_file -------------------------------------------
    cmd_file = cwd + '/cmds.txt'
    cmds = open(cmd_file, 'w')
    lines = open(module_loader, 'r').readlines()
    for li in lines:
        cmds.write(li.strip() + '\n')

    to_output = ' > processASKAP_{}.out'.format(run_date)
    cmd = 'processASKAP.sh -c ' + config_name + to_output
    cmds.write(cmd + '\n')
    cmds.close()
    print('source {}'.format(cmd_file))
    os.system('source {}'.format(cmd_file))

    # Find the last job in case any chained jobs are required.
    job_list = 'jobList.txt'
    jobid = -1
    if os.path.exists(job_list):
        # once processASKAP.sh finishes a file called joblist is created.
        # locate the jobid of the last job created.
        jobid = get_final_jobid(job_list)
    else:
        print('  No jobList found')

    print("")

    os.chdir(start_dir)
    print("start_pipeline inner loop completed")
    return jobid


if __name__ == "__main__":
    sys.exit(main())
