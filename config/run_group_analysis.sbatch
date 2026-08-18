#!/bin/bash

################################################################################
### Submit from the project root:
### sbatch config/run_group_analysis.sbatch <CAMPAIGN_NAME>
################################################################################

#SBATCH --partition=main
#SBATCH --time=2-00:00:00
#SBATCH --job-name=group_analysis
#SBATCH --output=logs/%j_%x.out
#SBATCH --error=logs/%j_%x.err
#SBATCH --mail-type=END,FAIL
#SBATCH --mem=100G
#SBATCH --cpus-per-task=4

set -euo pipefail

CAMPAIGN_NAME="${1:-}"

if [[ -z "${CAMPAIGN_NAME}" ]]; then
    echo "ERROR: No campaign name provided." >&2
    echo "Usage: sbatch config/run_group_analysis.sbatch <CAMPAIGN_NAME>" >&2
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
INPUT_NOTEBOOK="${PROJECT_ROOT}/src/temp/group_analysis.ipynb"
OUTPUT_DIRECTORY="${PROJECT_ROOT}/logs/group_analysis"
OUTPUT_NOTEBOOK="${OUTPUT_DIRECTORY}/${SLURM_JOB_ID}_${CAMPAIGN_NAME}_group_analysis.ipynb"

if [[ ! -f "${INPUT_NOTEBOOK}" ]]; then
    echo "ERROR: Notebook does not exist: ${INPUT_NOTEBOOK}" >&2
    exit 1
fi

mkdir -p "${OUTPUT_DIRECTORY}"
cd "${PROJECT_ROOT}"

echo "$(date)"
echo -e "\nSLURM_JOB_ID:\t\t${SLURM_JOB_ID}"
echo -e "SLURM_JOB_NODELIST:\t${SLURM_JOB_NODELIST}"
echo -e "Job name:\t\t${SLURM_JOB_NAME}"
echo -e "Campaign:\t\t${CAMPAIGN_NAME}"
echo -e "Input notebook:\t\t${INPUT_NOTEBOOK}"
echo -e "Output notebook:\t${OUTPUT_NOTEBOOK}"

module load anaconda

echo "Starting group analysis for ${CAMPAIGN_NAME}..."

conda run --no-capture-output -n backbone_env_v2 \
    papermill \
    "${INPUT_NOTEBOOK}" \
    "${OUTPUT_NOTEBOOK}" \
    -p campaign_name "${CAMPAIGN_NAME}"

echo "Completed group analysis for ${CAMPAIGN_NAME}."
