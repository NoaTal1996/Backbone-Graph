### Interactive Jupyter Notebook ###
conda activate backbone_env_v2
sjupyter --gpu rtx_6000:1


### Non-Interactive Job ###

# 1_translate_topics_entities
cd /home/amitner/Backbone-Graph/src
sbatch "../config/run_1_translate_topics_entities.sbatch" ../data/Labeled_Datasets/Ecuador/Ecuador_part_all.gzip.parquet

# 2_big_data_clustering
cd /home/amitner/Backbone-Graph/src
sbatch "../config/run_2_big_data_clustering.sbatch" ../results/Labeled_Datasets/Ecuador/Ecuador_part_all/step_1_translate_topics_entities/Ecuador_part_all_step_1.gzip.parquet 256

# 3_key_authors_graph
cd /home/amitner/Backbone-Graph/src
sbatch "../config/run_3_key_authors_graph.sbatch" ../results/Labeled_Datasets/Ecuador/Ecuador_part_all/step_2_big_data_clustering/topic_col_BERTopic_topic_256/Ecuador_part_all_step_2.gzip.parquet

# 4_inter_intra_classification
cd /home/amitner/Backbone-Graph/src
sbatch "../config/run_4_inter_intra_classification.sbatch" ../results/Labeled_Datasets/Ecuador/Ecuador_part_all/step_3_key_authors_graph/topic_col_BERTopic_topic_256_top_percentage_1/

### Interactive Job ###
sinteractive  --time 0-8:00:00  --gpu rtx_6000:1
sinteractive --time 0-8:00:00 --cpu 4

### Utils ###

# List of My Currently Running Jobs
squeue --me

# Cancel Jobs
scancel <job id>
