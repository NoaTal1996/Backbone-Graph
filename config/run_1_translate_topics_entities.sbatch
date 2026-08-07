#!/bin/bash

################################################################################################
### sbatch configuration parameters must start with #SBATCH and must precede any other commands.
### To ignore, just add another # - like so: ##SBATCH
################################################################################################

#SBATCH --partition main			                    ### partition name where to run a job. change only if you have a matching qos!! main: all nodes; gtx1080: 1080 gpu card nodes; rtx2080: 2080 nodes; teslap100: p100 nodes; titanrtx: titan nodes
#SBATCH --time 7-00:00:00			                    ### Time Limit Format: D-H:MM:SS
#SBATCH --job-name 1_translate_topics_entities		    ### name of the job
#SBATCH --output=../logs/%j_%x.out                      ### %j – Job ID, %x – Job name
#SBATCH --error=../logs/%j_%x.err
#SBATCH --gpus=rtx_4090:1		                        ### number of GPUs, allocating more than 1 requires IT team's permission. Example to request 3090 gpu: #SBATCH --gpus=rtx_3090:1

### Note: Lines are with ## are commented out
#SBATCH --mail-user=amitner@post.bgu.ac.il	            ### user's email for sending job status messages
#SBATCH --mail-type=ALL			                        ### conditions for sending the email. ALL,BEGIN,END,FAIL, REQUEU, NONE
#SBATCH --mem=80G				                        ### RAM memory; use an explicit GiB suffix

################  Following lines will be executed by a compute node    #######################




################################### run from the IN_NOTEBOOK folder ###################################



### Read argument from command line
INPUT_FILE_PATH="$1"
FORCE_RESTART="${2:-false}"

if [ -z "$INPUT_FILE_PATH" ]; then
    echo "ERROR: No input file path provided!"
    echo "Usage: sbatch run_1_translate_topics_entities.sbatch <INPUT_FILE_PATH> [FORCE_RESTART]"
    exit 1
fi

if [[ "$FORCE_RESTART" != "true" && "$FORCE_RESTART" != "false" ]]; then
    echo "ERROR: FORCE_RESTART must be 'true' or 'false'."
    exit 1
fi

### Print some data to output file ###
echo "$(date)"
echo -e "\nSLURM_JOB_ID:\t\t$SLURM_JOB_ID"
echo -e "SLURM_JOB_NODELIST:\t$SLURM_JOB_NODELIST"
echo -e "Job name:\t\t$SLURM_JOB_NAME"
echo -e "INPUT_FILE_PATH:\t$INPUT_FILE_PATH"
echo -e "FORCE_RESTART:\t\t$FORCE_RESTART"

### Start your code below ####
module load anaconda				### load anaconda module
source activate backbone_env_v2

# papermill
IN_NOTEBOOK="${SLURM_JOB_NAME}.ipynb"

OUT_NOTEBOOK="../logs/${SLURM_JOB_ID}_${SLURM_JOB_NAME}.ipynb"

conda run -n backbone_env_v2 papermill \
    "${IN_NOTEBOOK}" \
    "${OUT_NOTEBOOK}" \
    -p input_data_path "$INPUT_FILE_PATH" \
    -p force_restart "$FORCE_RESTART"
