# TruthLens-UA — необхідні дії та розрахунковий час

**Оновлено:** 05.03.2026  

---

## Виконано автоматично (Agent)

| Дія | Стан | Примітка |
|-----|------|----------|
| Ініціалізація Git (`git init`, `branch -M main`) | ✅ | Репо створено локально |
| Індекс і коміти (`git add -A`, `git commit`) | ✅ | Документація, merge з origin |
| Remote `origin` (GitHub) | ✅ | `https://github.com/102012dl/TruthLens-UA.git` |
| **Push у GitHub** | ✅ | Код у [github.com/102012dl/TruthLens-UA](https://github.com/102012dl/TruthLens-UA) |
| Remote `gitlab` | ✅ | `https://gitlab.com/102012dl/truthlens-ua.git` |
| Push у GitLab | ⏳ | Виконати `git push -u gitlab main` (при потребі — логін у терміналі) |

**Далі потрібні дії від вас** — нижче з орієнтовним часом.

---

## Необхідні дії (від користувача) та розрахунковий час

| № | Дія | Розрахунковий час | Деталі |
|---|-----|-------------------|--------|
| 1 | **Створити репо на GitHub** (якщо ще немає) | **5–10 хв** | [github.com/new](https://github.com/new) → Repository name: `TruthLens-UA`, Public. Далі: `git push -u origin main`. |
| 2 | **Push у GitHub** | **1–2 хв** | У корені проєкту: `git push -u origin main`. Потрібен увійти в GitHub (браузер/CLI). |
| 3 | **Опційно: GitLab** — створити проєкт, додати remote, push | **10–15 хв** | [GitLab New project](https://gitlab.com/projects/new). Потім: `git remote add gitlab https://gitlab.com/102012dl/truthlens-ua.git`, `git push -u gitlab main`. |
| 4 | **Завантажити ISOT (Fake.csv, True.csv)** | **10–15 хв** | Kaggle: [Fake and Real News Dataset](https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset). Розархівувати й покласти обидва CSV у `data/`. Див. `data/README.md`. |
| 5 | **Запустити ноутбук 01 (тренування моделі)** | **20–40 хв** | Відкрити `notebooks/01_isot_fake_news_mlflow.ipynb` → **Run All**. Збережеться `artifacts/best_model.joblib`. |
| 6 | **Запустити ноутбук 03 (A/B, MLflow)** | **15–25 хв** | `notebooks/03_ua_nlp_training.ipynb` → Run All для порівняння моделей. |
| 7 | **Деплой (Render або Railway)** | **15–20 хв** | Підключити репо до Render/Railway за `docs/DEPLOYMENT.md`, налаштувати Build/Start (Procfile вже є). |
| 8 | **Підготовка до захисту (слайди, демо)** | **1–2 год** | 8 демо-текстів у мастер-промпті; прогнати через API перед захистом. |

---

## Сумарний розрахунковий час

| Сценарій | Час |
|----------|-----|
| **Мінімум до MVP (push + дані + ноутбук 01 + деплой)** | **~1–1,5 год** |
| **Повний цикл (GitHub + GitLab + ISOT + 01 + 03 + деплой)** | **~1,5–2,5 год** |
| **З підготовкою до захисту (слайди, демо)** | **~2,5–4 год** |

---

## Швидкі команди після виконаного Agent

```bash
# Після створення репо на GitHub:
git push -u origin main

# Перевірка стану проєкту:
python scripts/next_step.py
```

Детальні кроки: **docs/GIT_SETUP.md**, **docs/DEPLOYMENT.md**, **data/README.md**.
