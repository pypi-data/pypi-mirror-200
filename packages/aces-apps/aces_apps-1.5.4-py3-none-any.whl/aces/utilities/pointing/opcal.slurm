#!/bin/bash -l
#SBATCH --time=60
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1
#SBATCH --job-name=opcal
#SBATCH --no-requeue
#SBATCH --export=NONE
#SBATCH --account=askaprt

export OMP_NUM_THREADS=1

msin=opcal_${SLURM_JOB_ID}.in
ms=$1

cat > $msin <<EOF

dataset=$ms
Feed=0
maxtime = 3600.
#maxtime = 300.
#maxtime = 120.

sources.names = [src1]

sources.src1.components = [src1]
sources.src1.flux.i = 100
sources.src1.direction.ra = 0
sources.src1.direction.dec = 0

# Wasim's model from ACES-200
#sources.src1.components = [src1a,src1b]
sources.src1a.flux.i        = 1356.65
sources.src1a.direction.ra  = 1.15822e-05
sources.src1a.direction.dec = 8.36914e-05
sources.src1a.shape.bmaj  = 0.000127131
sources.src1a.shape.bmin  = 0.000100861
sources.src1a.shape.bpa   = 0.196966
sources.src1b.flux.i        = 1093.69
sources.src1b.direction.ra  = -0.000128048
sources.src1b.direction.dec = 0.000157099
sources.src1b.shape.bmaj  = 0.000112852
sources.src1b.shape.bmin  = 8.59426e-05
sources.src1b.shape.bpa   = -1.20895

gridder = SphFunc
niter = 45
refant = 0
nant = 28

EOF

#IFS='.'
#fields=( $ms )
#ofln="opcal_${fields[0]}.log"
#unset IFS

ofln="opcal.log"
srun --export=ALL opcal -c $msin > $ofln
