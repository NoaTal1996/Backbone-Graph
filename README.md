# Backbone-Graph

A framework for social media graph representation used for social platform discourse analysis and IO (information operation) detection, where edges represent behavioural similarity through entity usage patterns, using TF-IDF scoring.


## Core Idea

Social media users exhibit behavioral patterns through their use of entities (hashtags, mentions). This project constructs **graphs** where:
- **Nodes** represent authors
- **Edges** indicate behavioral similarity based on shared entity usage

The graph representation is used for social platform discourse analysis and more IO detection, enabling analysis of user communities and behavioral clusters through graph-based measures.

## Key Concepts

- **Goal**: Accurate identification of IO (information operation) authors
- **Focus**: Relationships and interactions between authors
- **Analysis Scope**: Narrow analysis to key authors only
- **Detection**: Identify abnormal coordinated behavioral patterns

## Project Structure

```
Backbone-Graph/
├── data/                               # Datasets (Parquet format)
├── docs/                               # Design documentation
├── neo4j/                              # Graph database adapters
├── src/                                # Core notebooks & scripts
|   ├── Topic_Clustring_and_NER.ipynb   # Preprocessing, Topic clustering, NER
│   ├── key_authors_graph.ipynb         # Graph construction
│   ├── config/                         # SLURM commends and environments requirements
│   └── Evaluation/                     
└── results/                            
```



## Quick Start

1. **Environment**: `conda env create -f config/requirements/conda_requirements.yml`
2. **Process Data**: Run `src/Topic_Clustring_and_NER.ipynb` with your dataset parameters
3. **Graph Building**: Run `src/key_authors_graph.ipynb`


## Output

- **Data Statistics**
- **Author level IO centereleties indicators**
- **GEXF Files**: Graph exports compatible with Gephi
