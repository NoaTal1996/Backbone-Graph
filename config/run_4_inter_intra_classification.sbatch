#!/bin/bash

################################################################################################
### sbatch configuration parameters must start with #SBATCH and must precede any other commands.
### To ignore, just add another # - like so: ##SBATCH
################################################################################################

#SBATCH --partition main
#SBATCH --time 7-00:00:00
#SBATCH --job-name 4_inter_intra_classification
#SBATCH --output=../logs/%j_%x.out
#SBATCH --error=../logs/%j_%x.err
#SBATCH --mail-user=amitner@post.bgu.ac.il
#SBATCH --mail-type=ALL
##SBATCH --mem=48G
##SBATCH --cpus-per-task=24

# INPUT_FILE_PATH="$1"

# if [ -z "$INPUT_FILE_PATH" ]; then
#     echo "ERROR: No input path provided!"
#     echo "Usage: sbatch run_4_inter_intra_classification.sbatch <INPUT_STEP_3_FOLDER>"
#     exit 1
# fi

echo "$(date)"
echo -e "\nSLURM_JOB_ID:\t\t$SLURM_JOB_ID"
echo -e "SLURM_JOB_NODELIST:\t$SLURM_JOB_NODELIST"
echo -e "Job name:\t\t$SLURM_JOB_NAME"
echo -e "INPUT_FILE_PATH:\t$INPUT_FILE_PATH"

module load anaconda
source activate backbone_env_v2

IN_NOTEBOOK="${SLURM_JOB_NAME}.ipynb"
OUT_NOTEBOOK="../logs/${SLURM_JOB_ID}_${SLURM_JOB_NAME}.ipynb"

echo "Starting papermill..."
conda run -n backbone_env_v2 papermill "${IN_NOTEBOOK}" "${OUT_NOTEBOOK}" -p # input_data_path "$INPUT_FILE_PATH"

echo "Completed ${SLURM_JOB_NAME}!"
