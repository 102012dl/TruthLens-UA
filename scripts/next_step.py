#!/usr/bin/env python3
"""
TruthLens-UA — визначення наступного кроку та швидка перевірка стану проєкту.
Запуск: з кореня проєкту: python scripts/next_step.py
"""
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)


def run(cmd: list[str]) -> tuple[bool, str]:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=30, cwd=ROOT)
        return r.returncode == 0, (r.stdout or "") + (r.stderr or "")
    except Exception as e:
        return False, str(e)


def check(name: str, ok: bool, msg: str = "") -> None:
    sym = "✅" if ok else "❌"
    print(f"  {sym} {name}" + (f" — {msg}" if msg else ""))


def main() -> None:
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    print("=== TruthLens-UA — перевірка стану проєкту ===\n")

    # 1. Git remotes
    print("1. Git remotes")
    ok_origin, out = run(["git", "remote", "-v"])
    has_origin = "origin" in out and "102012dl" in out and "TruthLens" in out
    has_gitlab = "gitlab" in out and "truthlens-ua" in out
    check("origin (GitHub TruthLens-UA)", has_origin, "git remote add origin https://github.com/102012dl/TruthLens-UA.git" if not has_origin else "")
    check("gitlab (GitLab truthlens-ua)", has_gitlab, "git remote add gitlab git@gitlab.com:102012dl/truthlens-ua.git" if not has_gitlab else "")
    if not ok_origin:
        print("     (git не ініціалізовано або не в корені репо)")
    print()

    # 2. Data
    print("2. Датасет ISOT (data/)")
    data_dir = ROOT / "data"
    fake = data_dir / "Fake.csv"
    true = data_dir / "True.csv"
    has_fake, has_true = fake.exists(), true.exists()
    check("Fake.csv", has_fake)
    check("True.csv", has_true)
    if not (has_fake and has_true):
        print("     -> Завантажте з Kaggle (Fake and Real News), покладіть у data/ (див. data/README.md)")
    print()

    # 3. Model
    print("3. Модель (artifacts/)")
    model_path = ROOT / "artifacts" / "best_model.joblib"
    has_model = model_path.exists()
    check("best_model.joblib", has_model)
    if not has_model:
        print("     -> Після завантаження даних виконайте notebooks/01_isot_fake_news_mlflow.ipynb")
    print()

    # 4. Tests
    print("4. Тести (pytest)")
    ok_pytest, out_pytest = run([sys.executable, "-m", "pytest", "tests/unit/", "-v", "--tb=no", "-q"])
    check("pytest", ok_pytest, "частина тестів може падати без моделі (це ок)")
    if not ok_pytest and "model_loaded" in out_pytest:
        print("     -> test_model_loaded очікує best_model.joblib; решта тестів — rule-based")
    print()

    # 5. Next step recommendation
    print("=== Рекомендований наступний крок ===\n")
    if not has_origin and not has_gitlab:
        print("  • Ініціалізуйте git, додайте remotes і зробіть перший push (див. docs/GIT_SETUP.md).")
    elif not (has_fake and has_true):
        print("  • Завантажте ISOT: data/README.md. Потім запустіть notebooks/01_isot_fake_news_mlflow.ipynb.")
    elif not has_model:
        print("  • Запустіть notebooks/01_isot_fake_news_mlflow.ipynb (Run All) — збережеться artifacts/best_model.joblib.")
    else:
        print("  • Модель є. Далі: notebooks/03_ua_nlp_training.ipynb (A/B), push у origin/gitlab, деплой (docs/DEPLOYMENT.md).")
    print("\nДетальний промт для Cursor: docs/NEXT_STEP.md")
    print()


if __name__ == "__main__":
    main()
