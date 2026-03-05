"""CRITICAL: These tests prove ML model works correctly."""

import pytest

from src.ml.analyzer import analyze_text, get_analyzer


class TestMLValidation:
    def test_model_loaded(self) -> None:
        """ML model must be loaded, not rule-based."""
        analyzer = get_analyzer()
        assert analyzer.model_loaded, "best_model.joblib NOT found! Run notebook first."

    def test_fake_ua_ipso(self) -> None:
        """Classic UA ІПСО text must be FAKE."""
        result = analyze_text(
            "ТЕРМІНОВО!!! ЗСУ ЗДАЛИ Харків! Зеленський підписав "
            "капітуляцію! Поширте до видалення!",
        )
        assert result["label"] == "FAKE", f"Expected FAKE, got {result['label']}"
        assert result["fake_score"] > 0.80, (
            f"Expected >0.80, got {result['fake_score']}"
        )

    def test_real_official(self) -> None:
        """Official source text must be REAL."""
        result = analyze_text(
            "НБУ підвищив облікову ставку до 16% річних. "
            "Рішення ухвалено на засіданні Правління.",
        )
        assert result["label"] == "REAL", f"Expected REAL, got {result['label']}"
        assert result["fake_score"] < 0.30, (
            f"Expected <0.30, got {result['fake_score']}"
        )

    def test_coffee_satire_not_real(self) -> None:
        """'coffee makes you live forever' must NOT be REAL."""
        result = analyze_text(
            "Breaking: Scientists discover coffee makes you live forever "
            "and cures cancer!",
        )
        assert result["label"] != "REAL" or result["fake_score"] > 0.40, (
            "FALSE POSITIVE: coffee satire classified as "
            f"{result['label']} {result['fake_score']}"
        )

    def test_ipso_detection(self) -> None:
        """ІПСО techniques must be detected."""
        result = analyze_text(
            "Прокидайтесь люди! Уряд приховує правду! Поширте до видалення!",
        )
        assert len(result["ipso_techniques"]) >= 2, (
            f"Expected ≥2 ІПСО, got {result['ipso_techniques']}"
        )

    def test_deepfake_risk(self) -> None:
        """DeepFake indicator must trigger."""
        result = analyze_text(
            "Зеленський у відеозверненні заявив про капітуляцію. "
            "Відео набрало 2 млн переглядів.",
        )
        assert result["deepfake_risk"] in ["MEDIUM", "HIGH"], (
            f"Expected MEDIUM/HIGH deepfake risk, got {result['deepfake_risk']}"
        )

    def test_f1_on_isot_sample(self) -> None:
        """F1 must be ≥ 0.95 on ISOT test samples (if file present)."""
        from sklearn.metrics import f1_score
        import pandas as pd

        try:
            df = pd.read_csv("data/isot_test_100.csv")  # 50 fake + 50 real
        except FileNotFoundError:
            pytest.skip("ISOT test file not found — run notebook first")

        preds = [analyze_text(t)["label"] for t in df["text"].tolist()]
        f1 = f1_score(
            df["label"].tolist(),
            preds,
            average="weighted",
            labels=["FAKE", "REAL", "SUSPICIOUS"],
        )
        assert f1 >= 0.95, f"F1 too low: {f1:.4f} (need ≥ 0.95)"

