"""H4 evaluation utilities for backbone sufficiency analysis.

This module evaluates whether a reduced backbone graph preserves IO detection
performance compared with the full graph.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

try:
    # Preferred import when used as part of the src/evaluation namespace package.
    from old.very_old.h3_narrative_amplification import delong_test
except ImportError:  # pragma: no cover - fallback for direct local execution.
    from old.very_old.h3_narrative_amplification import delong_test


@dataclass
class H4ModelResult:
    """Container for one model's H4 comparison output.

    Args:
        model_name: Model identifier.
        auc_full_graph: ROC-AUC on the full graph indicators.
        auc_backbone_graph: ROC-AUC on the backbone graph indicators.
        auc_delta_backbone_minus_full: Backbone AUC minus full-graph AUC.
        delong_z_score: DeLong z-score for paired ROC comparison.
        delong_p_value: DeLong two-sided p-value.
        h4_supported: Whether H4 is supported for this model.
        n_train: Number of train samples.
        n_test: Number of test samples.
    """

    model_name: str
    auc_full_graph: float
    auc_backbone_graph: float
    auc_delta_backbone_minus_full: float
    delong_z_score: float
    delong_p_value: float
    h4_supported: bool
    n_train: int
    n_test: int


def build_io_labels(index: pd.Index, io_authors_set: set[str] | set[int]) -> pd.Series:
    """Build binary IO labels from author index and IO author set.

    Args:
        index: Author/account index to label.
        io_authors_set: Set of IO author IDs.

    Returns:
        pd.Series: Binary labels (1=IO, 0=Non-IO) indexed by account.
    """
    io_authors_str_set = set(map(str, io_authors_set))
    io_labels = pd.Series(index.astype(str).isin(io_authors_str_set).astype(int), index=index, name="io_label")
    return io_labels


def align_full_and_backbone_indicators(
    full_graph_indicators_df: pd.DataFrame,
    backbone_graph_indicators_df: pd.DataFrame,
    *,
    author_universe: pd.Index | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Align full/backbone indicator matrices on the same author and feature space.

    Args:
        full_graph_indicators_df: Indicator matrix from full graph.
        backbone_graph_indicators_df: Indicator matrix from backbone graph.
        author_universe: Optional explicit author index to enforce.

    Returns:
        tuple[pd.DataFrame, pd.DataFrame]:
            Aligned full and backbone indicator matrices.
    """
    full_df = full_graph_indicators_df.copy()
    backbone_df = backbone_graph_indicators_df.copy()

    # Keep only numeric indicators to avoid model dtype issues.
    full_df = full_df.select_dtypes(include=[np.number])
    backbone_df = backbone_df.select_dtypes(include=[np.number])

    if full_df.shape[1] == 0:
        raise ValueError("full_graph_indicators_df has no numeric columns.")
    if backbone_df.shape[1] == 0:
        raise ValueError("backbone_graph_indicators_df has no numeric columns.")

    # Normalize author IDs to strings for stable matching.
    full_df.index = full_df.index.astype(str)
    backbone_df.index = backbone_df.index.astype(str)

    # Enforce one shared author universe and fill missing rows with zeros.
    if author_universe is None:
        author_universe = full_df.index
    author_universe = pd.Index(author_universe.astype(str), name=full_df.index.name)
    full_df = full_df.reindex(author_universe, fill_value=0.0)
    backbone_df = backbone_df.reindex(author_universe, fill_value=0.0)

    # Use one shared indicator set and fill missing columns with zeros.
    common_indicator_cols = sorted(set(full_df.columns) | set(backbone_df.columns))
    full_df = full_df.reindex(columns=common_indicator_cols, fill_value=0.0)
    backbone_df = backbone_df.reindex(columns=common_indicator_cols, fill_value=0.0)

    return full_df, backbone_df


