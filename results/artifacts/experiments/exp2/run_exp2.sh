#!/bin/bash
# Wrapper script for running Experiment 2 (Progressive Layer Activation)

set -e

TRIALS=${TRIALS:-5}
DB_PATH=${DB_PATH:-exp2_results.db}
LOG_FILE=${LOG_FILE:-exp2_execution.log}
OUTPUT_DIR=${OUTPUT_DIR:-results}
SEED=${SEED:-42}

echo "=========================================="
echo "Running Experiment 2: Progressive Layer Activation"
echo "=========================================="
echo "Trials: $TRIALS"
echo "Database: $DB_PATH"
echo "Log file: $LOG_FILE"
echo "Output directory: $OUTPUT_DIR"
echo "Random seed: $SEED"
echo "=========================================="

python3 run_experiments_corrected.py \
    --experiment 2 \
    --trials $TRIALS \
    --db-path $DB_PATH \
    --log-file $LOG_FILE \
    --output-dir $OUTPUT_DIR \
    --seed $SEED \
    --no-confirm
