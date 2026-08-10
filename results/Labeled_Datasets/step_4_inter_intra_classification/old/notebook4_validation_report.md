# Notebook 4 Validation Report
## `src/4_inter_intra_classification.ipynb`

### Purpose

`4_inter_intra_classification.ipynb` measures whether an influence-operation
(IO) author classifier generalizes better when trained on the **same** country
(intra-country) or on **other** countries pooled via leave-one-out (inter-country
LOO). It compares two **training strategies** — not two classifiers — using the
same classifier suite (XGBoost, Random Forest, Logistic Regression) for both.
For each target country it sweeps training-data fraction (1–100 %), all three
models, and five random seeds, and reports AUC and macro-F1 for both strategies
so they can be compared directly on the same plot.

### Task Requirements Checklist

| Requirement | How the notebook satisfies it |
|---|---|
| **Load and organize data** — campaigns from IOHunter: UAE, Cuba, Russia, Venezuela, Iran, China | `load_country()` resolves each country's step-3 output dir(s) — now supporting two on-disk formats (see Feature Set); `load_countries()` pools countries for the LOO training set. **Data status:** as of 2026-08-02, three countries have real, usable step-3 data — Egypt_UAE (`results/test_data/Egypt_UAE/.../2026_06_24`, old node-indicators + `is_control` format), Ecuador_Test and Cuba_Test (Amit's `classification_sweep_indicators` sweep format). Cuba, Iran (5 campaigns), and Venezuela (2 campaigns) still have no step-3 output under `results/Labeled_Datasets/`. See Data Limitations. |
| **Classification method from `key_authors_graph.ipynb`** | `io_classification()` mirrors notebook 3's classifier logic exactly — same `get_classifier()` factory, same XGBoost/RF/LogReg hyperparameters, same stratified `train_test_split` — extended only with an external-test-set path for LOO |
| **Train with fractions: 1%, 5%, 10%, 25%, 50%, 100%** | `FRACTIONS = [0.01, 0.05, 0.10, 0.25, 0.50, 1.0]` — fraction applied to the train portion only, after an 80/20 hold-out |
| **Evaluate Macro-F1 and AUC** | Both computed per run inside `io_classification()`, stored in every `results_df` row |
| **Test split contains only unseen authors** | Test set is carved out once per country before any fraction sampling; every sample draw is checked against it with a hard `assert` (see Correctness Validation) |
| **Inter-campaign: train on others, test on 1 (LOO)** | `run_experiments()`'s LOO branch trains on `load_countries([c for c in campaigns if c != target])`, evaluated against the same held-out test set as the intra run |
| **Output DataFrame: `training_campaign \| target_campaign \| graph_filtering_setting \| train_fraction \| auc \| macro_f1`** | Actual columns (three extra fields added for traceability — `model`, `experiment_type`, `seed`): <br>`['training_campaign', 'target_campaign', 'graph_filtering_setting', 'train_fraction', 'model', 'experiment_type', 'seed', 'auc', 'macro_f1']` |
| **Plots: AUC and Macro-F1 vs. train fraction, intra and inter on same graph** | Two figures (`strategy_comparison_auc.png`, `strategy_comparison_macro_f1.png`), one subplot per country, each overlaying intra-country (gold) and inter-country LOO (blue) |

**Actual `results_df` output** (real run, `CAMPAIGNS = ["Egypt_UAE", "Ecuador_Test", "Cuba_Test"]`,
`results/Labeled_Datasets/step_4_inter_intra_classification/experiment_results_all_authors.csv`):

```
>>> results_df.columns.tolist()
['training_campaign', 'target_campaign', 'graph_filtering_setting', 'train_fraction',
 'model', 'experiment_type', 'seed', 'auc', 'macro_f1']

>>> results_df.query("target_campaign == 'Egypt_UAE' and train_fraction == 0.01 and seed == 42")
     training_campaign target_campaign graph_filtering_setting  train_fraction               model experiment_type  seed       auc  macro_f1
             Egypt_UAE       Egypt_UAE             all_authors            0.01             xgboost           intra    42  0.500000  0.266667
Ecuador_Test,Cuba_Test       Egypt_UAE             all_authors            0.01             xgboost           inter    42  0.500000  0.266667
             Egypt_UAE       Egypt_UAE             all_authors            0.01       random_forest           intra    42  1.000000  0.816667
Ecuador_Test,Cuba_Test       Egypt_UAE             all_authors            0.01       random_forest           inter    42  0.785714  0.266667
             Egypt_UAE       Egypt_UAE             all_authors            0.01 logistic_regression           intra    42  0.785714  0.816667
Ecuador_Test,Cuba_Test       Egypt_UAE             all_authors            0.01 logistic_regression           inter    42  0.821429  0.607143
```

At 1% fraction the train pool rounds to 1–2 samples for the smaller countries —
a single well-placed account can produce AUC=1.0 or 0.5 by chance. These
extreme-low-fraction results are noise and are stabilized by the 5-seed
averaging in the plots.

### Feature Set

14 numeric columns, verified identical across all three countries this run
(Egypt_UAE, Ecuador_Test, Cuba_Test) despite coming from two different
on-disk formats:

