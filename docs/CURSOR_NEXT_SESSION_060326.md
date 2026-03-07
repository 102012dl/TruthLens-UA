# ═══════════════════════════════════════════════════════════════════════════════
# CURSOR AI — TRUTHLENS UA — NEXT SESSION PROMPT
# Стан після паузи: 05.03.2026 23:11
# Виконати: відкрити Cursor AI → Composer → Agent Mode → вставити цей файл
# ═══════════════════════════════════════════════════════════════════════════════

=== CURSOR AI — TRUTHLENS UA — CONTINUE AFTER PAUSE (06.03.2026) ===

## СТАН ПІСЛЯ ПАУЗИ (05.03.2026, 23:11)

### ✅ УЖЕ ЗРОБЛЕНО — НЕ ПОВТОРЮВАТИ:
- GitHub: github.com/102012dl/TruthLens-UA (синхронізовано, конфлікти вирішено)
- GitLab: gitlab.com/102012dl/truthlens-ua (синхронізовано)
- ISOT Data: data/True.csv (~53MB) + data/Fake.csv (~63MB) — завантажено
- best_model.joblib: artifacts/best_model.joblib — згенеровано з notebook 01
- Архітектура, код, API, тести — 90% готово

### ❌ ЗАЛИШИЛОСЬ (у порядку пріоритету):
1. notebooks/03_ua_nlp_training.ipynb — A/B тести + MLflow → DagsHub
2. Railway deploy — Python API live
3. 8 демо-текстів через /api/analyze
4. Скріншоти + план Розділу 3

---

## TASK 1 — NOTEBOOK 03 (A/B Tests + MLflow) — 20 хв

### Перевірити чи існує notebook 03:
```bash
ls notebooks/03_ua_nlp_training.ipynb 2>/dev/null && echo "EXISTS" || echo "CREATE"
```

### Якщо НЕ існує — створити:
```python
# notebooks/03_ua_nlp_training.ipynb
# Створити через: jupyter nbconvert або написати Python скрипт

import pandas as pd
import joblib
import mlflow
import mlflow.sklearn
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, accuracy_score
import time

# Load ISOT (already downloaded)
import os
true_df = pd.read_csv("data/True.csv")
fake_df = pd.read_csv("data/Fake.csv")
true_df["label"] = "REAL"
fake_df["label"] = "FAKE"
df = pd.concat([true_df, fake_df]).sample(frac=1, random_state=42)
df["text"] = (df.get("title", "") + " " + df.get("text", "")).str.strip()
X = df["text"].values
y = df["label"].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# A/B Test — 4 models
mlflow.set_experiment("ab-test-ukraine-nlp")

models = {
    "LinearSVC_C1":   LinearSVC(max_iter=10000, C=1.0),
    "LinearSVC_C05":  LinearSVC(max_iter=10000, C=0.5),
    "LogisticReg":    LogisticRegression(max_iter=1000),
    "RandomForest":   RandomForestClassifier(n_estimators=100, random_state=42),
}

results = {}
for name, clf in models.items():
    with mlflow.start_run(run_name=f"AB_{name}"):
        mlflow.set_tags({
            "ab_test": True,
            "student": "102012dl",
            "language": "ua+en",
            "dataset": "ISOT_39103",
        })
        pipe = Pipeline([
            ("tfidf", TfidfVectorizer(max_features=50000, ngram_range=(1,2), min_df=2)),
            ("clf", clf),
        ])
        t0 = time.time()
        pipe.fit(X_train, y_train)
        latency = round((time.time() - t0) * 1000)
        
        preds = pipe.predict(X_test)
        f1 = f1_score(y_test, preds, average="weighted")
        acc = accuracy_score(y_test, preds)
        
        mlflow.log_metrics({"f1": f1, "accuracy": acc, "latency_ms": latency})
        mlflow.sklearn.log_model(pipe, f"model_{name}")
        results[name] = {"f1": f1, "acc": acc, "lat": latency}
        print(f"{name}: F1={f1:.4f} | Acc={acc:.4f} | Lat={latency}ms")

best = max(results, key=lambda k: results[k]["f1"])
print(f"\n🏆 WINNER: {best} (F1={results[best]['f1']:.4f})")
print("\n=== MLflow A/B Test Complete ===")
```

