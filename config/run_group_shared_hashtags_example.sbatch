#!/bin/bash

################################################################################
### Submit from the project root:
### sbatch config/run_group_shared_hashtags_example.sbatch <CAMPAIGN_NAME> <TIME_DELTA>
### Example: sbatch config/run_group_shared_hashtags_example.sbatch Iran_1 15min
################################################################################

#SBATCH --partition=main
#SBATCH --time=2-00:00:00
#SBATCH --job-name=group_shared_hashtags
#SBATCH --output=logs/%j_%x.out
#SBATCH --error=logs/%j_%x.err
#SBATCH --mail-user=amitner@post.bgu.ac.il
#SBATCH --mail-type=ALL
##SBATCH --mem=100G
##SBATCH --cpus-per-task=4

set -euo pipefail

CAMPAIGN_NAME="${1:-}"
TIME_DELTA="${2:-1h}"

if [[ -z "${CAMPAIGN_NAME}" ]]; then
    echo "Usage: sbatch config/run_group_shared_hashtags_example.sbatch <CAMPAIGN_NAME> <TIME_DELTA>" >&2
    exit 1
fi

PROJECT_ROOT="${SLURM_SUBMIT_DIR:-$(pwd)}"
INPUT_NOTEBOOK="${PROJECT_ROOT}/src/temp/group_shared_hashtags_example.ipynb"
OUTPUT_DIRECTORY="${PROJECT_ROOT}/logs/group_shared_hashtags_example"
OUTPUT_NOTEBOOK="${OUTPUT_DIRECTORY}/${SLURM_JOB_ID}_${CAMPAIGN_NAME}_time_delta_${TIME_DELTA}_group_shared_hashtags_example.ipynb"

if [[ ! -d "${PROJECT_ROOT}/results" ]]; then
    echo "ERROR: Project root does not contain results/: ${PROJECT_ROOT}" >&2
    exit 1
fi

if [[ ! -f "${INPUT_NOTEBOOK}" ]]; then
    echo "ERROR: Notebook does not exist: ${INPUT_NOTEBOOK}" >&2
    exit 1
fi

mkdir -p "${OUTPUT_DIRECTORY}"
cd "${PROJECT_ROOT}"

module load anaconda

echo "Running shared-hashtag example for ${CAMPAIGN_NAME}, time delta ${TIME_DELTA}."
conda run --no-capture-output -n backbone_env_v2 \
    papermill \
    "${INPUT_NOTEBOOK}" \
    "${OUTPUT_NOTEBOOK}" \
    -p campaign_name "${CAMPAIGN_NAME}" \
    -p time_window "${TIME_DELTA}"

echo "Completed shared-hashtag example for ${CAMPAIGN_NAME}."
