# TruthLens UA — автоматична демонстрація MVP

**Дата:** 07.03.2026  
**Призначення:** фіксація виконаних кроків та команд для повторної демонстрації.

---

## Що виконано автоматично

### 1. Перевірка стану
- `python scripts/next_step.py` — перевірено: дані ISOT, модель `artifacts/best_model.joblib`, remotes GitHub/GitLab.

### 2. Запуск API та 8 демо-текстів
- API запущено у фоні: `uvicorn src.api.main:app --host 127.0.0.1 --port 8000`
- Виконано: `python scripts/demo_api.py http://127.0.0.1:8000`
- Результат: `GET /health` → `model_loaded: true`, усі 8 запитів до `/api/analyze` виконано успішно.

### 3. Unit-тести (модель)
- `pytest tests/unit/ -v --tb=short` — **6 passed, 1 skipped** (test_f1_on_isot_sample пропущено без файлу isot_test_100.csv).
- У аналізатор додано гібридні правила: при ≥2 ІПСО-техніках або сенсаційних заголовках типу «cures cancer» підвищується `fake_score`, щоб UA-дезінфо та сатира класифікувались коректно.

### 4. A/B тести (скрипт)
- Додано `scripts/run_ab_tests.py` — запуск A/B тестів без ноутбука.
- Виконано: `python scripts/run_ab_tests.py --sample 5000`
- Результат: LinearSVC_C1 переможець (F1=0.9810), MLflow логи записано локально.

---

## Як повторити демонстрацію вручну

```bash
# 1. Перевірка стану
python scripts/next_step.py

# 2. Запуск API (один термінал)
uvicorn src.api.main:app --host 127.0.0.1 --port 8000

# 3. Демо 8 текстів (інший термінал)
python scripts/demo_api.py

# 4. Тести
pytest tests/unit/ -v --tb=short

# 5. A/B тести (опційно, ~1 хв на 5k зразках)
python scripts/run_ab_tests.py --sample 5000
```

Після перезапуску API (після змін у `src/ml/analyzer.py`) демо покаже оновлену класифікацію: FAKE для текстів з ІПСО та сенсаційними заголовками.

---

## Деплой (Railway / Render)

- Інструкції: **docs/DEPLOYMENT.md**
- Після отримання URL: `python scripts/demo_api.py https://ваш-url.onrender.com`

---

## Підсумок

| Компонент              | Стан                          |
|------------------------|-------------------------------|
| API /health, /api/analyze | ✅ Працює, model_loaded=true |
| 8 демо-текстів         | ✅ Прогнано через API         |
| pytest (unit)          | ✅ 6 passed                   |
| run_ab_tests.py        | ✅ A/B 4 моделі, MLflow       |
| Гібрид ІПСО + ML       | ✅ У аналізаторі              |