### Запустити як скрипт (якщо nbconvert недоступний):
```bash
python scripts/run_ab_tests.py
# або
jupyter nbconvert --to notebook --execute notebooks/03_ua_nlp_training.ipynb
```

### DagsHub публікація:
```bash
pip install dagshub --quiet
python -c "
import dagshub, mlflow
dagshub.init(repo_owner='102012dl', repo_name='TruthLens', mlflow=True)
print('DagsHub URI:', mlflow.get_tracking_uri())
"
# Скопіювати URI в .env: MLFLOW_TRACKING_URI=https://dagshub.com/...
```

---

## TASK 2 — RAILWAY DEPLOY — 15 хв

```bash
# Перевірити Railway CLI
railway --version 2>/dev/null || npm install -g @railway/cli

# Логін
railway login

# Деплой (з кореня проєкту)
railway link  # вибрати або створити проєкт TruthLens-UA
railway up

# Отримати URL
RAILWAY_URL=$(railway domain 2>/dev/null || echo "")
echo "Railway URL: $RAILWAY_URL"

# КРИТИЧНА перевірка
curl -s "$RAILWAY_URL/health" | python3 -c "
import sys, json
d = json.load(sys.stdin)
loaded = d.get('model_loaded', False)
print('model_loaded:', loaded)
if not loaded:
    print('❌ MODEL NOT LOADED — перевір MODEL_PATH env var!')
    print('   Set in Railway: MODEL_PATH=artifacts/best_model.joblib')
else:
    print('✅ Railway API ready!')
"

# ЯКЩО model_loaded=false:
# railway variables set MODEL_PATH=artifacts/best_model.joblib
# railway redeploy
```

### Оновити Replit з Railway URL:
```bash
# В Replit → Settings → Secrets:
# PYTHON_API_URL = https://YOUR-APP.railway.app
# Перезапустити Replit backend
```

---

## TASK 3 — 8 DEMO TEXTS через API — 10 хв

```bash
# Встановити змінну
RAILWAY_URL="https://YOUR-APP.up.railway.app"  # замінити реальним URL

# --- ТЕСТ 1: FAKE (ІПСО-атака) ---
echo "=== TEST 1: UA ІПСО ==="
curl -s -X POST "$RAILWAY_URL/api/analyze" \
  -H "Content-Type: application/json" \
  -d '{"text": "ТЕРМІНОВО!!! ЗСУ ЗДАЛИ Харків! Зеленський підписав капітуляцію! Поширте до видалення!"}' \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'Label: {d[\"label\"]} | Score: {d[\"fake_score\"]} | ІПСО: {d.get(\"ipso_techniques\",[][:2])}')"
# ОЧІКУЄТЬСЯ: FAKE, score > 0.80

# --- ТЕСТ 2: REAL (офіційне) ---
echo "=== TEST 2: REAL Official ==="
curl -s -X POST "$RAILWAY_URL/api/analyze" \
  -H "Content-Type: application/json" \
  -d '{"text": "НБУ підвищив облікову ставку до 16% річних. Рішення ухвалено на засіданні Правління."}' \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'Label: {d[\"label\"]} | Score: {d[\"fake_score\"]}')"
# ОЧІКУЄТЬСЯ: REAL, score < 0.30

# --- ТЕСТ 3: КРИТИЧНИЙ ВИПРАВЛЕННЯ ---
echo "=== TEST 3: COFFEE (CRITICAL FIX) ==="
curl -s -X POST "$RAILWAY_URL/api/analyze" \
  -H "Content-Type: application/json" \
  -d '{"text": "Scientists discover coffee makes you live forever and cures all cancer!"}' \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'Label: {d[\"label\"]} | Score: {d[\"fake_score\"]} — Expected: NOT REAL!')"
# ОЧІКУЄТЬСЯ: FAKE або SUSPICIOUS (НЕ REAL 75%!)

# --- ТЕСТ 4: REAL (kmu.gov.ua) ---
curl -s -X POST "$RAILWAY_URL/api/analyze" \
  -H "Content-Type: application/json" \
  -d '{"text": "Кабінет Міністрів затвердив програму підтримки малого бізнесу. Фінансування 12 млрд грн."}'

# --- ТЕСТ 5: FAKE (Антивакс) ---
curl -s -X POST "$RAILWAY_URL/api/analyze" \
  -H "Content-Type: application/json" \
  -d '{"text": "Уряд ПРИХОВУЄ правду про вакцини!!! Лікарі мовчать бо їм платять! Прокидайтесь люди!!!"}'

# --- ТЕСТ 6: SUSPICIOUS (DeepFake) ---
curl -s -X POST "$RAILWAY_URL/api/analyze" \
  -H "Content-Type: application/json" \
  -d '{"text": "Зеленський у відеозверненні заявив про капітуляцію. Відео набрало 2 млн переглядів."}'

# --- ТЕСТ 7: FAKE (5G) ---
curl -s -X POST "$RAILWAY_URL/api/analyze" \
  -H "Content-Type: application/json" \
  -d '{"text": "5G ВЕЖІ ЗАРАЖАЮТЬ ЛЮДЕЙ ЧЕРЕЗ COVID!!! Правда яку приховує ВООЗ! Перешли усім!!!"}'

# --- ТЕСТ 8: REAL (Параолімпіада) ---
curl -s -X POST "$RAILWAY_URL/api/analyze" \
  -H "Content-Type: application/json" \
  -d '{"text": "Польська телерадіокомпанія TVP оголосила про трансляцію Параолімпійських ігор 2026 у Мілані."}'

echo "=== All 8 demo texts tested ==="
```

