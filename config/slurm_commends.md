### Interactive Jupyter Notebook ###
conda activate backbone_env
sjupyter --gpu rtx_6000:1


### Non-Interactive Job ###
cd /home/amitner/Backbone-Graph
sbatch "/home/amitner/Backbone-Graph/config/run_notebook.sbatch" Ecuador_part_3.gzip.parquet

### Interactive Job ###
sinteractive --gpu rtx_6000:1


# List of My Currently Running Jobs
squeue --me

# Cancel Jobs
scancel <job id>
