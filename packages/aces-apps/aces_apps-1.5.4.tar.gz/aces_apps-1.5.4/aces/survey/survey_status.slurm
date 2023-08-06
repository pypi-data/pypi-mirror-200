#!/bin/bash -l
#SBATCH --cluster=galaxy
#SBATCH --partition=workq
#SBATCH --time=00:05:00
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1
#SBATCH --job-name=surveystatus
#SBATCH --export=NONE

# Expects $1 $2 :  epoch num
EPOCH=$1
NUM=$2

module unload numpy
conda activate aces

echo $PWD

srun --export=ALL survey_status.py -i MBSCP -e $EPOCH -n $NUM 
srun --export=ALL survey_validation.py -f -v -e $EPOCH -n $NUM

