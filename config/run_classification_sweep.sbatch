#!/bin/bash

################################################################################################
### sbatch configuration parameters must start with #SBATCH and must precede any other commands.
### To ignore, just add another # - like so: ##SBATCH

### Submit from src/:
### sbatch ../config/run_classification_sweep.sbatch <INPUT_FILE_PATH>
################################################################################################

#SBATCH --partition=main
#SBATCH --time=7-00:00:00
#SBATCH --job-name=classification_sweep
#SBATCH --output=../logs/%A_%a_%x.out
#SBATCH --error=../logs/%A_%a_%x.err
#SBATCH --mail-user=amitner@post.bgu.ac.il
#SBATCH --mail-type=END,FAIL
#SBATCH --mem=58G
#SBATCH --cpus-per-task=8
#SBATCH --array=1-210%21

set -euo pipefail

INPUT_FILE_PATH="${1:-}"

if [[ -z "${INPUT_FILE_PATH}" ]]; then
    echo "ERROR: No input file path provided." >&2
    echo "Usage: sbatch ../config/run_classification_sweep.sbatch <INPUT_FILE_PATH>" >&2
    exit 1
fi

if [[ ! -e "${INPUT_FILE_PATH}" ]]; then
    echo "ERROR: Input path does not exist: ${INPUT_FILE_PATH}" >&2
    exit 1
fi

echo "$(date)"
echo -e "\nSLURM_ARRAY_JOB_ID:\t${SLURM_ARRAY_JOB_ID}"
echo -e "SLURM_ARRAY_TASK_ID:\t${SLURM_ARRAY_TASK_ID}"
echo -e "SLURM_JOB_NODELIST:\t${SLURM_JOB_NODELIST}"
echo -e "Job name:\t\t${SLURM_JOB_NAME}"
echo -e "INPUT_FILE_PATH:\t${INPUT_FILE_PATH}"

IN_NOTEBOOK="classification_sweep.ipynb"
OUT_NOTEBOOK="../logs/${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}_${SLURM_JOB_NAME}.ipynb"

echo "Starting Papermill task ${SLURM_ARRAY_TASK_ID}..."

if ! conda run --no-capture-output -n backbone_env_v2 \
    papermill \
    "${IN_NOTEBOOK}" \
    "${OUT_NOTEBOOK}" \
    -p input_data_path "${INPUT_FILE_PATH}" \
    -p classification_task_id "${SLURM_ARRAY_TASK_ID}"; then

    echo "ERROR: Classification sweep task ${SLURM_ARRAY_TASK_ID} failed." >&2
    exit 1
fi

echo "Completed classification sweep task ${SLURM_ARRAY_TASK_ID}."

echo "Accounting summary for job ${SLURM_JOB_ID}:"
sacct -j "${SLURM_JOB_ID}" \
    --format=JobName,MaxRSS,AllocTRES,State,Elapsed,Start,ExitCode,DerivedExitCode,Comment
