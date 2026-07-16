"""H3 evaluation utilities for narrative amplification analysis.

This module evaluates whether adding key-score features improves IO
classification beyond baseline node indicators.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier


DEFAULT_KEY_SCORE_COLUMNS = ("key_score_sum", "key_score_dominance", "top_topic")


@dataclass
class H3EvaluationResult:
    """Container for H3 model comparison outputs.

    Args:
        baseline_auc: ROC-AUC score for baseline model.
        augmented_auc: ROC-AUC score for model with key-score features.
        auc_delta: Augmented AUC minus baseline AUC.
        delong_p_value: Two-sided p-value from DeLong test.
        delong_z_score: Z score from DeLong test.
        n_train: Number of train samples.
        n_test: Number of test samples.
    """

    baseline_auc: float
    augmented_auc: float
    auc_delta: float
    delong_p_value: float
    delong_z_score: float
    n_train: int
    n_test: int


def _prepare_feature_matrix(
    features_df: pd.DataFrame,
    *,
    categorical_cols: list[str] | None = None,
) -> pd.DataFrame:
    """Prepare a model-ready feature matrix with stable dtypes.

    Args:
        features_df: Input feature DataFrame indexed by account ID.
        categorical_cols: Optional list of columns to one-hot encode.

    Returns:
        pd.DataFrame: Prepared feature matrix with numeric dtypes.
    """
    prepared_df = features_df.copy()

    # Auto-detect categorical columns when not supplied.
    if categorical_cols is None:
        categorical_cols = [
            col
            for col in prepared_df.columns
            if prepared_df[col].dtype == "object" or str(prepared_df[col].dtype).startswith("category")
        ]

    # One-hot encode categorical features while preserving row index.
    if categorical_cols:
        prepared_df[categorical_cols] = prepared_df[categorical_cols].astype(str)
        prepared_df = pd.get_dummies(
            prepared_df,
            columns=categorical_cols,
            drop_first=False,
            dtype=float,
        )

    # Keep only numeric columns for modeling.
    numeric_cols = prepared_df.select_dtypes(include=[np.number]).columns
    prepared_df = prepared_df[numeric_cols]

    if prepared_df.shape[1] == 0:
        raise ValueError("No numeric features available after preprocessing.")

    return prepared_df


def build_h3_feature_sets(
    node_indicators_df: pd.DataFrame,
    *,
    key_score_cols: tuple[str, ...] = DEFAULT_KEY_SCORE_COLUMNS,
    baseline_cols: list[str] | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Build baseline and augmented feature sets for H3 evaluation.

    Baseline features are all indicators except `key_score_cols`, unless
    `baseline_cols` is explicitly supplied. Augmented features include baseline
    plus all key-score columns.

    Args:
        node_indicators_df: Indicators table indexed by account ID.
        key_score_cols: Key-score columns to test as added predictive signal.
        baseline_cols: Optional explicit baseline feature column list.

    Returns:
        tuple[pd.DataFrame, pd.DataFrame]:
            Baseline matrix and augmented matrix aligned on the same index.
    """
    missing_key_cols = [col for col in key_score_cols if col not in node_indicators_df.columns]
    if missing_key_cols:
        raise KeyError(f"Missing key-score columns in node_indicators_df: {missing_key_cols}")

    if baseline_cols is None:
        baseline_cols = [col for col in node_indicators_df.columns if col not in key_score_cols]
    else:
        missing_baseline_cols = [col for col in baseline_cols if col not in node_indicators_df.columns]
        if missing_baseline_cols:
            raise KeyError(f"Missing baseline columns in node_indicators_df: {missing_baseline_cols}")

    baseline_raw_df = node_indicators_df[baseline_cols].copy()
    augmented_raw_df = node_indicators_df[baseline_cols + list(key_score_cols)].copy()

    baseline_df = _prepare_feature_matrix(baseline_raw_df)
    augmented_df = _prepare_feature_matrix(augmented_raw_df, categorical_cols=["top_topic"])

    # Align encoded matrices to guarantee consistent row order.
    baseline_df = baseline_df.sort_index()
    augmented_df = augmented_df.sort_index()

    if not baseline_df.index.equals(augmented_df.index):
        raise ValueError("Baseline and augmented features are not aligned by index.")

    return baseline_df, augmented_df


