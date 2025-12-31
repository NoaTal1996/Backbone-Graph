# Backbone-Graph Copilot Instructions

## Project Overview
This project analyzes information flow in social media topics by building directed graphs where nodes represent key authors (identified via TF-IDF) and edges represent influence through hashtag/mention reuse within time windows. Core architecture uses NetworkX for graph construction and analysis, with data stored in Parquet format and results exported as GEXF files for visualization tools like Gephi.

## Key Architecture Components
- **Data Flow**: Raw social media data → Parquet files in `data/Labeled_Datasets/` → Notebook processing → Graph analysis → GEXF exports in `results/Labeled_Datasets/`
- **Graph Model**: Nodes have properties like `username`, `tfidf_score`, `hashtags` (JSON), `mentions` (JSON); Edges have `shared_entity_count`, `shared_hashtags`, `shared_mentions`
- **Filtering**: Key authors only (high TF-IDF), entity reuse within min/max time bounds, entities below threshold frequency
- **Adapters**: Neo4j adapters exist in `neo4j/adapters/` but are not fully integrated; current implementation uses in-memory NetworkX graphs

## Developer Workflows
- **Local Development**: Run Jupyter notebooks in `src/` (e.g., `key_authors_graph.ipynb`) with parameters like `dataset_name = "Labeled_Datasets/Ecuador"`, `file_name = "Ecuador_part_1.gzip.parquet"`
- **Batch Execution**: Use SLURM via `src/config/run_notebook.sbatch` with `sbatch run_notebook.sbatch <DATASET_FILE_NAME>`; executes notebooks with Papermill in `backbone_env` conda environment
- **Environment Setup**: `conda env create -f src/config/requirements/conda_requirements.yml` then `conda activate backbone_env`; additional pip installs from `src/config/requirements/requirements.txt`
- **Data Processing**: Load Parquet with `pd.read_parquet()`, compute TF-IDF using `TfidfVectorizer`, build graphs with `nx.DiGraph()`, export with `nx.write_gexf()`

## Project Conventions
- **Dataset Naming**: `{Country}_part_{number}.gzip.parquet` (e.g., `Ecuador_part_1.gzip.parquet`)
- **Date Formatting**: `YYYY_MM_DD` for processed dates (e.g., `2025_12_16`)
- **Output Structure**: Results in `results/Labeled_Datasets/{Country}/{part}/YYYY_MM_DD/` with `dataset_summary.txt`, `accounts_graph.gexf`, `io_key_authors_summary.txt`
- **Code Style**: Notebooks for exploratory analysis, modular functions for reusable logic; avoid hardcoding paths, use `Path` for file handling
- **Graph Construction**: Always filter entities by frequency threshold, apply time window constraints, use directed edges for temporal influence

## Integration Points
- **Visualization**: Export graphs to GEXF for Gephi analysis; summaries in TXT for quick insights
- **Dependencies**: Core: pandas, networkx, scikit-learn; NLP: spacy, nltk, sentence-transformers; HPC: papermill for parameterized execution
- **External Services**: Neo4j for potential persistence (drafts in `src/drafts/Key_Authors.ipynb`), but not required for core analysis

## Common Patterns
- **Key Author Selection**: `tfidf_scores = vectorizer.fit_transform(corpus); top_authors = scores.argsort()[-k:]`
- **Entity Reuse Edges**: For each author pair, check shared hashtags/mentions within time window; create edge if count > 0
- **Time Filtering**: Use pandas datetime for min/max bounds: `df[(df['timestamp'] > start) & (df['timestamp'] < end)]`
- **JSON Properties**: Store entity counts as `json.dumps({"#tag": count})` in node properties

Reference: `docs/Information_Flow_Graph_Design.md` for detailed schema, `src/key_authors_graph.ipynb` for implementation example.</content>
<parameter name="filePath">/home/amitner/Backbone-Graph/.github/copilot-instructions.md