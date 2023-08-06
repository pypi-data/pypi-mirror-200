#!/bin/bash -l
#SBATCH -n 1
#SBATCH -N 1
#SBATCH --time=120
#SBATCH --job-name=msavg
#SBATCH --no-requeue
#SBATCH --export=NONE
#SBATCH --account=askaprt

# Runs mssplit to do 54 channel averaging (resulting in 1 MHz resolution)

msin=mssplit_${SLURM_JOB_ID}.in
ms=$(ls -1d /astro/askaprt/askapops/askap-scheduling-blocks/$1/2*.ms)
echo "Processing $ms"

cat > $msin <<EOF
# Input measurement set
vis = $ms

# Output measurement set
outputvis = ChAvg.ms

# The channel range to split out into its own measurement set
# Can be either a single integer (e.g. 1) or a range (e.g. 1-300). The range
# is inclusive of both the start and end, indexing is one-based.
# Default: <no default>

#channel     = 1-16416
channel     = 1-15552
#channel     = 1-12960
#channel     = 1-10368
#channel     = 1-7776
#channel     = 1-2592

# Defines the number of channels to average to form the one output channel
# Default: 1
width       = 54

# Set a larger bucketsize
stman.bucketsize  = 1048576
# Make the tile size 54 channels, as that is what we will average over
stman.tilenchan   = 54

EOF

srun --export=ALL mssplit -c $msin