def get_classifier(model_name: str, random_state: int = 42):
    """Build a classifier by model name.

    Args:
        model_name: Model name (rf/random_forest, xgb/xgboost, lr/logistic_regression).
        random_state: Random seed for reproducibility.

    Returns:
        sklearn-compatible classifier.
    """
    normalized_model_name = model_name.strip().lower()

    if normalized_model_name in ("random_forest", "rf"):
        return RandomForestClassifier(
            n_estimators=300,
            max_depth=None,
            min_samples_split=2,
            min_samples_leaf=1,
            random_state=random_state,
            n_jobs=-1,
            class_weight="balanced",
        )
    if normalized_model_name in ("xgboost", "xgb"):
        return XGBClassifier(
            n_estimators=300,
            max_depth=6,
            learning_rate=0.05,
            subsample=0.9,
            colsample_bytree=0.9,
            eval_metric="logloss",
            random_state=random_state,
        )
    if normalized_model_name in ("logistic_regression", "lr", "logistic"):
        return LogisticRegression(
            max_iter=2000,
            solver="lbfgs",
            class_weight="balanced",
            random_state=random_state,
        )

    raise ValueError(
        f"Unsupported model_name='{model_name}'. "
        "Use random_forest/rf, xgboost/xgb, or logistic_regression/lr/logistic."
    )


def _fit_and_predict_proba(
    features_df: pd.DataFrame,
    y_series: pd.Series,
    train_ids: np.ndarray,
    test_ids: np.ndarray,
    model_name: str,
    random_state: int,
) -> np.ndarray:
    """Fit a model and return predicted probabilities for one shared split.

    Args:
        features_df: Feature matrix indexed by author ID.
        y_series: Binary IO labels indexed by author ID.
        train_ids: Train author IDs.
        test_ids: Test author IDs.
        model_name: Model identifier.
        random_state: Random seed.

    Returns:
        np.ndarray: Predicted positive-class probabilities on test IDs.
    """
    X_train = features_df.loc[train_ids].to_numpy()
    X_test = features_df.loc[test_ids].to_numpy()
    y_train = y_series.loc[train_ids].to_numpy()

    # Fit on the selected graph feature set.
    clf = get_classifier(model_name=model_name, random_state=random_state)
    clf.fit(X_train, y_train)
    y_proba = clf.predict_proba(X_test)[:, 1]
    return y_proba


def run_h4_backbone_vs_full_comparison(
    full_graph_indicators_df: pd.DataFrame,
    backbone_graph_indicators_df: pd.DataFrame,
    io_authors_set: set[str] | set[int],
    *,
    model_names: tuple[str, ...] = ("random_forest", "xgboost", "logistic_regression"),
    test_size: float = 0.2,
    random_state: int = 42,
    alpha: float = 0.05,
    practical_delta_threshold: float = 0.02,
    metadata: dict | None = None,
) -> pd.DataFrame:
    """Run H4 paired AUC comparison between full and backbone graphs.

    Args:
        full_graph_indicators_df: Full-graph node indicators.
        backbone_graph_indicators_df: Backbone-graph node indicators.
        io_authors_set: Set of IO author IDs.
        model_names: Models to evaluate.
        test_size: Fraction reserved for test split.
        random_state: Random seed.
        alpha: Significance threshold for DeLong p-value.
        practical_delta_threshold: Practical comparability threshold on |AUC delta|.
        metadata: Optional metadata columns to append to each result row.

    Returns:
        pd.DataFrame: One row per model with AUCs, DeLong stats, and H4 decision.
    """
    full_df, backbone_df = align_full_and_backbone_indicators(
        full_graph_indicators_df=full_graph_indicators_df,
        backbone_graph_indicators_df=backbone_graph_indicators_df,
    )

    io_labels = build_io_labels(full_df.index, io_authors_set)
    if io_labels.nunique() < 2:
        raise ValueError("Need both IO and non-IO classes in io_labels.")

    # Use one shared train/test split to keep the DeLong comparison paired.
    all_author_ids = full_df.index.to_numpy()
    train_ids, test_ids = train_test_split(
        all_author_ids,
        test_size=test_size,
        random_state=random_state,
        stratify=io_labels.loc[all_author_ids].to_numpy(),
    )
    y_test = io_labels.loc[test_ids].to_numpy()

    result_rows = []
    for model_name in model_names:
        full_proba = _fit_and_predict_proba(
            features_df=full_df,
            y_series=io_labels,
            train_ids=train_ids,
            test_ids=test_ids,
            model_name=model_name,
            random_state=random_state,
        )
        backbone_proba = _fit_and_predict_proba(
            features_df=backbone_df,
            y_series=io_labels,
            train_ids=train_ids,
            test_ids=test_ids,
            model_name=model_name,
            random_state=random_state,
        )

        auc_full = float(roc_auc_score(y_test, full_proba))
        auc_backbone = float(roc_auc_score(y_test, backbone_proba))
        auc_delta = auc_backbone - auc_full
        delong_z_score, delong_p_value = delong_test(y_test, full_proba, backbone_proba)

        # H4 is supported when difference is statistically non-significant
        # and practically small.
        h4_supported = bool((delong_p_value >= alpha) and (abs(auc_delta) <= practical_delta_threshold))

        model_result = H4ModelResult(
            model_name=model_name,
            auc_full_graph=auc_full,
            auc_backbone_graph=auc_backbone,
            auc_delta_backbone_minus_full=auc_delta,
            delong_z_score=delong_z_score,
            delong_p_value=delong_p_value,
            h4_supported=h4_supported,
            n_train=len(train_ids),
            n_test=len(test_ids),
        )
        result_rows.append(model_result.__dict__)

    results_df = pd.DataFrame(result_rows)
    results_df["alpha"] = alpha
    results_df["practical_delta_threshold"] = practical_delta_threshold
    if metadata:
        for key, value in metadata.items():
            results_df[key] = value

    return results_df


