#!/usr/bin/env python
from __future__ import print_function
import subprocess
import os
import errno
import pwd
import shutil
import sys
import re
import glob
import argparse as ap
import askap.parset.parset as ps
# noinspection PyPackageRequirements
from aces import sefd
# noinspection PyPackageRequirements
from aces.askapdata.schedblock import SchedulingBlock
from numpy import pi
# noinspection PyPackageRequirements
from aces.obsplan.config import ACESConfig
from askap.jira import Jira

NOFORMAT = '{noformat}\n'
ARCHIVE = '/astro/askaprt/askapops/askap-scheduling-blocks/'


def mkdir_p(path):
    # from https://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python
    try:
        os.makedirs(path)
    except OSError as exc:  # Python > 2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def slurm_array_str(the_list):
    # Return a string giving the input list of integers in condensed form, with contiguous
    # sequences of numbers i, i+1, i+2, ... j as i-j.
    if len(the_list) == 0:
        return ""
    # the_list.sort()
    ret = []
    k = -1
    i1 = 0
    for i, j in enumerate(the_list):
        if k < 0:
            i1 = j
            k = j
        elif j == k + 1:
            k = j
        else:
            if k == i1:
                ret.append("{:d}".format(i1))
            else:
                ret.append("{:d}-{:d}".format(i1, k))
            i1 = j
            k = j
    if k == i1:
        ret.append("{:d}".format(i1))
    else:
        ret.append("{:d}-{:d}".format(i1, k))
    return ','.join(ret)


def arg_init():
    parser = ap.ArgumentParser(prog='start_SEFD', formatter_class=ap.RawDescriptionHelpFormatter,
                               description='Launch SEFD processing',
                               epilog='See -x for more explanation')
    # noinspection PyTypeChecker
    parser.add_argument('sbid', nargs="+", type=int, help="SBID")
    parser.add_argument('-r', '--realtime', action='store_true', help="run with high priority under askaprt group")
    parser.add_argument('-p', '--parset', default=None, help="Parset for additional inputs")
    parser.add_argument('-a', '--archive', default=ARCHIVE, help="Directory containing ms data")
    parser.add_argument('-d', '--workdir', default='.', help='working directory')
    parser.add_argument('-n', '--noreplace', action='store_true', help="Do not replace existing hdf5 outputs")
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-x', '--explain', action='store_true', help="give an expanded explanation")
    # noinspection PyTypeChecker
    parser.add_argument('-j', '--jira', metavar='ISSUE', type=str, help='post jira report to ISSUE')
    return parser


def get_footprint(sb):
    aces_cfg = ACESConfig()
    fp_factory = aces_cfg.footprint_factory
    name = sb.get_footprint_name()
    pitch = sb.get_footprint_pitch()
    # Catch the single mset_inx footprint, which may have zero pitch, disallowed by the footprint factory.
    if pitch == 0.0:
        pitch = 1.0
    rotation = sb.get_footprint_rotation()
    fp = fp_factory.make_footprint('ak:' + name, pitch * pi / 180, rotation * pi / 180)
    return fp


def build_cmd(func, sb, array_set, depend_jobid=None, group='askap', jira=None, out_path='.'):
    if jira:
        jiraopt = '-j {} '.format(jira.issue)
    else:
        jiraopt = ''

    array_str = slurm_array_str(array_set)

    # fp = get_footprint(sb)
    # n_beams = 0
    # if parset is not None:
    #     n_beams = parset.get_value('n_beams', default=0)
    # if n_beams > 0:
    #     # override number of beams from parset
    #     array_str = "0-{0:d}".format(n_beams - 1)
    # elif fp.n_beams > 1:
    #     # number of beams from footprint
    #     array_str = "0-{0:d}".format(fp.n_beams - 1)
    # else:
    #     array_str = "0"
    cmd = ''

    if func == 'proc':
        cmd = "sbatch -o sefd.log -e sefd.log --open-mode append --job-name=sefdProc{0:d} " \
              "-D {3} -A {1} --array={2} sefdProcessing.sh {0:d} {3}".format(sb.id, group, array_str, out_path)
    elif func == 'merge':
        print(sb.id, group, depend_jobid, out_path)
        cmd = 'sbatch -o sefd.log -e sefd.log --open-mode append --job-name=sefdMerge{0:d} ' \
              '-D {3} -A {1} --depend=afterany:{2:d} sefdmerge.sh {0:d}'.format(sb.id, group, depend_jobid, out_path)
    elif func == 'summ':
        cmd = 'sbatch -o sefd.log -e sefd.log --open-mode append --job-name=sefdSumm{0:d} ' \
              '-D {4} -A {1} --depend=afterany:{2:d} sefdsummary.sh {3}{0:d}'.format(sb.id, group, depend_jobid,
                                                                                     jiraopt, out_path)
    return cmd