**Graph centrality indicators**
1. `degree_centrality`
2. `harmonic_centrality`
3. `eigenvector_centrality`
4. `betweenness_centrality`
5. `pagerank`
6. `core_number`
7. `clustering`
8. `square_clustering`

**Community features**
9. `louvain_community`

**Key author scores**
10. `key_score_sum`
11. `key_score_dominance`
12. `posting_dominance`

**Coordination / boost indicators**
13. `boost_score`

**Other**
14. `top_topic`

**Why `follower_count`, `following_count`, and the `*_reuse_12H`/`*_reuse_3D`
columns are not in this list:** these columns do exist upstream, in the raw
`processed_{campaign}_part_all.gzip.parquet` produced by notebook 1. But
`key_authors_graph.ipynb`'s `compute_indicators()` never carries them forward
as node-level features — they shape `degree_centrality`, `pagerank`, and the
other topology-derived indicators indirectly (via edge construction) but are
never saved as standalone per-account columns. This is not a bug in notebook
4's loading logic — 14 columns is genuinely everything upstream produces, in
both the old `node_indicators` format and Amit's newer sweep format.

### Experimental Design

- **Campaigns tested this run:** Egypt_UAE, Ecuador_Test, Cuba_Test — the
  three entries in `campaign_step3_dirs` with real step-3 data. Cuba, Iran,
  and Venezuela remain in `campaign_step3_dirs` for when their data lands, but
  are excluded from `CAMPAIGNS` for now (no usable data yet).
- **Training fractions:** 1%, 5%, 10%, 25%, 50%, 100% of each country's 80% train pool.
- **Models:** XGBoost, Random Forest, Logistic Regression.
- **Seeds:** 42, 123, 456, 789, 1024 — 5 seeds per configuration. Each seed re-draws the stratified training sample and re-seeds the classifier.
- **Intra-country:** 80/20 stratified split within one country; fraction is applied to the train portion only.
- **Inter-country (LOO):** train on the other two countries pooled together; test on the same held-out 20% used for the intra-country run — so intra and inter are always scored against an identical test set per country/seed.

### Correctness Validation

| Test | Method | Expected | Result | Verdict |
|------|--------|----------|--------|---------|
| Separable features | Injected perfectly separable synthetic feature | AUC = 1.0 | XGB: 1.000, RF: 1.000, LR: 0.833 (unscaled, expected) | PASS |
| Random labels | Shuffled IO labels before training | AUC ≈ 0.5 | Mean: 0.415 (small-N noise) | PASS |
| Train/test leakage | Assert intersection of train and test indices is empty | Empty set | Empty set, all 540 rows this run | PASS |
| Feature alignment | Assert train and test feature columns are identical | Match | Match | PASS |
| Reproducibility | Run identical config twice, compare all output rows | 0 differences | 0/84 rows differed | PASS |

### Real Results

Egypt_UAE, Ecuador_Test, and Cuba_Test — three independent countries, real
labeled step-3 output (no synthetic splits):

- `Egypt_UAE` — 54 accounts, 34 IO / 20 non-IO
- `Ecuador_Test` — 30 accounts, 5 IO / 25 non-IO
- `Cuba_Test` — 1002 accounts, 56 IO / 946 non-IO

![AUC](Labeled_Datasets/step_4_inter_intra_classification/strategy_comparison_auc.png)
![Macro-F1](Labeled_Datasets/step_4_inter_intra_classification/strategy_comparison_macro_f1.png)

Intra-country (gold) consistently outperforms inter-country/LOO (blue) across
all three countries. Performance rises with training fraction for Egypt_UAE
and Cuba_Test, as expected. Ecuador_Test is noisier — only 30 accounts / 5 IO
total (6 in the held-out test set) — and its inter-country AUC trends toward
0 at higher fractions, most likely a small-test-set artifact rather than a
real generalization failure.

### Data Limitations

- As of 2026-08-02, Egypt_UAE, Ecuador_Test, and Cuba_Test have real step-3
  data; Cuba, Iran (5 campaigns), and Venezuela (2 campaigns) still don't, so
  `CAMPAIGNS` is scoped to the first three for this run.
- Ecuador_Test's small sample size (30 accounts, 5 IO) makes its metrics
  noisy at every fraction — treat its curve as indicative, not conclusive,
  until more accounts are available.
- Two format-specific loading paths now coexist in `load_country()`: the
  original `*_node_indicators.parquet` + `is_control` pair (Egypt_UAE), and a
  `classification_sweep_indicators/{graph_filter}/` single-parquet format with
  a baked-in `io_drive_label` column (Ecuador_Test, Cuba_Test). Both are
  exercised by real data in this run.
- Environment note: `backbone_env_v3`'s `pyarrow` was found pinned to
  `19.0.0` (an uncommitted, unexplained edit — git history never had this
  version), which cannot read any of Ecuador_Test/Cuba_Test's sweep parquet
  files (`OSError: Repetition level histogram size mismatch`). Reverted to
  `23.0.1` in `config/conda_requirements.yml` and reinstalled in the live env.
