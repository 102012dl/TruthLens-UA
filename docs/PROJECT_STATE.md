# TruthLens-UA — поточний стан проєкту

**Оновлено (UTC):** 2026-03-07T21:54:33Z

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
bfd83f45228255d93a3fbdce9fa1e5bae72900c0 2026-03-07 22:54:26 +0100 feat: MVP auto-demo â€” analyzer hybrid IPSO, demo_api, run_ab_tests, pytest pass
```

## Рекомендований наступний крок

Деплой (docs/DEPLOYMENT.md), потім python scripts/demo_api.py [URL]; git push origin main && git push gitlab main.

## Примітка

Файли даних (Fake.csv, True.csv) та модель (best_model.joblib) не комітяться в репо — вони лише локально. Після клону: python scripts/download_datasets.py та запуск ноутбука 01.

---

Після перезавантаження: запустіть `python scripts/next_step.py` та прочитайте **docs/CONTINUE_AFTER_PAUSE.md**.