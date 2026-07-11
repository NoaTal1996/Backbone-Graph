### Interactive Jupyter Notebook ###
conda activate backbone_env_v2
sjupyter --gpu rtx_6000:1


### Non-Interactive Job ###

# 1_translate_topics_entities
cd /home/amitner/Backbone-Graph/src
sbatch "../config/run_translate_topics_entities.sbatch" ../data/Labeled_Datasets/Ecuador/Ecuador_part_all.gzip.parquet

# 2_big_data_clustering
cd /home/amitner/Backbone-Graph/src
sbatch "../config/run_big_data_clustering.sbatch" ../results/Labeled_Datasets/Ecuador/Ecuador_part_all/step_1/Ecuador_part_all_step1.gzip.parquet 256

# 3_key_authors_graph
cd /home/amitner/Backbone-Graph/src
sbatch "../config/run_key_authors_graph.sbatch" ../results/Labeled_Datasets/Ecuador/Ecuador_part_all/step_2/Ecuador_part_all_step2.gzip.parquet

# inter_intra_classification
cd /home/amitner/Backbone-Graph/src
sbatch "../config/run_inter_intra_classification.sbatch" ../results/Labeled_Datasets/Ecuador/Ecuador_part_all/step_3/

### Interactive Job ###
sinteractive  --time 0-8:00:00  --gpu rtx_6000:1
sinteractive --time 0-8:00:00 --cpu 4

### Utils ###

# List of My Currently Running Jobs
squeue --me

# Cancel Jobs
scancel <job id>
