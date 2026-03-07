#!/usr/bin/env python3
"""
TruthLens-UA — оновлення файлу стану проєкту (прогрес, статистика).
Зберігає поточний стан у docs/PROJECT_STATE.md та docs/PROJECT_STATE.json
для продовження роботи після паузи чи перезавантаження.

Запуск: з кореня проєкту: python scripts/update_project_state.py
"""
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)
STATE_MD = ROOT / "docs" / "PROJECT_STATE.md"
STATE_JSON = ROOT / "docs" / "PROJECT_STATE.json"


def run(cmd: list[str]) -> tuple[bool, str]:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=30, cwd=ROOT)
        return r.returncode == 0, (r.stdout or "").strip() + (r.stderr or "").strip()
    except Exception as e:
        return False, str(e)


def collect_state() -> dict:
    data_dir = ROOT / "data"
    fake = data_dir / "Fake.csv"
    true = data_dir / "True.csv"
    model_path = ROOT / "artifacts" / "best_model.joblib"

    has_fake = fake.exists()
    has_true = true.exists()
    has_model = model_path.exists()

    ok_remote, out_remote = run(["git", "remote", "-v"])
    has_origin = ok_remote and "origin" in out_remote and "102012dl" in out_remote and "TruthLens" in out_remote
    has_gitlab = ok_remote and "gitlab" in out_remote and "truthlens-ua" in out_remote

    ok_log, out_log = run(["git", "log", "-1", "--format=%H %ci %s"])
    last_commit = out_log if ok_log else ""

    # Рекомендований наступний крок
    if not has_origin and not has_gitlab:
        next_step = "Ініціалізуйте git, додайте remotes, перший push (docs/GIT_SETUP.md)."
    elif not (has_fake and has_true):
        next_step = "Завантажте ISOT: python scripts/download_datasets.py або data/README.md."
    elif not has_model:
        next_step = "Запустіть notebooks/01_isot_fake_news_mlflow.ipynb (Run All)."
    else:
        next_step = "Деплой (docs/DEPLOYMENT.md), потім python scripts/demo_api.py [URL]; git push origin main && git push gitlab main."

    return {
        "updated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "data": {
            "Fake.csv": has_fake,
            "True.csv": has_true,
        },
        "artifacts": {"best_model.joblib": has_model},
        "remotes": {"origin_github": has_origin, "gitlab": has_gitlab},
        "last_commit": last_commit,
        "next_step": next_step,
        "note": "Файли даних (Fake.csv, True.csv) та модель (best_model.joblib) не комітяться в репо — вони лише локально. Після клону: python scripts/download_datasets.py та запуск ноутбука 01.",
    }


def write_state(state: dict) -> None:
    STATE_MD.parent.mkdir(parents=True, exist_ok=True)

    # Markdown для людей
    lines = [
        "# TruthLens-UA — поточний стан проєкту",
        "",
        "**Оновлено (UTC):** " + state["updated_utc"],
        "",
        "Цей файл оновлюється скриптом `python scripts/update_project_state.py` для збереження прогресу після паузи чи перезавантаження.",
        "",
        "## Чеклист",
        "",
        "| Елемент | Стан |",
        "|---------|------|",
        f"| data/Fake.csv | {'✅' if state['data']['Fake.csv'] else '❌'} |",
        f"| data/True.csv | {'✅' if state['data']['True.csv'] else '❌'} |",
        f"| artifacts/best_model.joblib | {'✅' if state['artifacts']['best_model.joblib'] else '❌'} |",
        f"| remote origin (GitHub) | {'✅' if state['remotes']['origin_github'] else '❌'} |",
        f"| remote gitlab | {'✅' if state['remotes']['gitlab'] else '❌'} |",
        "",
        "## Останній коміт",
        "",
        "```",
        state["last_commit"],
        "```",
        "",
        "## Рекомендований наступний крок",
        "",
        state["next_step"],
        "",
        "## Примітка",
        "",
        state["note"],
        "",
        "---",
        "",
        "Після перезавантаження: запустіть `python scripts/next_step.py` та прочитайте **docs/CONTINUE_AFTER_PAUSE.md**.",
    ]
    STATE_MD.write_text("\n".join(lines), encoding="utf-8")

    # JSON для скриптів/автоматизації
    STATE_JSON.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    state = collect_state()
    write_state(state)
    print("State updated:", state["updated_utc"])
    print("  PROJECT_STATE.md, PROJECT_STATE.json written to docs/")
    print("  Next step:", state["next_step"])


if __name__ == "__main__":
    main()
