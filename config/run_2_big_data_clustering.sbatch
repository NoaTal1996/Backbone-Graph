#!/bin/bash

################################################################################################
### sbatch configuration parameters must start with #SBATCH and must precede any other commands.
### To ignore, just add another # - like so: ##SBATCH
################################################################################################

#SBATCH --partition main			                ### specify partition name where to run a job. change only if you have a matching qos!! main: all nodes; gtx1080: 1080 gpu card nodes; rtx2080: 2080 nodes; teslap100: p100 nodes; titanrtx: titan nodes
#SBATCH --time 7-00:00:00			                ### limit the time of job running. Make sure it is not greater than the partition time limit!! Format: D-H:MM:SS
#SBATCH --job-name 2_big_data_clustering			### name of the job
#SBATCH --output=../logs/%x_%j.out                  ### %x – Job name, %j – Job ID
#SBATCH --error=../logs/%x_%j.err
#SBATCH --gpus=rtx_4090:1		                    ### number of GPUs, allocating more than 1 requires IT team's permission. Example to request 3090 gpu: #SBATCH --gpus=rtx_3090:1

### Note: Lines are with ## are commented out
#SBATCH --mail-user=idanmu@post.bgu.ac.il	        ### user's email for sending job status messages
#SBATCH --mail-type=ALL			                    ### conditions for sending the email. ALL,BEGIN,END,FAIL, REQUEU, NONE
#SBATCH --mem=60G				                    ### ammount of RAM memory, allocating more than 60G requires IT team's permission

################  Following lines will be executed by a compute node    #######################



################################### run from the IN_NOTEBOOK folder ###################################


### Read argument from command line
INPUT_FILE_PATH="$1"
MIN_TOPIC_SIZE="$2"

if [ -z "$INPUT_FILE_PATH" ]; then
    echo "ERROR: No input file path provided!"
    echo "Usage: sbatch run_2_big_data_clustering.sbatch <INPUT_FILE_PATH> [MIN_TOPIC_SIZE]"
    exit 1
fi

### Print some data to output file ###
echo `date`
echo -e "\nSLURM_JOBID:\t\t" $SLURM_JOBID
echo -e "SLURM_JOB_NODELIST:\t" $SLURM_JOB_NODELIST "\n\n"
echo -e "Job name:\t\t$SLURM_JOB_NAME"
echo -e "\nINPUT_FILE_PATH:\t" $INPUT_FILE_PATH
echo -e "\nMIN_TOPIC_SIZE:\t" $MIN_TOPIC_SIZE

### Start your code below ####
module load anaconda				### load anaconda module
source activate backbone_env_v2

# papermill
IN_NOTEBOOK="${SLURM_JOB_NAME}.ipynb"
OUT_NOTEBOOK="../logs/${SLURM_JOB_NAME}_${SLURM_JOB_ID}.ipynb"

PAPERMILL_ARGS=(-p input_file_path "$INPUT_FILE_PATH")
if [ -n "$MIN_TOPIC_SIZE" ]; then
    OUT_NOTEBOOK="../logs/${SLURM_JOB_NAME}_${SLURM_JOB_ID}_size_${MIN_TOPIC_SIZE}.ipynb"
    PAPERMILL_ARGS+=(-p min_topic_size "$MIN_TOPIC_SIZE")
fi

conda run -n backbone_env_v2 papermill "${IN_NOTEBOOK}" "${OUT_NOTEBOOK}" "${PAPERMILL_ARGS[@]}"
