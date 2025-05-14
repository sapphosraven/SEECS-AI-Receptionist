#!/bin/bash
#$ -cwd
#$ -j y
#$ -S /bin/bash

# Activate conda environment
source ~/anaconda3/etc/profile.d/conda.sh
conda activate seecs-ai-receptionist

# Start backend server
cd GUI/backend
node server.js
