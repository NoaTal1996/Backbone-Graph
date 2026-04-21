### Interactive Jupyter Notebook ###
conda activate backbone_env_v2
sjupyter --gpu rtx_6000:1


### Non-Interactive Job ###

# translate_topics_entities
cd /home/amitner/Backbone-Graph/src
sbatch "../config/run_translate_topics_entities.sbatch" Ecuador_part_all.gzip.parquet

# big_data_clustering
cd /home/amitner/Backbone-Graph/src
sbatch "../config/run_big_data_clustering.sbatch" 256

# key_authors_graph
cd /home/amitner/Backbone-Graph/src
sbatch "../config/run_key_authors_graph.sbatch"

### Interactive Job ###
sinteractive  --time 0-8:00:00  --gpu rtx_6000:1
sinteractive --time 0-8:00:00 --cpu 4

### Utils ###

# List of My Currently Running Jobs
squeue --me

# Cancel Jobs
scancel <job id>
