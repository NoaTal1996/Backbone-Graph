## Workflow

![Workflow](../docs/figures/workflow.jpg)

This folder (`Backbone-Graph/src`) contains the code for this workflow.

## Working Directory

Working directory assumption (matches the notebooks): run from `Backbone-Graph/src`.

## Results Folder Structure

Each dataset part has one folder under
`results/<dataset_name>/<country>/<part>/`. Notebook steps are stored as
sibling folders. Steps 2 and 3 include the parameters that identify their
configuration.

```text
results/
└── <dataset_name>/
    └── <country>/
        └── <part>/
            ├── step_1_translate_topics_entities/
            │   ├── <part>_step_1.gzip.parquet
            │   └── progress_report.txt
            ├── step_2_BERTopic_clustering/
            │   └── topic_col_<topic_col>/
            │       ├── <part>_step_2.gzip.parquet
            │       └── progress_report.txt
            ├── step_3_key_authors_graph/
            │   └── topic_col_<topic_col>_top_percentage_<top_percentage>/
            │       ├── <part>_step_3.gzip.parquet
            │       └── progress_report.txt
            ├── step_4_inter_intra_classification/
            │   └── progress_report.txt
            └── step_Boost/
                └── progress_report.txt
```

For example, with `topic_col = "BERTopic_topic_256"` and
`top_percentage = 1`, the Step 3 output folder is:

```text
results/Labeled_Datasets/Ecuador/Ecuador_part_all/
step_3_key_authors_graph/topic_col_BERTopic_topic_256_top_percentage_1/
```

## Terms

- **Information Operation (IO)**: A collection of publications produced by a set of actors performing similar or complementary actions in pursuit of a shared intent, while misleading others.
- **IO Driver**: An account that participates in one or more IO.
- Author’s **IO Label**: label = 1 if the author is IO Driver and label = 0 if not.
- **Key Author**: An author who acts as a leading participant in one or more narratives or topics.


## Notebook order (pipeline)

### 1. `1_translate_topics_entities.ipynb`
  - Pre-processing: Dataset cleaning and text translation.
  - Entities Recognition (NER): Identifying and storing named entities.
  - Topic modeling (for data up to 100k posts).

> **Large dataset?** Switch to `2_BERTopic_clustering.ipynb` for the clustering step — pre-processing and NER still run here first.

### 2. `3_key_authors_graph.ipynb`
  - Calculates TF-IDF score for entities, posts and authors.
  - key authors selection: Identifies leading participants within specific topics.
  - Backbone graph building: Constructs a directed account graph (GEXF) based on user interactions.
  - IO indicators: Generates summaries of Information Operation (IO) activity.

### Not part of the pipeline

- `Boost.ipynb` is not part of the ordered workflow.

### 3. `4_inter_intra_classification.ipynb`
  - Runs classification experiments from a `step_3_key_authors_graph/` configuration folder.
  - Saves results and plots to the matching `step_4_inter_intra_classification/` folder.

## Evaluation
### a. `author_insights.ipynb`
- Gives insights about an author

### b. `topic_clustering_evaluation.ipynb`
- Produce a report on the topic clustering.
- Calculate Coherence for each topic

## Notebook details

### 1) `1_translate_topics_entities.ipynb`

The pipeline's entry point. Takes a raw social media dataset, cleans and translates the text, extracts named entities, and clusters posts into topics.

**Inputs**
- Parameters in the notebook:
  - `input_data_path` — raw parquet path under `data/` (e.g., `"../data/Labeled_Datasets/Venezuela/Venezuela_part_all.gzip.parquet"`).
  - `min_topic_size` — BERTopic minimum cluster size.
- Input Parquet must follow the schema at https://zenodo.org/records/14189193.

**What it does**
- Loads the parquet and performs dataset cleaning.
- Translates posts' text.
- Runs NER and stores enriched columns in the dataframe.
- Builds embeddings and performs topic clustering (BERTopic, K-Means).
- Writes progress logs during execution.

**Outputs**
- Output folder: `results/<dataset>/<country>/<part>/step_1_translate_topics_entities/`
- Main Artifacts created:
  - `<input_stem>_step_1.gzip.parquet`
  - `dataset_summary.txt`
  - `progress_report.txt`
  - `BERTopic_model_<min_topic_size>` 
  - `Topic plots` (PNG) such as BERTopic topic distribution / accounts distribution.


