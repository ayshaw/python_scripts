#!/bin/bash

#SBATCH -n 1                    # Number of cores
#SBATCH -N 1                    # Ensure that all cores are on one machine
#SBATCH -t 0-12:00              # Runtime in D-HH:MM
#SBATCH -p huce_intel           # Partition to submit to
#SBATCH --mem=16000            # Memory pool for all cores (see also --mem-per-cpu)
#SBATCH -o benchmark_rst_%j.out           # File to which STDOUT will be written
#SBATCH -e benchmark_rst_%j.err           # File to which STDERR will be written
#SBATCH --mail-type=END         # Type of email notification- BEGIN,END,FAIL,ALL
#SBATCH --mail-user=ayshaw@g.harvard.edu      # Email to which notifications will be sent
module load python/3.6.0-fasrc01
source activate ody

python ./132_lvl_CO2_rst.py
