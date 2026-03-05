# TruthLens UA — Fake News & ІПСО Detector

**Repository:** https://github.com/102012dl/TruthLens-UA  
**GitLab mirror (CI/CD):** https://gitlab.com/102012dl/truthlens-ua (user **102012dl**, не group)  

Backend MVP for **TruthLens UA**, a Ukrainian/English fake news and information-operations (ІПСО) detector.

## Components

- `src/ml/analyzer.py` — hybrid analyzer (LinearSVC + UA ІПСО rule-based fallback)
- `src/api/main.py` — FastAPI backend with `/health`, `/api/analyze`, `/api/models`, `/api/stats`
- `tests/unit/test_ml_validation.py` — ML and ІПСО validation tests

## Quick start

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt

uvicorn src.api.main:app --reload
```

Then open `http://localhost:8000/docs` to test the API.

## Наступний крок

З кореня проєкту: **`python scripts/next_step.py`** — перевірка стану (remotes, дані, модель, тести) і рекомендація одного наступного кроку. Детально: **docs/NEXT_STEP.md**.

## CI/CD and GitLab mirror

- **GitHub Actions:** on push to `main` — lint, tests, ML validation; then mirror to GitLab.
- **GitLab:** same code runs in GitLab CI (see `.gitlab-ci.yml`). To enable the mirror, add `GITLAB_SSH_KEY` in GitHub Secrets and follow **docs/GITLAB_MIRROR.md**.
