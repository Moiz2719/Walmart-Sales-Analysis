"""Scale customer behaviour features and assign K-Means clusters."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "outputs" / "customers_cleaned.csv"
DEFAULT_OUTPUT = ROOT / "outputs" / "customers_segmented.csv"
DEFAULT_METRICS = ROOT / "outputs" / "cluster_evaluation.json"

FEATURES = [
    "Age", "Income", "Children_Total", "Recency", "Total_Spending",
    "Total_Purchases", "NumWebVisitsMonth", "NumDealsPurchases",
]


def select_features(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    available = [c for c in FEATURES if c in df.columns]
    if len(available) < 2:
        raise ValueError(f"At least two segmentation features must exist. Available: {available}")
    matrix = df[available].apply(pd.to_numeric, errors="coerce")
    matrix = matrix.replace([np.inf, -np.inf], np.nan)
    matrix = matrix.fillna(matrix.median()).fillna(0)
    return matrix, available


def fit_best_kmeans(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    matrix, features = select_features(df)
    if len(df) < 3:
        raise ValueError("At least three records are required for cluster selection.")

    scaler = StandardScaler()
    scaled = scaler.fit_transform(matrix)

    scores = {}
    upper_k = min(8, len(df) - 1)
    for k in range(2, upper_k + 1):
        model = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = model.fit_predict(scaled)
        if len(set(labels)) > 1:
            scores[str(k)] = float(silhouette_score(scaled, labels))

    if not scores:
        raise ValueError("Could not evaluate a valid cluster count for this dataset.")

    best_k = int(max(scores, key=scores.get))
    final_model = KMeans(n_clusters=best_k, random_state=42, n_init=10)
    result = df.copy()
    result["Segment_ID"] = final_model.fit_predict(scaled)

    metrics = {
        "features_used": features,
        "candidate_silhouette_scores": scores,
        "selected_k": best_k,
        "selected_silhouette_score": scores[str(best_k)],
        "method": "KMeans with StandardScaler; k selected by highest silhouette score in range 2..8",
        "random_state": 42,
    }
    return result, metrics


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--metrics", type=Path, default=DEFAULT_METRICS)
    args = parser.parse_args()

    if not args.input.exists():
        raise FileNotFoundError(f"Cleaned dataset not found: {args.input}. Run src/clean_data.py first.")

    df = pd.read_csv(args.input)
    segmented, metrics = fit_best_kmeans(df)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.to_csv(args.output, index=False)
    args.metrics.parent.mkdir(parents=True, exist_ok=True)
    args.metrics.write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    print(f"Features used: {metrics['features_used']}")
    print(f"Selected number of clusters: {metrics['selected_k']}")
    print(f"Silhouette score: {metrics['selected_silhouette_score']:.3f}")
    print(f"Saved assigned segments to: {args.output}")


if __name__ == "__main__":
    main()
