#!/bin/bash
#$ -cwd
#$ -j y
#$ -S /bin/bash

# Activate conda environment
source ~/anaconda3/etc/profile.d/conda.sh
conda activate seecs-ai-receptionist

# Start frontend (GUI)
cd GUI
yarn install
yarn dev
