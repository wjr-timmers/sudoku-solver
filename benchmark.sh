#!/bin/bash
#SBATCH --job-name=sudoku_benchmark
#SBATCH --output=logs/bench_%A_%a.out
#SBATCH --error=logs/bench_%A_%a.err
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=64
#SBATCH --time=01:00:00

module load 2025
module load Python/3.13.1-GCCcore-14.2.0

cp -r $SLURM_SUBMIT_DIR/* $TMPDIR/
cd $TMPDIR

CHUNK_SIZE=140625 # Is exactly 9 million if chunk size is 140625 , approx 1 hour of total calc. 
NUM_PUZZLES=$(( CHUNK_SIZE * SLURM_CPUS_PER_TASK ))

echo "Starting benchmark: Total $NUM_PUZZLES puzzles using $SLURM_CPUS_PER_TASK workers."

python3 benchmark.py --num_puzzles $NUM_PUZZLES --chunk_size $CHUNK_SIZE --num_workers $SLURM_CPUS_PER_TASK