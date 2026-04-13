#!/bin/bash
#
#SBATCH --job-name sinteractive
#SBATCH --partition main
#SBATCH --qos normal

#SBATCH --cpus-per-task=4
#SBATCH --time=0-8:00:00
#SBATCH --gpus=0
#SBATCH --mem=24G
#SBATCH --nodes=1
#SBATCH -o /home/amitner/Backbone-Graph/interactive_%J.out

#export NODE_TLS_REJECT_UNAUTHORIZED='0'

echo Sun 12 Apr 2026 10:17:42 IDT
launch='sleep 600'
echo " STARTING JOB WITH THE COMMAND:  $launch "
while true; do
        eval $launch
done
