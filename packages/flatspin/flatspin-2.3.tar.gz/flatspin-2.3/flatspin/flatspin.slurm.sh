#!/bin/bash
#SBATCH --job-name=flatspin
#SBATCH --partition=GPUQ
#SBATCH --time=72:00:00
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=1
#SBATCH --mem=16G
#SBATCH --output={job_script_dir}/{job_script_name}.slurm-%j.log
#SBATCH --account=share-ie-idi

set -e

module load GCC/10.2.0 CUDA/11.1.1-GCC-10.2.0
module load Python/3.8.6-GCCcore-10.2.0

set -x

env

# SLURM will set CUDA_VISIBLE_DEVICES for us which automatically selects the allocated GPU
# OpenCL will always see the allocated GPU as device 0
flatspin-run -r worker -o {basepath} --worker-id ${{SLURM_ARRAY_TASK_ID}} --num-workers $((SLURM_ARRAY_TASK_MAX+1))

