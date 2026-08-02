# Classification Sweep Patterns: Armenia and Iran_1

## Material Passport

- Origin Skill: academic-research-suite / experiment-agent
- Origin Mode: validate
- Origin Date: 2026-08-02
- Verification Status: ANALYZED
- Version Label: classification_sweep_comparison_v1

## Executive summary

The comparison reveals five meaningful patterns:

1. **Performance depends strongly on the evaluation population.** Small `top_percentage` values tend to maximize classification among `graph_authors`, whereas larger values strongly improve performance on `all_authors`. This is especially pronounced for Iran_1.
2. **Similarity-based relations provide a large all-author gain over interactions alone, but are much more expensive.** The median runtime multiplier is about 106x in Armenia and 141x in Iran_1.
3. **Combining interactions with similarity rarely helps.** Across paired configurations, adding interactions to an existing similarity relation produces changes near zero and is more often negative than positive.
4. **Betweenness and harmonic centrality appear dispensable in these sweeps.** Removing both has essentially no median effect in either dataset. Core number alone, however, is inadequate for Armenia and slightly but consistently weaker for Iran_1.
5. **Iran_1 is substantially easier to classify than Armenia under matched configurations.** This difference is descriptive, not evidence that the underlying country-level phenomenon is intrinsically easier: sample size, label balance, graph coverage, and split composition may differ.

## Sources and method

This analysis uses the two generated reports:

- [Armenia classification sweep](../results/Labeled_Datasets/Armenia/Armenia_part_all/step_3_key_authors_graph/topic_col_BERTopic_topic_256_top_percentage_1/classification_sweep_results.md)
- [Iran_1 classification sweep](../results/Labeled_Datasets/Iran_1/Iran_1_part_all/step_3_key_authors_graph/topic_col_BERTopic_topic_256_top_percentage_1/classification_sweep_results.md)

The Armenia report contains 1,200 configurations and the Iran_1 report contains 1,260. Comparisons described as *paired* hold topic method, `top_percentage`, relation configuration, indicator configuration, and model fixed except for the factor being compared. A descriptive composite score—the unweighted mean of ROC-AUC, F1, and AUC-PR—is used only to summarize multidimensional performance. It is not an additional model metric.

No confidence intervals, cross-validation variation, per-split results, class prevalence, or independent final-test evaluation are reported. Consequently, small score differences should not be treated as statistically significant.

## 1. Graph-author performance and all-author generalization diverge

Increasing `top_percentage` from 0.01 to 1.0 has opposite effects on the two evaluation populations.

| Dataset | Evaluation population | Median paired composite change, 0.01 to 1.0 | Configurations improved |
|---|---:|---:|---:|
| Armenia | `graph_authors` | -0.060 | 7.7% |
| Armenia | `all_authors` | +0.106 | 70.2% |
| Iran_1 | `graph_authors` | -0.006 | 4.3% |
| Iran_1 | `all_authors` | +0.404 | 99.0% |

The median all-author metrics by `top_percentage` make this coverage effect particularly clear:

| Dataset | `top_percentage` | ROC-AUC | F1 | AUC-PR |
|---|---:|---:|---:|---:|
| Armenia | 0.01 | 0.719 | 0.368 | 0.260 |
| Armenia | 0.50 | 0.863 | 0.591 | 0.558 |
| Armenia | 1.00 | 0.936 | 0.724 | 0.760 |
| Iran_1 | 0.01 | 0.710 | 0.511 | 0.462 |
| Iran_1 | 0.50 | 0.988 | 0.960 | 0.958 |
| Iran_1 | 1.00 | 0.994 | 0.978 | 0.989 |

Interpretation: selecting a small graph can produce an easily classified, highly distinctive subset, but the resulting model does not transfer as well to all authors. Broader graph coverage sacrifices little—or some—performance inside the selected graph while greatly improving population coverage. Therefore, `graph_authors` results should not be used as a proxy for all-author performance.

## 2. Similarity relations improve coverage at a large runtime cost

Relative to `interactions`, plain `similarity` improves the all-author composite score in 89.7% of paired Armenia configurations and 100% of paired Iran_1 configurations.

| Dataset | Median graph composite gain | Median all-author composite gain | Median runtime multiplier |
|---|---:|---:|---:|
| Armenia | +0.017 | +0.140 | 106x |
| Iran_1 | +0.036 | +0.154 | 141x |

The median absolute runtimes show the practical scale of this tradeoff:

| Dataset | Interactions | Similarity | Text similarity |
|---|---:|---:|---:|
| Armenia | 1.0 s | 75.3 s | 103.9 s |
| Iran_1 | 17.8 s | 2,839.0 s | 2,729.7 s |

