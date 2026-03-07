# TruthLens-UA — поточний стан проєкту

**Оновлено (UTC):** 2026-03-07T21:34:55Z

Цей файл оновлюється скриптом `python scripts/update_project_state.py` для збереження прогресу після паузи чи перезавантаження.

## Чеклист

| Елемент | Стан |
|---------|------|
| data/Fake.csv | ✅ |
| data/True.csv | ✅ |
| artifacts/best_model.joblib | ✅ |
| remote origin (GitHub) | ✅ |
| remote gitlab | ✅ |

## Останній коміт

```
d568f8858593c9926d0364196297c3fe282191c4 2026-03-05 23:17:16 +0100 docs: session report 050326 2311 â€” step-by-step, stats, pause/shutdown OK
```

## Рекомендований наступний крок

notebooks/03_ua_nlp_training.ipynb (A/B), git push origin main && git push gitlab main, деплой (docs/DEPLOYMENT.md).

## Примітка

Файли даних (Fake.csv, True.csv) та модель (best_model.joblib) не комітяться в репо — вони лише локально. Після клону: python scripts/download_datasets.py та запуск ноутбука 01.

---

Після перезавантаження: запустіть `python scripts/next_step.py` та прочитайте **docs/CONTINUE_AFTER_PAUSE.md**.