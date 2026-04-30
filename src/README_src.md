## Workflow

![Workflow](../docs/figures/workflow.jpg)

This folder (`Backbone-Graph/src`) contains the code for this workflow.

## Working Directory

Working directory assumption (matches the notebooks): run from `Backbone-Graph/src`.

## Terms

- **Information Operation (IO)**: A collection of publications produced by a set of actors performing similar or complementary actions in pursuit of a shared intent, while misleading others.
- **IO Driver**: An account that participates in one or more IO.
- Author ‘s **IO Label**: label =  1 if the author is IO Driver and label = 0 if not.
- **Key Author**: An author who acts as a leading participant in one or more narratives or topics.


## Notebook order (pipeline)

### 1. `translate_topics_entities.ipynb`
  - Pre-processing: Dataset cleaning and text translation.
  - Entities Recognition (NER): Identifying and storing named entities.
  - Topic modeling (for data up to 100k posts). <br/>
      If the dataset is too large for the clustering (usealy OOM error), use `big_data_clustering.ipynb` for the topic modeling. Note that pre-prosses and NER are stiil preformed by `translate_and_clustering.ipynb`.

### 2. `key_authors_graph.ipynb`
  - Calculates TF-IDF score for enttities, posts and authors.
  - key autros selection : Identifies leading participants within specific topics.
  - Backbone graph bulding : Constructs a directed account graph (GEXF) based on user interactions.
  - IO indicators : Generates summaries of Information Operation (IO) activity.

### Not part of the pipeline

- `Boost.ipynb` is  not part of the ordered workflow.

## Evaluation
### a. `author_insights.ipynb`
- Gives insights about an author

### b. `topic_clustering_evaluation.ipynb`
- Produce a report on the topic clustering.
- Calculate Coherence for each topic

## Notebook details

### 1) `translate_and_clustering.ipynb`

**Inputs**
- Path to a combined Dataset parquet with the secma like https://zenodo.org/records/14189193.
- `min_topic_size` (used for BERTopic and naming the output folder)

**What it does**
- Loads the parquet and performs dataset cleaning.
- Translates posts' text.
- Runs NER and stores enriched columns in the dataframe.
- Builds embeddings and performs topic clustering (BERTopic, K-Means).
- Writes progress logs during execution.

**Outputs**
- Output to `results/<campaing's name>` folder or `final_results` folder. Examaple: 
- Main Artifacts created:
  - `processed_<file_name>` (gzip parquet)
  - `dataset_summary.txt`
  - `progress_report.txt`
  - `BERTopic_model` 
  - `Topic plots` (PNG) such as BERTopic topic distribution / accounts distribution.


---

### 1b) `big_data_clustering.ipynb` (for huge datasets)

This notebook is intended for **large-scale topic clustering** (chunked BERTopic + merge). It should be used after `translate_topic_entities.ipynb` rins into OOM.

**Inputs**
- A path to **preprocessed parquet** that already contains the translated / NER-enriched content required for clustering.
- Parameters in the notebook:
  - `min_topic_size` (used for BERTopic and naming the output folder).
  - `chunk_size` (controls how many documents per BERTopic chunk).

**What it does**
- Loads the preprocessed dataset.
- Trains BERTopic in chunks and merges the chunk models.
- Adds topic labels back into the dataframe.
- Generates topic statistics and plots (post counts per topic, unique accounts per topic).
- Saves progress reports during long runs.

**Outputs**
- Output root (current behavior):
  - `processed_<raw_file_name_no_suffixes>.gzip.parquet`
  - `progress_reports/progress_report_min_topic_size_<min_topic_size>.txt`
  - `BERTopic_models_min_topic_size_<min_topic_size>/` (chunk models + merged model)
  - Plots (PNG) like `<topic_col>_topic_clustering.png` and `<topic_col>_topic_accounts.png`

---

### 2) `key_authors_graph.ipynb`

This notebook builds the **Key-Authors Backbone graph** for the chosen topic column and exports it to GEXF.

**Inputs**
- A processed parquet (with topic labels) at:
- Parameters in the notebook:
  - Path to the the procced dataset from notbook (1).
  - `topic_col` (example: `BERTopic_topic_512`)
  - `top_n` (example: `300`; top authors per topic)
- The processed dataframe is expected to contain:
  - An account identifier (default: `accountid`)
  - The chosen `topic_col`
  - Interaction columns used to build edges (e.g., replies/mentions/reposts; see notebook)

**What it does**
- Computes author-topic TF-IDF and identifies “key authors” per topic.
- Produces IO summaries.
- Builds a directed accounts graph and exports.

**Outputs** (written to the same folder as the processed parquet)
- `author_topic_tfidf_by_<topic_col>.parquet`
- `io_key_authors_summary.txt`
- `<topic_col>_accounts_graph.gexf`
- `<topic_col>_accounts_graph_spring.png`
- Additional indicators/plots/parquets (information gain, comparisons, etc.)

## Batch execution (SLURM)

The repo contains papermill-based SLURM scripts:
- Translate + clustering:

  - `sbatch ../config/run_translate_and_clustering.sbatch <DATASET_FILE_NAME>`
  - Script: `../config/run_translate_and_clustering.sbatch`
  - Note: it passes only `file_name`; `dataset_name` and other parameters remain as set inside the notebook.
- Big data clustering:

  - `sbatch ../config/run_big_data_clustering.sbatch <MIN_TOPIC_SIZE>`
  - Script: `../config/run_big_data_clustering.sbatch`

See `../config/slurm_commends.md` for examples.
