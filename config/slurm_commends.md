### Interactive Job ###
```bash
sinteractive  --time 0-8:00:00  --gpu rtx_6000:1
sinteractive --time 0-8:00:00 --cpu 24
sinteractive --time 0-10:00:00

sjupyter --gpu rtx_6000:1  # not used
```

### Non-Interactive Job ###

# Run Full Pipeline
```bash
country="Ecuador"

/home/${USER}/Backbone-Graph/config/run_full_pipeline.sh ${country}
```

# 1_translate_topics_entities
```bash

country="Ecuador"

user="$USER"
cd "/home/${user}/Backbone-Graph/src"

echo "Submitting translate topics/entities job for country=${country}"
sbatch "../config/run_1_translate_topics_entities.sbatch" \
    "../data/Labeled_Datasets/${country}/${country}_part_all.gzip.parquet"
```

# 2_BERTopic_clustering
```bash

country="Cuba"
min_topic_sizes="10,128,256,512"

user="$USER"
cd "/home/${user}/Backbone-Graph/src"

echo "Submitting BERTopic clustering job for country=${country}, min_topic_sizes=${min_topic_sizes}"
sbatch "../config/run_2_BERTopic_clustering.sbatch" \
    "../results/Labeled_Datasets/${country}/${country}_part_all/step_1_translate_topics_entities/${country}_part_all_step_1.gzip.parquet" \
    "$min_topic_sizes"
```

# 3_key_authors_graph
```bash

country="Iran_1"

user="$USER"
cd "/home/${user}/Backbone-Graph/src"

echo "Submitting key authors graph job for country=${country}"
sbatch "../config/run_3_key_authors_graph.sbatch" \
    "../results/Labeled_Datasets/${country}/${country}_part_all/step_2_BERTopic_clustering/${country}_part_all_step_2.gzip.parquet"
```

# classification_sweep
```bash

country="Armenia"

user="$USER"
cd "/home/${user}/Backbone-Graph/src"

echo "Submitting classification sweep job for country=${country}"
sbatch "../config/run_classification_sweep.sbatch" \
    "../results/Labeled_Datasets/${country}/${country}_part_all/step_2_BERTopic_clustering/${country}_part_all_step_2.gzip.parquet"
```


# 4_inter_intra_classification
```bash

country="Cuba_Test"

user="$USER"
cd "/home/${user}/Backbone-Graph/src"

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
