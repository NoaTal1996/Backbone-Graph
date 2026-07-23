### Interactive Job ###
sinteractive  --time 0-8:00:00  --gpu rtx_6000:1
sinteractive --time 0-8:00:00 --cpu 24

sjupyter --gpu rtx_6000:1


### Non-Interactive Job ###

# 1_translate_topics_entities
```bash
user="$USER"

# Venezuela UAE Ecuador
country="Ecuador"

cd "/home/${user}/Backbone-Graph/src" || exit 1

echo "Submitting translate topics/entities job for country=${country}"
sbatch "../config/run_1_translate_topics_entities.sbatch" \
    "../data/Labeled_Datasets/${country}/${country}_part_all.gzip.parquet"
```

# 2_BERTopic_clustering
```bash

user="$USER"
country="UAE"

cd "/home/${user}/Backbone-Graph/src" || exit 1

for min_cluster_size in 10 128 256 512; do
    echo "Submitting BERTopic clustering job for country=${country}, min_cluster_size=${min_cluster_size}"
    sbatch "../config/run_2_BERTopic_clustering.sbatch" \
        "../results/Labeled_Datasets/${country}/${country}_part_all/step_1_translate_topics_entities/${country}_part_all_step_1.gzip.parquet" \
        "$min_cluster_size"
done
```

# 3_key_authors_graph
```bash
user="$USER"
country="UAE"

cd "/home/${user}/Backbone-Graph/src" || exit 1

echo "Submitting key authors graph job for country=${country}, topic_col=${topic_col}"
sbatch "../config/run_3_key_authors_graph.sbatch" \
    "../results/Labeled_Datasets/${country}/${country}_part_all/step_2_BERTopic_clustering/${country}_part_all_step_2.gzip.parquet"
```

# 4_inter_intra_classification
```bash
user="$USER"
country="UAE"

cd "/home/${user}/Backbone-Graph/src" || exit 1

echo "Submitting inter/intra classification job for country=${country}"
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
