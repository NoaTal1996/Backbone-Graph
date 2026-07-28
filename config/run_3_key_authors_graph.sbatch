#!/bin/bash

################################################################################################
### sbatch configuration parameters must start with #SBATCH and must precede any other commands.
### To ignore, just add another # - like so: ##SBATCH
################################################################################################

#SBATCH --partition main			                    ### partition name where to run a job
#SBATCH --time 7-00:00:00			                    ### Time Limit Format: D-H:MM:SS
#SBATCH --job-name 3_key_authors_graph		            ### name of the job
#SBATCH --output=../logs/%j_%x.out                      ### %j – Job ID, %x – Job name
#SBATCH --error=../logs/%j_%x.err
##SBATCH --gpus=rtx_4090:1

##SBATCH --mail-user=idanmu@post.bgu.ac.il	            ### user's email for sending job status messages
#SBATCH --mail-user=amitner@post.bgu.ac.il	            ### user's email for sending job status messages
#SBATCH --mail-type=ALL			                        ### conditions for sending the email. ALL,BEGIN,END,FAIL, REQUEU, NONE
#SBATCH --mem=120G				                        ### ammount of RAM memory, allocating more than 60G requires IT team's permission
#SBATCH --cpus-per-task=64

################  Following lines will be executed by a compute node    #######################

set -e

### Read argument from command line
INPUT_FILE_PATH="$1"

if [ -z "$INPUT_FILE_PATH" ]; then
    echo "ERROR: No input file path provided!"
    echo "Usage: sbatch run_3_key_authors_graph.sbatch <INPUT_FILE_PATH>"
    exit 1
fi

### Print some data to output file ###
echo "$(date)"
echo -e "\nSLURM_JOB_ID:\t\t$SLURM_JOB_ID"
echo -e "SLURM_JOB_NODELIST:\t$SLURM_JOB_NODELIST"
echo -e "Job name:\t\t$SLURM_JOB_NAME"
echo -e "INPUT_FILE_PATH:\t$INPUT_FILE_PATH"

### Start your code ###
module load anaconda
source activate backbone_env_v2

IN_NOTEBOOK="${SLURM_JOB_NAME}.ipynb"
OUT_NOTEBOOK="../logs/${SLURM_JOB_ID}_${SLURM_JOB_NAME}.ipynb"

echo "Starting papermill..."
conda run -n backbone_env_v2 papermill "${IN_NOTEBOOK}" "${OUT_NOTEBOOK}" -p input_data_path "$INPUT_FILE_PATH"

echo "Completed ${SLURM_JOB_NAME}!"
