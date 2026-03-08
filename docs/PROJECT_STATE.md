# TruthLens-UA — поточний стан проєкту

**Оновлено (UTC):** 2026-03-08T00:07:20Z

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
0ede6e118cfafddfb13748087ea5365883a45772 2026-03-08 00:57:22 +0100 fix(api): add GET / root response, fix Pydantic model_used warning
```

## Рекомендований наступний крок

Прогнати демо: python scripts/demo_api.py https://truthlens-ua.onrender.com; підготовка слайдів та план розділу 3 (docs/REQUIRED_ACTIONS_AND_TIME.md).

## Примітка

Файли даних (Fake.csv, True.csv) та модель (best_model.joblib) не комітяться в репо — вони лише локально. Після клону: python scripts/download_datasets.py та запуск ноутбука 01.

---

Після перезавантаження: запустіть `python scripts/next_step.py` та прочитайте **docs/CONTINUE_AFTER_PAUSE.md**.