def build_io_labels(index: pd.Index, io_authors_set: set[str] | set[int]) -> pd.Series:
    """Build binary IO labels from author index and IO author set.

    Args:
        index: Author/account index to label.
        io_authors_set: Set of IO author IDs.

    Returns:
        pd.Series: Binary labels (1=IO, 0=Non-IO) indexed by account.
    """
    io_authors_str_set = set(map(str, io_authors_set))
    y_series = pd.Series(index.astype(str).isin(io_authors_str_set).astype(int), index=index, name="io_label")
    return y_series


def _compute_midrank(x: np.ndarray) -> np.ndarray:
    """Compute midranks for DeLong AUC variance estimation.

    Args:
        x: 1D array of scores.

    Returns:
        np.ndarray: Midranks for input array.
    """
    j = np.argsort(x)
    z = x[j]
    n = len(x)
    t = np.zeros(n, dtype=float)
    i = 0
    while i < n:
        k = i
        while k < n and z[k] == z[i]:
            k += 1
        t[i:k] = 0.5 * (i + k - 1) + 1
        i = k
    out = np.empty(n, dtype=float)
    out[j] = t
    return out


def _fast_delong(predictions_sorted_transposed: np.ndarray, label_1_count: int) -> tuple[np.ndarray, np.ndarray]:
    """Fast DeLong covariance computation for correlated ROC AUCs.

    Args:
        predictions_sorted_transposed: Shape [n_classifiers, n_examples].
            Columns must be ordered with positives first, negatives second.
        label_1_count: Number of positive samples.

    Returns:
        tuple[np.ndarray, np.ndarray]: AUCs and covariance matrix.
    """
    m = label_1_count
    n = predictions_sorted_transposed.shape[1] - m
    positive_examples = predictions_sorted_transposed[:, :m]
    negative_examples = predictions_sorted_transposed[:, m:]

    k = predictions_sorted_transposed.shape[0]
    tx = np.empty((k, m), dtype=float)
    ty = np.empty((k, n), dtype=float)
    tz = np.empty((k, m + n), dtype=float)

    for r in range(k):
        tx[r, :] = _compute_midrank(positive_examples[r, :])
        ty[r, :] = _compute_midrank(negative_examples[r, :])
        tz[r, :] = _compute_midrank(predictions_sorted_transposed[r, :])

    aucs = tz[:, :m].sum(axis=1) / (m * n) - (m + 1.0) / (2.0 * n)
    v01 = (tz[:, :m] - tx[:, :]) / n
    v10 = 1.0 - (tz[:, m:] - ty[:, :]) / m
    sx = np.cov(v01)
    sy = np.cov(v10)
    delong_cov = sx / m + sy / n
    return aucs, delong_cov


def delong_test(y_true: np.ndarray, y_score_a: np.ndarray, y_score_b: np.ndarray) -> tuple[float, float]:
    """Run two-sided DeLong test for two correlated ROC AUCs.

    Args:
        y_true: Binary labels (0/1).
        y_score_a: Predicted probabilities from model A.
        y_score_b: Predicted probabilities from model B.

    Returns:
        tuple[float, float]: z-score and two-sided p-value.
    """
    order = np.argsort(-y_true)
    y_true_sorted = y_true[order]
    if not np.array_equal(np.unique(y_true_sorted), np.array([0, 1])):
        raise ValueError("y_true must contain both classes for DeLong test.")

    predictions = np.vstack([y_score_a, y_score_b])[:, order]
    label_1_count = int(y_true_sorted.sum())
    aucs, delong_cov = _fast_delong(predictions, label_1_count)

    diff = aucs[1] - aucs[0]
    var = delong_cov[0, 0] + delong_cov[1, 1] - 2 * delong_cov[0, 1]
    if var <= 0:
        raise ValueError("Non-positive variance in DeLong test; cannot compute z-score.")

    z_score = diff / np.sqrt(var)
    p_value = 2.0 * stats.norm.sf(abs(z_score))
    return float(z_score), float(p_value)


def _delong_test(y_true: np.ndarray, y_score_a: np.ndarray, y_score_b: np.ndarray) -> tuple[float, float]:
    """Backward-compatible private alias for DeLong test."""
    return delong_test(y_true=y_true, y_score_a=y_score_a, y_score_b=y_score_b)


