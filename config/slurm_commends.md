### Interactive Jupyter Notebook ###
conda activate backbone_env_v2
sjupyter --gpu rtx_6000:1


### Non-Interactive Job ###

# 1_translate_topics_entities
```bash
user="$USER"
country="UAE"

cd "/home/${user}/Backbone-Graph/src" || exit 1

sbatch "../config/run_1_translate_topics_entities.sbatch" \
    "../data/Labeled_Datasets/${country}/${country}_part_all.gzip.parquet"
```

# 2_big_data_clustering
```bash

user="$USER"
country="UAE"

cd "/home/${user}/Backbone-Graph/src" || exit 1

for min_cluster_size in 10 128 256 512; do
    sbatch "../config/run_2_big_data_clustering.sbatch" \
        "../results/Labeled_Datasets/${country}/${country}_part_all/step_1_translate_topics_entities/${country}_part_all_step_1.gzip.parquet" \
        "$min_cluster_size"
done
```

# 3_key_authors_graph
```bash
user="$USER"
country="UAE"
topic_col="BERTopic_topic_256"

cd "/home/${user}/Backbone-Graph/src" || exit 1

sbatch "../config/run_3_key_authors_graph.sbatch" \
    "../results/Labeled_Datasets/${country}/${country}_part_all/step_2_big_data_clustering/topic_col_${topic_col}/${country}_part_all_step_2.gzip.parquet"
```

# 4_inter_intra_classification
```bash
user="$USER"
country="UAE"

cd "/home/${user}/Backbone-Graph/src" || exit 1

sbatch "../config/run_4_inter_intra_classification.sbatch" \
    "../results/Labeled_Datasets/${country}/${country}_part_all/step_3_key_authors_graph/topic_col_BERTopic_topic_256_top_percentage_1/"
```

### Interactive Job ###
sinteractive  --time 0-8:00:00  --gpu rtx_6000:1
sinteractive --time 0-8:00:00 --cpu 4

### Utils ###

# List of My Currently Running Jobs
squeue --me

# Cancel Jobs
scancel <job id>