Text similarity is only marginally better than similarity. Its median paired all-author composite gain is +0.0012 for Armenia and +0.0004 for Iran_1. Without uncertainty estimates, these differences are too small to support a claim that one similarity method is reliably superior.

Interactions alone may still be useful when speed matters, but their best observed all-author composite scores are only 0.702 in Armenia and 0.829 in Iran_1, well below the best similarity-based results.

## 3. Extra relation channels add complexity without a stable gain

Adding interactions to an existing relation representation does not consistently improve performance.

| Added relation | Dataset | Median graph composite change | Median all-author composite change | All-author win rate |
|---|---|---:|---:|---:|
| `similarity` + interactions | Armenia | -0.0010 | -0.0004 | 35.6% |
| `text_similarity` + interactions | Armenia | -0.0033 | -0.0012 | 22.0% |
| `similarity+text_similarity` + interactions | Armenia | -0.0022 | -0.0013 | 32.8% |
| `similarity` + interactions | Iran_1 | -0.0001 | +0.0000 | 53.9% |
| `text_similarity` + interactions | Iran_1 | -0.0001 | -0.0001 | 35.0% |
| `similarity+text_similarity` + interactions | Iran_1 | -0.0000 | +0.0000 | 52.8% |

These differences are practically negligible in Iran_1 and slightly unfavorable in Armenia. The simplest single similarity channel therefore captures nearly all observed benefit.

## 4. Indicator ablations reveal a country-specific dependence

Removing betweenness and harmonic centrality has almost no effect while retaining the remaining indicators:

| Dataset | Median graph composite change | Median all-author composite change |
|---|---:|---:|
| Armenia | -0.0022 | -0.0001 |
| Iran_1 | -0.0000 | +0.0000 |

By contrast, using `Core Number Only` has very different consequences:

| Dataset | Median graph composite change vs. `All` | Median all-author composite change vs. `All` | Core-only wins |
|---|---:|---:|---:|
| Armenia | -0.526 | -0.448 | 0.0% graph; 0.2% all |
| Iran_1 | -0.016 | -0.015 | 0.0% graph; 0.0% all |

Core number alone is therefore not a safe cross-dataset representation. It is catastrophic for a typical Armenia configuration, but only modestly worse in a typical Iran_1 configuration. This suggests that Iran_1's labels align strongly with a coarse core-periphery structure, whereas Armenia requires information from additional indicators. This structural explanation is an inference and should be checked with feature importance or controlled ablations.

The reported `indicators_runtime_seconds` is identical across indicator subsets within a relation configuration. Thus, the current sweep does **not** demonstrate a runtime saving from dropping betweenness and harmonic centrality; those features appear to have been computed before the classifier-level ablation. A speed claim would require rerunning indicator construction without them.

## 5. Topic granularity affects transfer more than selected-node classification

For BERTopic, coarser topic representations generally perform better on all authors. Median values across the full sweep are:

| Dataset | BERTopic count | Graph ROC-AUC | All-author ROC-AUC | All-author F1 |
|---|---:|---:|---:|---:|
| Armenia | 10 | 0.932 | 0.927 | 0.717 |
| Armenia | 128 | 0.947 | 0.797 | 0.622 |
| Armenia | 256 | 0.913 | 0.647 | 0.368 |
| Armenia | 512 | 0.841 | 0.629 | 0.000 |
| Iran_1 | 10 | 0.994 | 0.974 | 0.947 |
| Iran_1 | 128 | 0.995 | 0.945 | 0.870 |
| Iran_1 | 256 | 0.996 | 0.890 | 0.785 |
| Iran_1 | 512 | 0.997 | 0.780 | 0.598 |

Iran_1 graph-author ROC-AUC remains almost unchanged as the number of topics grows, even while all-author performance declines sharply. Armenia shows an even stronger failure of the 512-topic representation. This reinforces the conclusion that excellent performance on selected graph authors can conceal weak generalization.

These topic-level medians partly mix differences in graph density and relation runtime, and Armenia's 512-topic sweep is incomplete. They are descriptive rather than isolated causal effects of topic count.

## 6. Model choice is secondary to graph construction

Random forest is more reliable for Armenia: XGBoost's median paired composite difference is -0.0096 for graph authors and -0.0075 for all authors, and XGBoost wins only 25.3% and 24.2% of configurations, respectively.

In Iran_1, model differences are negligible. XGBoost has a median +0.0006 graph composite advantage and wins 63.0% of graph comparisons, while its median all-author difference is -0.0002 and it wins 44.0%. Relation type, coverage, and indicator set matter much more than the choice between these two classifiers.

## Best observed balanced configurations

The following rows maximize the descriptive mean of ROC-AUC, F1, and AUC-PR. Because they were selected from 1,200 or more tested configurations, they should be treated as candidates for confirmation, not unbiased final estimates.

