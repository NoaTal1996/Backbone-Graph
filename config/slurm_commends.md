### Interactive Jupyter Notebook ###
conda activate backbone_env
sjupyter --gpu rtx_6000:1


### Non-Interactive Job ###
cd /home/amitner/Backbone-Graph
sbatch "/home/amitner/Backbone-Graph/config/run_clean_translate_topics.sbatch" Ecuador_part_1.gzip.parquet
sbatch /home/amitner/Backbone-Graph/config/run_big_data_clustering.sbatch 256

### Interactive Job ###
sinteractive --gpu rtx_6000:1


# List of My Currently Running Jobs
squeue --me

# Cancel Jobs
scancel <job id>
