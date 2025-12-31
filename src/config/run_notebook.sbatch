#!/bin/bash

################################################################################################
### sbatch configuration parameters must start with #SBATCH and must precede any other commands.
### To ignore, just add another # - like so: ##SBATCH
################################################################################################

#SBATCH --partition main			### specify partition name where to run a job. change only if you have a matching qos!! main: all nodes; gtx1080: 1080 gpu card nodes; rtx2080: 2080 nodes; teslap100: p100 nodes; titanrtx: titan nodes
#SBATCH --time 2-00:00:00			### limit the time of job running. Make sure it is not greater than the partition time limit!! Format: D-H:MM:SS
#SBATCH --job-name Topic_Clustring_and_NER			### name of the job
#SBATCH --output=logs/jupyter-%j.out
#SBATCH --error=logs/jupyter-%j.err	  ### output log for running job - %J for job number
#SBATCH --gpus=rtx_4090:1		  ### number of GPUs, allocating more than 1 requires IT team's permission. Example to request 3090 gpu: #SBATCH --gpus=rtx_3090:1

### Note: Lines are with ## are commented out
#SBATCH --mail-user=amitner@post.bgu.ac.il	  ### user's email for sending job status messages
#SBATCH --mail-type=ALL			                  ### conditions for sending the email. ALL,BEGIN,END,FAIL, REQUEU, NONE
##SBATCH --mem=24G				                    ### ammount of RAM memory, allocating more than 60G requires IT team's permission

################  Following lines will be executed by a compute node    #######################



### Read argument from command line
DATASET_FILE_NAME="$1"

if [ -z "$DATASET_FILE_NAME" ]; then
    echo "ERROR: No file name provided!"
    echo "Usage: sbatch run_notebook.sh <DATASET_FILE_NAME>"
    exit 1
fi

### Print some data to output file ###
echo `date`
echo -e "\nSLURM_JOBID:\t\t" $SLURM_JOBID
echo -e "SLURM_JOB_NODELIST:\t" $SLURM_JOB_NODELIST "\n\n"

### Start your code below ####
module load anaconda				### load anaconda module
source activate backbone_env
cd /home/amitner/Backbone-Graph/src
conda run -n backbone_env papermill "Topic_Clustring_and_NER.ipynb" "../logs/${DATASET_FILE_NAME}_Topic_Clustring_and_NER-${SLURM_JOB_ID}.ipynb" -p file_name "$DATASET_FILE_NAME"