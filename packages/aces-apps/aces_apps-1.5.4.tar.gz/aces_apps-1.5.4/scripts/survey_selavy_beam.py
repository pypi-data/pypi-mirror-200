#!/usr/bin/env python
"""Generate parsets and sbatch scripts to run selavy on RACS single beam images.

Output images are not written to conserve disk space.

The selavy job for each beam in the given field will be run in the same job allocation
in serial. If the field is complex, you may need to increase the time limit. Experience
suggests that the source finding for most RACS beams should complete within 10 minutes.

Example usage:
    survey_selavy_beam.py --submit selavy.in.template path/to/field_dir

The above will create a selavy parset and sbatch script for each beam image within
path/to/field_dir. The beam image filenames are assumed to follow typical pipeline naming
convention i.e. image.i.SBXXXX.cont.RACS_test4_1.05_XXXXXXXX.beamXX.taylor.X.restored.fits.
The parset_template is a selavy parset which must contain the following string format
placeholders:
    {image} -- the path to the single beam image.
    {image_base} -- the basename of the single beam image. Useful for naming outputs.
    {sbid} -- the observation SBID.

Outputs will be written to fields/<field_name> in the current working directory.
"""
__author__ = "Andrew O'Brien"
__email__ = "andrew.obrien@csiro.au>"

import sys
import re
import argparse
import textwrap
import subprocess
from pathlib import Path


def arg_init():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("parset_template", help="Selavy parset template file. Must contain format placeholders {image}, "
                                                "{image_base} and {sbid}.")
    parser.add_argument("field_dir", type=Path, help="Directory containing input FITS images for the same RACS field.")
    parser.add_argument("-s", "--submit", action="store_true", help="Submit the job to the cluster.")
    parser.add_argument("--clusters", default="galaxy", help="Cluster to run the job. Default: galaxy.")
    parser.add_argument("--account", default="askap", help="Account to run the job under. Default: askap.")
    parser.add_argument("-t", "--time", default="08:00:00", help="Time limit for the job allocation. Default 08:00:00.")
    parser.add_argument('-v', '--verbose', action='store_true')
    return parser


def main():
    args = arg_init().parse_args()

    verbose = args.verbose
    if verbose:
        print(args)


    # read the templates
    with open(args.parset_template) as parset_template_fd:
        print("reading parset template file: {}".format(args.parset_template))
        parset_template = parset_template_fd.read()

    images = args.field_dir.glob("image.i.*.taylor.0.restored.fits")
    field = args.field_dir.name

    # make field dir
    output_field_dir = Path("FLD_IMAGES/beam_selavy").joinpath(field)
    if not output_field_dir.exists():
        output_field_dir.mkdir(parents=True)

    # format the sbatch script header
    script_header = """
        #!/bin/bash -l
        #SBATCH --partition=workq
        #SBATCH --clusters={clusters}
        #SBATCH --account={account}
        #SBATCH --export=NONE
        #SBATCH --ntasks=19
        #SBATCH --ntasks-per-node=20
        #SBATCH --time={time}
        #SBATCH --job-name={job_name}
    
        module load slurm
        module unload python
        module load python
        module use /group/askap/modulefiles
        module load askapdata
        module unload askapsoft
        module load askapsoft/0.24.4
        module unload askappipeline
        module load askappipeline/0.24.4
    """.format(
        clusters=args.clusters,
        account=args.account,
        time=args.time,
        job_name="selavy_{field}".format(field=field)
    )
    script = textwrap.dedent(script_header)[1:]  # remove intentation and first blank line

    for image in images:
        print("image.stem : {}".format(image.stem))
        mat = re.match(r"image.i.SB(\d{4}).cont.RACS_test4_1.05_.+?.beam(\d{2}).taylor.\d.restored",
                              image.stem)
        if mat:
            sbid, beam = mat.groups()
            image_base = image.stem

            # write parset
            parset = parset_template.format(image=image.resolve(), image_base=image_base, sbid=sbid)
            parset_file = output_field_dir / Path("selavy_{}.in".format(image_base))
            with parset_file.open('w') as parset_file_fd:
                parset_file_fd.write(str(parset))

            srun_cmd = "srun --export=ALL --ntasks=19 --ntasks-per-node=20 selavy -c {parset}" \
                       " >> selavy_${{SLURM_JOB_ID}}.log".format(parset=parset_file.name)
            script += srun_cmd + "\n"

    script_file = output_field_dir / Path("selavy_{}.sbatch".format(field))
    with script_file.open('w') as script_file_fd:
        script_file_fd.write(str(script))

    # submit job
    if args.submit:
        subprocess.Popen("sbatch {}".format(script_file.name), shell=True, cwd=str(output_field_dir))


if __name__ == "__main__":
    sys.exit(main())

