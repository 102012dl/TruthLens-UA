#!/usr/bin/env python3
"""
TruthLens UA — A/B тести моделей (LinearSVC, LogReg, RandomForest) на ISOT.
Можна запускати замість повного ноутбука 03 для швидкої перевірки.
Запуск: python scripts/run_ab_tests.py [--sample N]
  --sample N  використати випадкову підвибірку N рядків (за замовч. усі дані)
"""
import argparse
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))

import pandas as pd
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, accuracy_score

try:
    import mlflow
    import mlflow.sklearn
    HAS_MLFLOW = True
except ImportError:
    HAS_MLFLOW = False


def load_isot(sample: int | None = None) -> tuple[list, list]:
    """Завантажити ISOT з data/; опційно обмежити sample рядками."""
    data_dir = ROOT / "data"
    fake_path = data_dir / "Fake.csv"
    true_path = data_dir / "True.csv"
    if not fake_path.exists() or not true_path.exists():
        print("Потрібні data/Fake.csv та data/True.csv. Запустіть: python scripts/download_datasets.py")
        sys.exit(1)
    fake = pd.read_csv(fake_path)
    true = pd.read_csv(true_path)
    fake["label"], true["label"] = "FAKE", "REAL"
    text_col = "text" if "text" in fake.columns else "title"
    df = pd.concat([fake[[text_col, "label"]], true[[text_col, "label"]]], ignore_index=True)
    df = df.dropna(subset=[text_col])
    df[text_col] = df[text_col].astype(str)
    if sample and len(df) > sample:
        df = df.sample(n=sample, random_state=42)
    X = df[text_col].tolist()
    y = df["label"].tolist()
    return X, y


def main() -> None:
    ap = argparse.ArgumentParser(description="A/B тести моделей на ISOT")
    ap.add_argument("--sample", type=int, default=None, help="Макс. к-сть зразків (для швидкого прогону)")
    args = ap.parse_args()
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    print("Завантаження ISOT...")
    X, y = load_isot(sample=args.sample)
    print(f"Зразків: {len(X)}, розподіл: {pd.Series(y).value_counts().to_dict()}")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    models = {
        "LinearSVC_C1": LinearSVC(max_iter=10000, C=1.0),
        "LinearSVC_C05": LinearSVC(max_iter=10000, C=0.5),
        "LogisticReg": LogisticRegression(max_iter=1000, C=1.0),
        "RandomForest": RandomForestClassifier(n_estimators=100, random_state=42),
    }
    if HAS_MLFLOW:
        mlflow.set_experiment("ab-test-ukraine-nlp")

    results = {}
    for name, clf in models.items():
        pipe = Pipeline([
            ("tfidf", TfidfVectorizer(max_features=50000, ngram_range=(1, 2), min_df=2)),
            ("clf", clf),
        ])
        t0 = time.time()
        pipe.fit(X_train, y_train)
        lat_ms = int((time.time() - t0) * 1000)
        preds = pipe.predict(X_test)
        f1 = f1_score(y_test, preds, average="weighted")
        acc = accuracy_score(y_test, preds)
        results[name] = {"f1": f1, "acc": acc, "latency_ms": lat_ms}
        if HAS_MLFLOW:
            with mlflow.start_run(run_name=f"AB_{name}"):
                mlflow.set_tags({"ab_test": True, "student": "102012dl", "dataset": "ISOT"})
                mlflow.log_metrics({"f1": f1, "accuracy": acc, "latency_ms": lat_ms})
                mlflow.sklearn.log_model(pipe, f"model_{name}")
        print(f"  {name}: F1={f1:.4f} | Acc={acc:.4f} | Lat={lat_ms}ms")
    best = max(results, key=lambda k: results[k]["f1"])
    print(f"\nПереможець: {best} (F1={results[best]['f1']:.4f})")
    print("=== A/B тести завершено ===")


if __name__ == "__main__":
    main()