def run_h3_xgboost_evaluation(
    node_indicators_df: pd.DataFrame,
    io_authors_set: set[str] | set[int],
    output_folder_path: str | Path | None = None,
    *,
    key_score_cols: tuple[str, ...] = DEFAULT_KEY_SCORE_COLUMNS,
    test_size: float = 0.2,
    random_state: int = 42,
) -> H3EvaluationResult:
    """Run H3 AUC comparison (baseline vs key-score-augmented) with XGBoost.

    Args:
        node_indicators_df: Node indicators indexed by account ID.
        io_authors_set: Set of account IDs labeled as IO.
        output_folder_path: Optional output folder for artifacts.
        key_score_cols: Key-score columns for augmented model.
        test_size: Fraction of data reserved for test split.
        random_state: Random seed for reproducibility.

    Returns:
        H3EvaluationResult: Summary metrics from the H3 experiment.
    """
    baseline_df, augmented_df = build_h3_feature_sets(
        node_indicators_df=node_indicators_df,
        key_score_cols=key_score_cols,
    )
    y_series = build_io_labels(baseline_df.index, io_authors_set)

    # Use one split index to ensure paired comparison on identical test labels.
    all_indices = baseline_df.index.to_numpy()
    train_idx, test_idx = train_test_split(
        all_indices,
        test_size=test_size,
        random_state=random_state,
        stratify=y_series.loc[all_indices].to_numpy(),
    )

    Xb_train = baseline_df.loc[train_idx]
    Xb_test = baseline_df.loc[test_idx]
    Xa_train = augmented_df.loc[train_idx]
    Xa_test = augmented_df.loc[test_idx]
    y_train = y_series.loc[train_idx].to_numpy()
    y_test = y_series.loc[test_idx].to_numpy()

    baseline_model = XGBClassifier(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.9,
        colsample_bytree=0.9,
        eval_metric="logloss",
        random_state=random_state,
    )
    augmented_model = XGBClassifier(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.9,
        colsample_bytree=0.9,
        eval_metric="logloss",
        random_state=random_state,
    )

    # Fit and score both models on the same split.
    baseline_model.fit(Xb_train, y_train)
    augmented_model.fit(Xa_train, y_train)
    baseline_proba = baseline_model.predict_proba(Xb_test)[:, 1]
    augmented_proba = augmented_model.predict_proba(Xa_test)[:, 1]

    baseline_auc = float(roc_auc_score(y_test, baseline_proba))
    augmented_auc = float(roc_auc_score(y_test, augmented_proba))
    auc_delta = augmented_auc - baseline_auc
    z_score, p_value = _delong_test(y_test, baseline_proba, augmented_proba)

    result = H3EvaluationResult(
        baseline_auc=baseline_auc,
        augmented_auc=augmented_auc,
        auc_delta=auc_delta,
        delong_p_value=p_value,
        delong_z_score=z_score,
        n_train=len(train_idx),
        n_test=len(test_idx),
    )

    if output_folder_path is not None:
        output_dir = Path(output_folder_path)
        output_dir.mkdir(parents=True, exist_ok=True)

        results_df = pd.DataFrame(
            [
                {
                    "baseline_auc": result.baseline_auc,
                    "augmented_auc": result.augmented_auc,
                    "auc_delta": result.auc_delta,
                    "delong_z_score": result.delong_z_score,
                    "delong_p_value": result.delong_p_value,
                    "n_train": result.n_train,
                    "n_test": result.n_test,
                    "key_score_columns": ",".join(key_score_cols),
                    "model_name": "xgboost",
                }
            ]
        )
        results_df.to_parquet(output_dir / "h3_auc_comparison.parquet", compression="gzip", index=False)

        summary_text = (
            "H3 Narrative Amplification Evaluation\n"
            "===================================\n"
            f"Model: XGBoost\n"
            f"Baseline AUC: {result.baseline_auc:.6f}\n"
            f"Augmented AUC: {result.augmented_auc:.6f}\n"
            f"Delta AUC (augmented - baseline): {result.auc_delta:.6f}\n"
            f"DeLong z-score: {result.delong_z_score:.6f}\n"
            f"DeLong p-value: {result.delong_p_value:.6g}\n"
            f"Significant at alpha=0.05: {result.delong_p_value < 0.05}\n"
            f"Train samples: {result.n_train}\n"
            f"Test samples: {result.n_test}\n"
            f"Key-score columns: {', '.join(key_score_cols)}\n"
        )
        (output_dir / "h3_delong_summary.txt").write_text(summary_text, encoding="utf-8")

    return result
