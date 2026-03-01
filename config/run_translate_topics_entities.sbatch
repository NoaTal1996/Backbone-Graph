#!/bin/bash

################################################################################################
### sbatch configuration parameters must start with #SBATCH and must precede any other commands.
### To ignore, just add another # - like so: ##SBATCH
################################################################################################

#SBATCH --partition main			                    ### partition name where to run a job. change only if you have a matching qos!! main: all nodes; gtx1080: 1080 gpu card nodes; rtx2080: 2080 nodes; teslap100: p100 nodes; titanrtx: titan nodes
#SBATCH --time 3-00:00:00			                    ### Time Limit Format: D-H:MM:SS
#SBATCH --job-name translate_topics_entities		    ### name of the job
#SBATCH --output=../logs/%x_%j.out                      ### %x – Job name, %j – Job ID
#SBATCH --error=../logs/%x_%j.err
##SBATCH --gpus=rtx_4090:1		                        ### number of GPUs, allocating more than 1 requires IT team's permission. Example to request 3090 gpu: #SBATCH --gpus=rtx_3090:1

### Note: Lines are with ## are commented out
#SBATCH --mail-user=amitner@post.bgu.ac.il	            ### user's email for sending job status messages
#SBATCH --mail-type=ALL			                        ### conditions for sending the email. ALL,BEGIN,END,FAIL, REQUEU, NONE
#SBATCH --mem=60G				                        ### ammount of RAM memory, allocating more than 60G requires IT team's permission

################  Following lines will be executed by a compute node    #######################




################################### run from the IN_NOTEBOOK folder ###################################



### Read argument from command line
DATASET_FILE_NAME="$1"


if [ -z "$DATASET_FILE_NAME" ]; then
    echo "ERROR: No file name provided!"
    echo "Usage: sbatch run_translate_topics_entities.sbatch <DATASET_FILE_NAME>"
    exit 1
fi

### Print some data to output file ###
echo "$(date)"
echo -e "\nSLURM_JOB_ID:\t\t$SLURM_JOB_ID"
echo -e "SLURM_JOB_NODELIST:\t$SLURM_JOB_NODELIST"
echo -e "Job name:\t\t$SLURM_JOB_NAME"

### Start your code below ####
module load anaconda				### load anaconda module
source activate backbone_env

# papermill
IN_NOTEBOOK="${SLURM_JOB_NAME}.ipynb"
OUT_NOTEBOOK="../logs/${SLURM_JOB_NAME}_${SLURM_JOB_ID}_${DATASET_FILE_NAME}.ipynb"

conda run -n backbone_env papermill "${IN_NOTEBOOK}" "${OUT_NOTEBOOK}" -p file_name "$DATASET_FILE_NAME"