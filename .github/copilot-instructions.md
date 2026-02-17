# Backbone-Graph: Copilot Instructions

## Big picture
- Goal: build topic-specific **author graphs** for discourse / IO analysis. Nodes are authors; edges represent behavioral similarity signals.
- Core workflow is notebook-driven in [src/](../src/) and produces PNG + Parquet artifacts + GEXF graphs for Gephi.

## Where to run + data layout
- Run notebooks from [src/](../src/) (matches [src/README_src.md](../src/README_src.md)). Many paths assume `../results/` relative to `src/`.
- Inputs are Parquet files under [data/Labeled_Datasets/](../data/Labeled_Datasets/) (e.g. `Ecuador_part_1.gzip.parquet`).
- Outputs go under `../results/Labeled_Datasets/<Country>/<FileStem>/YYYY_MM_DD/` (sometimes `../final_results/`).

## Environment
- Conda env: `backbone_env` in [config/conda_requirements.yml](../config/conda_requirements.yml) (Python 3.12; pip installs BERTopic + transformers).
- Setup: `conda env create -f config/conda_requirements.yml` then `conda activate backbone_env`.

## Notebook pipeline (execution order)
1) [src/translate_and_clustering.ipynb](../src/translate_and_clustering.ipynb)
   - Set near the top: `dataset_name`, `file_name`, `min_topic_size`.
   - Produces `Topic_Ner_<file_name>` and `processed_<file_name>` plus reports/plots.
2) If clustering OOM: [src/big_data_clustering.ipynb](../src/big_data_clustering.ipynb)
   - Set: `dataset_name`, `raw_file_name`, `min_topic_size` → creates `BERTopic_topic_<min_topic_size>` column.
3) Graph + key authors: [src/key_authors_graph.ipynb](../src/key_authors_graph.ipynb)
   - Set: `file_name`, `account_id_col` (default `accountid`), `topic_col` (e.g. `BERTopic_topic_512`), `top_n`.
   - Exports `author_topic_tfidf_by_<topic_col>.parquet`, `io_key_authors_summary.txt`, `<topic_col>_accounts_graph.gexf`.

## Graph conventions (from the notebooks)
- Key authors are selected per-topic via TF‑IDF with a `top_n` cutoff.
- Directed edges use canonical author id `accountid` and interaction columns like `in_reply_to_accountid`, `account_mentions`, `reposted_accountid`.

## SLURM (papermill)
- Run from [src/](../src/):
  - `sbatch ../config/run_translate_and_clustering.sbatch <DATASET_FILE_NAME>` (passes papermill param `file_name`).
  - `sbatch ../config/run_big_data_clustering.sbatch <MIN_TOPIC_SIZE>` (passes papermill param `min_topic_size`).
- More examples in [config/slurm_commends.md](../config/slurm_commends.md).

## Experimental / prototypes
- Neo4j adapters: [src/neo4j/adapters/](../src/neo4j/adapters/).
- Entity reuse + time-window edge logic: [src/drafts/Key_Authors.ipynb](../src/drafts/Key_Authors.ipynb) (not guaranteed to run end-to-end).