---

## TASK 4 — SCREENSHOTS — 15 хв

```bash
# Зробити screenshots (вручну або через automation):

# 1. Replit Analyze tab — вставити текст FAKE → показати результат
# URL: https://replit.com/@102012dl/Truth-Lens-Factory

# 2. Replit History tab — 26+ записів

# 3. Replit Statistics tab — графіки

# 4. Railway Swagger UI: $RAILWAY_URL/docs

# 5. DagsHub MLflow: dagshub.com/102012dl/TruthLens.mlflow
#    → Experiments → ab-test-ukraine-nlp → 4+ runs

# 6. GitHub Actions: github.com/102012dl/TruthLens-UA/actions
#    → CI green badge

# Зберегти в: docs/screenshots/
mkdir -p docs/screenshots
# Назвати: 01_replit_analyze_fake.png, 02_replit_history.png, etc.
```

---

## TASK 5 — GIT FINAL COMMIT — 5 хв

```bash
# Після виконання tasks 1-4:
git add -A
git commit -m "feat: A/B MLflow tests + Railway deploy + 8 demo texts verified

- notebooks/03_ua_nlp_training.ipynb: 4 models, A/B comparison
- MLflow: ab-test-ukraine-nlp experiment (DagsHub public)
- Railway URL: live, model_loaded=true
- 8 UA demo texts: FAKE/REAL/SUSPICIOUS verified
- docs/screenshots/: 6+ screenshots"

git tag v1.1.0-demo -m "Demo ready: Railway+MLflow+8texts"
git push origin main --tags
git push gitlab main --tags

echo "🎉 Demo ready! v1.1.0-demo"
```

---

## ОЧІКУВАНІ РЕЗУЛЬТАТИ

| Компонент | Після TASK 1-5 | Прогноз оцінки |
|-----------|---------------|----------------|
| MLflow A/B | 4+ runs DagsHub | +5 MVP балів |
| Railway API | model_loaded: true | +8 MVP балів |
| Demo texts | 8/8 correct | +4 MVP балів |
| Screenshots | 6+ images | +3 Docs балів |
| **РАЗОМ** | **77 → 95/100** | **A/A+** |

---

## ЯКЩО ЩОСЬ ПІШЛО НЕ ТАК

### Railway model_loaded=false:
```bash
# Перевірити env vars
railway variables list | grep MODEL
# Встановити
railway variables set MODEL_PATH=artifacts/best_model.joblib
railway redeploy
```

### MLflow не пише в DagsHub:
```bash
# Перевірити token
echo $DAGSHUB_TOKEN
# Якщо порожньо — otrimati з dagshub.com → Settings → Tokens
export DAGSHUB_TOKEN=your_token_here
```

### Notebook 03 помилка пам'яті:
```bash
# Використати менший датасет
# Замінити в коді: df = df.sample(10000, random_state=42)
```

---
# END — TRUTHLENS UA NEXT SESSION PROMPT
# Час виконання: ~60-75 хвилин для tasks 1-5
# Після цього: тільки Thesis Section 3 (~90 хв) і ти ГОТОВИЙ!
# ═══════════════════════════════════════════════════════════════════════════════