def run_h4_grid(
    experiments: list[dict],
    io_authors_set: set[str] | set[int],
    *,
    model_names: tuple[str, ...] = ("random_forest", "xgboost", "logistic_regression"),
    test_size: float = 0.2,
    random_state: int = 42,
    alpha: float = 0.05,
    practical_delta_threshold: float = 0.02,
) -> pd.DataFrame:
    """Run H4 over a list of experiment configurations.

    Each experiment item must include:
      - `full_graph_indicators_df`
      - `backbone_graph_indicators_df`
    Any additional keys are treated as metadata and copied into output rows.

    Args:
        experiments: List of experiment configuration dictionaries.
        io_authors_set: Set of IO author IDs.
        model_names: Models to evaluate per experiment.
        test_size: Fraction reserved for test split.
        random_state: Random seed.
        alpha: Significance threshold.
        practical_delta_threshold: Practical comparability threshold.

    Returns:
        pd.DataFrame: Concatenated H4 results across all experiments.
    """
    all_results = []
    for experiment in experiments:
        full_df = experiment["full_graph_indicators_df"]
        backbone_df = experiment["backbone_graph_indicators_df"]
        metadata = {
            key: value
            for key, value in experiment.items()
            if key not in {"full_graph_indicators_df", "backbone_graph_indicators_df"}
        }

        result_df = run_h4_backbone_vs_full_comparison(
            full_graph_indicators_df=full_df,
            backbone_graph_indicators_df=backbone_df,
            io_authors_set=io_authors_set,
            model_names=model_names,
            test_size=test_size,
            random_state=random_state,
            alpha=alpha,
            practical_delta_threshold=practical_delta_threshold,
            metadata=metadata,
        )
        all_results.append(result_df)

    if not all_results:
        return pd.DataFrame()
    return pd.concat(all_results, ignore_index=True)


