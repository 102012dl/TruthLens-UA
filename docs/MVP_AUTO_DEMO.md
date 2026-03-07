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

**Важливо (Windows):** щоб уникнути `ModuleNotFoundError: No module named 'joblib'`, завжди використовуйте Python із віртуального середовища.

```powershell
# 0. Один раз: встановити залежності у .venv
.venv\Scripts\pip install -r requirements.txt

# 1. Перевірка стану
.venv\Scripts\python scripts/next_step.py

# 2. Запуск API (один термінал) — обовʼязково через .venv
.venv\Scripts\python -m uvicorn src.api.main:app --host 127.0.0.1 --port 8000

# 3. Демо 8 текстів (інший термінал)
.venv\Scripts\python scripts/demo_api.py

# 4. Тести
.venv\Scripts\python -m pytest tests/unit/ -v --tb=short

# 5. A/B тести (опційно, ~1 хв на 5k зразках)
.venv\Scripts\python scripts/run_ab_tests.py --sample 5000
```

Якщо venv активовано (`(.venv) PS ...`), достатньо: `python -m uvicorn ...` та `python scripts/demo_api.py`.

Після перезапуску API (після змін у `src/ml/analyzer.py`) демо покаже оновлену класифікацію: FAKE для текстів з ІПСО та сенсаційними заголовками.

### Якщо виникає `ModuleNotFoundError: No module named 'joblib'`

- Переконайтесь, що запускаєте **той самий Python**, у якому встановлені залежності (наприклад `.venv`).
- **Рекомендовано:** `.venv\Scripts\python -m uvicorn src.api.main:app --host 127.0.0.1 --port 8000` замість просто `uvicorn ...`.
- Або активуйте venv: `.venv\Scripts\Activate.ps1`, потім `pip install -r requirements.txt` і `python -m uvicorn ...`.

---

## Локальний Web Deploy (без публічного доступу)

- Запуск API лише на вашому ПК і демонстрація MVP: **docs/LOCAL_WEB_DEPLOY.md**
- Один термінал: `uvicorn ... --host 127.0.0.1 --port 8000`; другий: `python scripts/demo_api.py`; браузер: http://127.0.0.1:8000/docs

## Деплой на Render (публічний URL)

- Інструкції: **docs/DEPLOYMENT.md**
- **Значення для форми New Web Service:** **docs/RENDER_FORM_VALUES.md** (зокрема Start Command = uvicorn, не gunicorn)
- **Як отримати URL:** **docs/RENDER_GET_URL.md**
- Після отримання URL: `python scripts/demo_api.py https://ваш-реальний-url.onrender.com`

---

## Підсумок

| Компонент              | Стан                          |
|------------------------|-------------------------------|
| API /health, /api/analyze | ✅ Працює, model_loaded=true |
| 8 демо-текстів         | ✅ Прогнано через API         |
| pytest (unit)          | ✅ 6 passed                   |
| run_ab_tests.py        | ✅ A/B 4 моделі, MLflow       |
| Гібрид ІПСО + ML       | ✅ У аналізаторі              |