| Dataset / scope | Configuration | ROC-AUC | F1 | AUC-PR | Recall | Precision | Runtime |
|---|---|---:|---:|---:|---:|---:|---:|
| Armenia / graph | BERTopic 256; 0.01; interactions; All; random forest | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.56 s |
| Armenia / all | BERTopic 128; 1.00; text similarity; All; random forest | 0.958 | 0.808 | 0.842 | 0.677 | 1.000 | 229.94 s |
| Iran_1 / graph | BERTopic 512; 0.01; text similarity + interactions; no betweenness/harmonic; XGBoost | 0.998 | 0.996 | 0.997 | 0.992 | 1.000 | 10.74 s |
| Iran_1 / all | K-means 128; 1.00; text similarity; no betweenness/harmonic; XGBoost | 0.997 | 0.984 | 0.992 | 0.971 | 0.997 | 7,706.66 s |

The perfect Armenia graph result is not unique: 21 configurations at BERTopic 256 and `top_percentage=0.01` achieve ROC-AUC = F1 = AUC-PR = 1.0. Such broad perfection across ablations is a reason to inspect graph-subset size, class counts, split construction, duplicate authors, and potential feature leakage before interpreting it as robust performance.

## Cross-country comparison

There are 948 exactly matched configurations across the two reports. Iran_1 outperforms Armenia in 96.9% of matched graph-author comparisons and 99.8% of matched all-author comparisons. The median Iran_1 minus Armenia composite difference is +0.188 for graph authors and +0.287 for all authors.

This is a stable descriptive difference, but it is not yet an explanatory result. A valid explanation requires comparable class prevalence, numbers of authors, train/test procedures, label noise, graph connectivity, and evaluation sample sizes. In particular, higher performance can reflect an easier or more homogeneous dataset rather than a better graph method.

## Data-quality and validation cautions

- **Incomplete grid:** Armenia has no BERTopic-512 rows at `top_percentage=0.01`; at 0.05 it lacks `interactions`; at 0.10 it lacks both text-similarity variants. Iran_1 contains the complete 1,260-row grid. Aggregate Armenia medians are therefore not perfectly balanced.
- **Many-model selection:** Reporting the maximum from 1,200–1,260 configurations creates a look-elsewhere/selection effect. Use a locked configuration and untouched test set, or nested cross-validation, to confirm the apparent winners.
- **No uncertainty:** Point estimates alone cannot establish whether small differences are reproducible. Per-fold metrics, confidence intervals, and repeated seeds are needed.
- **Unknown class baseline:** AUC-PR is included, which is appropriate for imbalance, but the positive-class prevalence is absent. The magnitude of AUC-PR cannot be judged against its random baseline.
- **Threshold dependence:** F1, recall, and precision depend on the chosen classification threshold. The report does not state whether that threshold was fixed or tuned on held-out data.
- **Potential selection bias:** `graph_authors` are a selected subset. The large graph/all gap shows that conclusions about this subset do not automatically extend to all authors.

## Statistical fallacy scan

Coverage: **11/11 types checked**. The reports support descriptive validation only.

| Fallacy | Status | Assessment |
|---|---|---|
| Simpson's paradox | Not assessable | No subgroup-level metrics are provided. |
| Ecological fallacy | Avoided here | No individual-level claim is inferred from a country aggregate. |
| Berkson's paradox | Caution | Restricting evaluation to graph authors is a selection mechanism and may induce atypical associations. |
| Collider bias | Not assessable | The feature-generation and selection causal structure is not documented. |
| Base-rate neglect | Caution | Class prevalence and the AUC-PR baseline are missing. |
| Regression to the mean | Not applicable | The reports do not describe an extreme-group pre/post design. |
| Survivorship bias | Caution | Graph membership acts like inclusion filtering; excluded authors perform differently. |
| Look-elsewhere effect | Caution | More than 1,000 configurations are searched and maxima are reported. |
| Garden of forking paths | Caution | There are many modeling choices and no nested selection or independent confirmation is shown. |
| Correlation implies causation | Avoided here | The analysis makes no causal performance claim. |
| Reverse causality | Not applicable | No directional causal relationship is asserted. |

## Practical conclusions

- Evaluate and select configurations using `all_authors` metrics when population-wide classification is the goal.
- Start confirmation runs with one similarity channel; extra interaction channels are not justified by the observed point estimates.
- Retain the full indicator set or remove only betweenness and harmonic centrality. Do not rely on core number alone across datasets.
- Prefer random forest as the Armenia baseline. Treat random forest and XGBoost as effectively tied for Iran_1 until repeated-run uncertainty is available.
- Confirm one or two candidate configurations on an untouched test set before treating the reported maxima as final performance.
