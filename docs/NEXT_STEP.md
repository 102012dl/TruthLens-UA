# TruthLens-UA — наступний крок (автоматизований промт і команди)

Скрипт перевірки стану: **`python scripts/next_step.py`** (запускати з кореня проєкту). Він покаже, що вже є і що робити далі.

---

## 0. Поточний стан та один наступний крок (оновлено 05.03.2026)

| Перевірка | Стан |
|-----------|------|
| Git (локально) | ✅ `git init`, коміт, remote `origin` додано |
| Git push (GitHub) | ⏳ потрібно створити репо та виконати `git push -u origin main` |
| data/Fake.csv, True.csv | ❌ відсутні |
| artifacts/best_model.joblib | ❌ відсутня |
| pytest | ⚠️ частина тестів очікує модель |

**Один конкретний наступний крок:**

1. **Створіть репо на GitHub** (якщо ще немає): [github.com/new](https://github.com/new) → name `TruthLens-UA`, Public.  
2. **Виконайте push:** у корені проєкту: `git push -u origin main`.  
3. Далі: завантажити ISOT у `data/` (див. `data/README.md`) → виконати `notebooks/01_isot_fake_news_mlflow.ipynb` → деплой за `docs/DEPLOYMENT.md`.

**Усі необхідні дії та розрахунковий час:** **docs/REQUIRED_ACTIONS_AND_TIME.md**.

---

## 1. Промт для Cursor Agent (скопіюй і вставити)

```
Проаналізуй проєкт TruthLens-UA (GitHub 102012dl/TruthLens-UA, GitLab 102012dl/truthlens-ua). 
Виконай наступне по черзі, лише те що ще не зроблено:
1) Перевір наявність data/Fake.csv та data/True.csv; якщо їх немає — виведи чіткі інструкції за data/README.md та не змінюй код.
2) Якщо дані є — запусти або підготуй запуск notebooks/01_isot_fake_news_mlflow.ipynb (всі клітинки), переконайся що зберігається artifacts/best_model.joblib.
3) Запусти pytest tests/unit/ -v --tb=short і зафіксуй результат (якщо модель є — test_model_loaded має пройти).
4) Перевір що .github/workflows/ci.yml веде mirror на git@gitlab.com:102012dl/truthlens-ua.git та що docs посилаються на user 102012dl і slug truthlens-ua.
Підсумуй виконане та напиши один конкретний наступний крок для користувача.
```

---

## 2. Команди по черзі (ручний варіант)

Виконувати з **кореня проєкту** (де лежать `src/`, `notebooks/`, `data/`).

| № | Дія | Команда або дія |
|---|-----|------------------|
| 1 | Перевірити стан | `python scripts/next_step.py` |
| 2 | Remotes | `git remote -v` (мають бути origin → GitHub, gitlab → GitLab truthlens-ua) |
| 3 | Push у GitHub | `git add -A && git commit -m "..." && git push -u origin main` |
| 4 | Push у GitLab (якщо є SSH) | `git push -u gitlab main` |
| 5 | Дані ISOT | Завантажити з Kaggle у `data/` (Fake.csv, True.csv) — див. data/README.md |
| 6 | Тренування моделі | Відкрити Jupyter, виконати **Run All** у `notebooks/01_isot_fake_news_mlflow.ipynb` |
| 7 | Тести | `pytest tests/unit/ -v --tb=short` |
| 8 | Деплой | Підключити репо до Render/Railway за docs/DEPLOYMENT.md |

---

## 3. Що робить scripts/next_step.py

- Перевіряє наявність remote **origin** (GitHub) та **gitlab** (GitLab truthlens-ua).
- Перевіряє наявність **data/Fake.csv** та **data/True.csv**.
- Перевіряє наявність **artifacts/best_model.joblib**.
- Запускає **pytest tests/unit/** і показує результат.
- Виводить **один рекомендований наступний крок** і посилання на цей файл.

Запуск: `python scripts/next_step.py` (краще з активованим venv і встановленими залежностями).