def submit_sefd(sb, array_set, group='askap', jira=None, out_path='.'):
    jobnum = -1

    print('\nCommencing SEFD processing for SB{}'.format(sb.id))
    notice = 'Commencing SEFD processing for *SB{}*'.format(sb.id)
    report = ''
    for fnc in ['proc', 'merge', 'summ']:
        cmd = build_cmd(fnc, sb, array_set, jobnum, group, jira, out_path)
        report += 'Submitting job {} with command: {}\n'.format(fnc, cmd)
        status, response = subprocess.getstatusoutput(cmd)
        if status == 0:
            jobnum = int(response.strip().split(' ')[-1])
            report += "{} job is {}\n".format(fnc, jobnum)
        else:
            report += response + '\n'
    print(report)
    if jira:
        jira.add_comment(jira.issue, notice + NOFORMAT + report + NOFORMAT)


def main():
    args = arg_init().parse_args()
    if args.verbose:
        print("ARGS = ", args)
        # sys.exit()
    if args.realtime:
        group = 'askaprt'
    else:
        group = 'askap'

    if args.jira:
        jira = Jira()
        jira.authenticate()
        jira.issue = args.jira
    else:
        jira = None

    parset = args.parset
    parset_name = "SEFD_%d.parset"

    data_dir = args.archive

    # check schedblock ice service is up
    try:
        print('Testing connection to Scheduling Block Service: ,')
        sys.stdout.flush()
        SchedulingBlock(555)
        print('PASSED')
    except Exception as err:
        print('FAILED')
        print('Power or Network to MRO may be down!')
        raise err

    # If an additional inputs parset is given, open it and pre-load the main inputs parset.
    # The inputs in this extra parset will apply to all SBIDs being processed.
    p_extra = ps.ParameterSet()
    if parset:
        if os.path.exists(parset):
            p_extra = ps.ParameterSet(parset)
        else:
            print("Extra input parset {} not found".format(parset))

    for j in args.sbid:
        file_query = (data_dir + '{:d}/*.ms').format(j)
        msets = glob.glob(file_query)
        n_ms = len(msets)
        # hard code this for now. In future allow specification of subset through arguments.
        array_set = [k for k in range(n_ms)]
        print("SBID : {:d}".format(j))
        print(file_query)
        p = ps.ParameterSet()
        for pk in p_extra.keys():
            p[pk] = p_extra[pk]

        sb = SchedulingBlock(j)
        p.sbid = sb.id
        fp = get_footprint(sb)
        p.footprint = fp.to_parset()
        p.footprint.pitch = sb.get_footprint_pitch()
        p.footprint.rotation = sb.get_footprint_rotation()
        out_path = 'SEFD{:d}'.format(sb.id)
        out_path = os.path.join(args.workdir, out_path)
        mkdir_p(out_path)

        code_path = os.path.dirname(os.path.abspath(sefd.__file__))
        defaults_file_name = 'SEFD_defaults.parset'
        defaults_fullfile = os.path.join(code_path, 'SEFD_defaults.parset')

        if not os.path.isfile(os.path.join(out_path, defaults_file_name)):
            print('Copying SEFD_defaults.parset to working directory')
            shutil.copy(defaults_fullfile, out_path)

        p.to_file(os.path.join(out_path, parset_name % sb.id))
        if args.noreplace:
            gq = "{}/SEFD_A-{:d}_beam_*.hdf5".format(out_path, j)
            already = glob.glob(gq)
            dont_do = [int(re.findall("[0-9]+", re.findall("[0-9]+\.", f)[0])[0]) for f in already]
            todo = list(set(array_set) - set(dont_do))
            array_set = todo
        submit_sefd(sb, array_set, group, jira, out_path)

    # show the current status with 'squeue'
    user = pwd.getpwuid(os.getuid()).pw_name
    response = subprocess.getoutput("squeue | grep %s" % user)
    notice = 'Current SEFD processing status for user={}:'.format(user)
    print(notice)
    print(response)
    # if jira:
    #     jira.add_comment(jira.issue, notice + '\n' + NOFORMAT + response + NOFORMAT)


if __name__ == "__main__":
    sys.exit(main())
