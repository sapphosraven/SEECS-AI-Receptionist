#!/bin/bash
#$ -cwd
#$ -j y
#$ -S /bin/bash

# Activate conda environment
source ~/anaconda3/etc/profile.d/conda.sh
conda activate seecs-ai-receptionist

# Run LangGraph Adaptive RAG (edit the script name as needed)
cd LLM/RAG-DATA
python langgraph_adaptive_rag_final.py
