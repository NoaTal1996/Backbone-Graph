### Interactive Jupyter Notebook ###
conda activate backbone_env
sjupyter --gpu rtx_6000:1


### Non-Interactive Job ###
cd /home/amitner/Backbone-Graph/src
sbatch "../config/run_translate_topics_entities.sbatch" Ecuador_part_1.gzip.parquet

cd /home/amitner/Backbone-Graph/src
sbatch "../config/run_big_data_clustering.sbatch" 256

cd /home/amitner/Backbone-Graph/src
sbatch "../config/run_key_authors_graph.sbatch"

### Interactive Job ###
sinteractive --gpu rtx_6000:1


# List of My Currently Running Jobs
squeue --me

# Cancel Jobs
scancel <job id>