def merge_h4_with_grid_results(
    grid_df: pd.DataFrame,
    h4_results_df: pd.DataFrame,
    *,
    grid_merge_keys: tuple[str, ...] = ("topic_col", "top_percentage", "key_authors_mode", "is_directed_graphs"),
    target_model_name: str = "xgboost",
) -> pd.DataFrame:
    """Merge H4 metrics into an existing parameter-sweep grid output.

    Args:
        grid_df: Existing parameter-sweep DataFrame.
        h4_results_df: H4 results (one row per model per configuration).
        grid_merge_keys: Keys used to join H4 and grid outputs.
        target_model_name: Model row from h4_results_df to merge into grid_df.

    Returns:
        pd.DataFrame: Grid DataFrame with H4 columns appended.
    """
    if h4_results_df.empty:
        return grid_df.copy()

    filtered_h4_df = h4_results_df[h4_results_df["model_name"] == target_model_name].copy()
    if filtered_h4_df.empty:
        raise ValueError(f"No H4 rows found for model '{target_model_name}'.")

    required_h4_cols = list(grid_merge_keys) + [
        "auc_full_graph",
        "auc_backbone_graph",
        "auc_delta_backbone_minus_full",
        "delong_z_score",
        "delong_p_value",
        "h4_supported",
    ]
    missing_h4_cols = [col for col in required_h4_cols if col not in filtered_h4_df.columns]
    if missing_h4_cols:
        raise KeyError(f"Missing H4 merge columns: {missing_h4_cols}")

    merged_df = grid_df.merge(
        filtered_h4_df[required_h4_cols],
        on=list(grid_merge_keys),
        how="left",
        validate="many_to_one",
    )
    return merged_df


def save_h4_artifacts(
    h4_results_df: pd.DataFrame,
    output_folder_path: str | Path,
    *,
    parquet_filename: str = "h4_backbone_vs_full_results.parquet",
    summary_filename: str = "h4_backbone_vs_full_summary.txt",
    plot_filename: str = "h4_backbone_vs_full_auc_plot.png",
) -> None:
    """Save H4 result parquet, text summary, and AUC comparison plot.

    Args:
        h4_results_df: H4 result rows.
        output_folder_path: Folder for saved artifacts.
        parquet_filename: Output parquet file name.
        summary_filename: Output text summary file name.
        plot_filename: Output plot file name.
    """
    output_dir = Path(output_folder_path)
    output_dir.mkdir(parents=True, exist_ok=True)

    h4_results_df.to_parquet(output_dir / parquet_filename, compression="gzip", index=False)

    if h4_results_df.empty:
        (output_dir / summary_filename).write_text("No H4 results were produced.\n", encoding="utf-8")
        return

    support_rate = float(h4_results_df["h4_supported"].mean())
    summary_lines = [
        "H4 Backbone Sufficiency Evaluation",
        "=================================",
        f"Number of model comparisons: {len(h4_results_df):,}",
        f"H4 supported rate: {support_rate:.1%}",
        "",
    ]
    for _, row in h4_results_df.iterrows():
        summary_lines.extend(
            [
                f"Model: {row['model_name']}",
                f"  AUC(full): {row['auc_full_graph']:.6f}",
                f"  AUC(backbone): {row['auc_backbone_graph']:.6f}",
                f"  Delta(backbone-full): {row['auc_delta_backbone_minus_full']:.6f}",
                f"  DeLong z: {row['delong_z_score']:.6f}",
                f"  DeLong p: {row['delong_p_value']:.6g}",
                f"  H4 supported: {bool(row['h4_supported'])}",
            ]
        )
    (output_dir / summary_filename).write_text("\n".join(summary_lines) + "\n", encoding="utf-8")

    # Plot AUC(full) vs AUC(backbone) by model.
    fig, ax = plt.subplots(figsize=(7, 5))
    x = h4_results_df["auc_full_graph"].to_numpy()
    y = h4_results_df["auc_backbone_graph"].to_numpy()
    ax.scatter(x, y, s=80, alpha=0.8)
    for _, row in h4_results_df.iterrows():
        ax.annotate(str(row["model_name"]), (row["auc_full_graph"], row["auc_backbone_graph"]), fontsize=9)
    line_min = float(min(x.min(), y.min()))
    line_max = float(max(x.max(), y.max()))
    ax.plot([line_min, line_max], [line_min, line_max], linestyle="--", linewidth=1.0)
    ax.set_xlabel("AUC (full graph)")
    ax.set_ylabel("AUC (backbone graph)")
    ax.set_title("H4: Full vs Backbone AUC")
    fig.tight_layout()
    fig.savefig(output_dir / plot_filename, dpi=300)
    plt.close(fig)