---

### 1b) `2_BERTopic_clustering.ipynb` (for huge datasets)

This notebook is intended for **large-scale topic clustering** (chunked BERTopic + merge). It should be used after `1_translate_topics_entities.ipynb` runs into OOM.

**Inputs**
- Parameters in the notebook:
  - `input_data_path` — Step 1 parquet path (e.g., `"../results/Labeled_Datasets/Egypt_UAE/Egypt_UAE_part_all/step_1_translate_topics_entities/Egypt_UAE_part_all_step_1.gzip.parquet"`).
  - `min_topic_size` (used for BERTopic and deriving `topic_col`).
  - `chunk_size` (controls how many documents per BERTopic chunk).
- Reads the preprocessed parquet produced by notebook 1.

**What it does**
- Loads the preprocessed dataset.
- Trains BERTopic in chunks and merges the chunk models.
- Adds topic labels back into the dataframe.
- Generates topic statistics and plots (post counts per topic, unique accounts per topic).
- Saves progress reports during long runs.

**Outputs**
- Output folder: `step_2_BERTopic_clustering/topic_col_<topic_col>/`
- `<input_stem>_step_2.gzip.parquet`
- `BERTopic_models_min_topic_size_<min_topic_size>/` (chunk models + merged model)
- Plots (PNG): `<topic_col>_topic_clustering.png`, `<topic_col>_topic_accounts.png`

---

### 2) `3_key_authors_graph.ipynb`

This notebook builds the **Key-Authors Backbone graph** for the chosen topic column and exports it to GEXF.

**Inputs**
- Parameters in the notebook:
  - `input_data_path` — Step 1 or Step 2 parquet path.
  - `topic_col` (example: `BERTopic_topic_256`)
  - `top_percentage` — fraction of top authors per topic to select as key authors (e.g., `0.01` = top 1%).
  - `account_id_col` — account identifier column (default: `"accountid"`).
- The processed dataframe is expected to contain:
  - The chosen `topic_col`
  - Interaction columns used to build edges (e.g., replies/mentions/reposts; see notebook)

**What it does**
- Computes author-topic TF-IDF and identifies “key authors” per topic.
- Produces IO summaries.
- Builds a directed accounts graph and exports it to GEXF.

**Outputs** (written to `step_3_key_authors_graph/topic_col_<topic_col>_top_percentage_<top_percentage>/`)
- `<input_stem>_step_3.gzip.parquet`
- `author_topic_key_score_by_<topic_col>.parquet`
- `io_key_authors_summary.txt`
- `accounts_graph_topic_col_<topic_col>.gexf`
- Additional indicators/plots/parquets (information gain, IO classification reports, comparisons, etc.)

### 3) `4_inter_intra_classification.ipynb`

Runs classification experiments from a Step 3 output folder.

**Inputs**
- Parameters in the notebook:
  - `input_data_path` — Step 3 configuration folder path.
  - `target_campaign` — label used in the results for single-folder runs.
  - `graph_filtering_setting` — node-indicators variant to load.

**Outputs** (written to the matching `step_4_inter_intra_classification/` folder)
- `experiment_results_<graph_filtering_setting>.csv`
- `strategy_comparison_auc.png`
- `strategy_comparison_macro_f1.png`

## Batch execution (SLURM)

The repo contains papermill-based SLURM scripts:
- Translate + clustering:

  - `sbatch ../config/run_1_translate_topics_entities.sbatch <INPUT_FILE_PATH>`
  - Script: `../config/run_1_translate_topics_entities.sbatch`
- Big data clustering:

  - `sbatch ../config/run_2_BERTopic_clustering.sbatch <STEP_1_PARQUET> [MIN_TOPIC_SIZE]`
  - Script: `../config/run_2_BERTopic_clustering.sbatch`
- Key authors graph:

  - `sbatch ../config/run_3_key_authors_graph.sbatch <STEP_1_OR_STEP_2_PARQUET>`
  - Script: `../config/run_3_key_authors_graph.sbatch`
- Inter/intra classification:

  - `sbatch ../config/run_4_inter_intra_classification.sbatch <STEP_3_FOLDER>`
  - Script: `../config/run_4_inter_intra_classification.sbatch`

See `../config/slurm_commends.md` for examples.
