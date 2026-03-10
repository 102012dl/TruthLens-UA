# TruthLens UA — AI-Powered Information Credibility Analysis Platform

Status | Python | License | Coverage  
------ | ------ | ------- | --------  
MVP | 3.11+ | MIT (як у TruthLens) | pytest + pytest-cov  

Capstone Project \| Neoversity \| Master of Science in Computer Science  
Author: **102012dl** \| Email: **102012dl@gmail.com**

**Repository:** https://github.com/102012dl/TruthLens-UA  
**GitLab mirror (CI/CD):** https://gitlab.com/102012dl/truthlens-ua (user **102012dl**, не group)  

Backend MVP for **TruthLens UA**, a Ukrainian/English fake news and information-operations (ІПСО) detector.

---

## 📋 Зміст

- **🎯 Огляд проєкту**
- **🏗 Архітектура**
- **🛠 Технології**
- **🚀 Швидкий старт**
- **🧠 ML Pipeline**
- **📡 API Документація**
- **🔄 CI/CD & Security**
- **📦 Deployment**
- **📄 Ліцензія**
- **👨‍💻 Автор**

---

## 🎯 Огляд проєкту

**TruthLens UA** — це практичний MVP для виявлення фейкових новин та ІПСО-маніпуляцій українською й англійською мовами.  
Сервіс поєднує **ML-модель (LinearSVC + TF-IDF)** з **правиловим аналізом 10+ ІПСО-технік**, повертаючи не лише класифікацію FAKE/REAL/SUSPICIOUS, а й пояснення, чому текст підозрілий.

Основні сценарії:
- швидка перевірка новин/постів через **API** або **Streamlit-дашборд**;
- мобільне використання через **Telegram-бота**;
- демонстрація повного ML/ІПСО-pipeline для диплому/захисту/менторського перегляду.

---

## 🏗 Архітектура

Кодова база спрощена від початкового проєкту **TruthLens**, зосереджена на MVP:

- `src/ml/analyzer.py` — гібридний аналізатор (LinearSVC + UA ІПСО rule-based fallback).
- `src/api/main.py` — FastAPI backend з ендпоінтами:
  - `/` — кореневий health/info.
  - `/health` — статус сервісу та моделі.
  - `/api/analyze` — аналіз одного тексту.
  - `/api/models` — інформація про наявні моделі.
  - `/api/stats` — агрегована статистика викликів.
- `scripts/truthlens_dashboard.py` — Streamlit-дешборд (Analyze, History, Statistics, QR).
- `scripts/demo_api.py`, `scripts/demo_mvp_like_replit.py`, `scripts/demo_streamlit_flow.py` — демо-скрипти для Render API і локального потоку.
- `tests/unit/test_ml_validation.py` — юніт-тести для ML та ІПСО-логіки.
- `data/` — датасет ISOT (Fake/True) у форматі CSV.
- `artifacts/best_model.joblib` — навчена ML-модель.

Детальний аналіз зв’язку з оригінальним репо TruthLens — у `docs/TRUTHLENS_REPO.md`.

---

## 🛠 Технології

- **Мова та фреймворки:** Python 3.11+, FastAPI, Pydantic, Streamlit.
- **ML/NLP:** scikit-learn (LinearSVC, TF-IDF), rule-based ІПСО-аналіз.
- **MLOps:** MLflow (notebooks, експерименти), joblib (серіалізація моделі).
- **Інфраструктура:** Render (API), GitHub Actions + GitLab CI, можливість Docker-образів.
- **Тестування:** pytest, pytest-cov, ruff.

---

## 🚀 Швидкий старт (локальний запуск)

### 1. Створення середовища та встановлення залежностей

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# або source .venv/bin/activate для Linux/Mac

pip install -r requirements.txt
```

### 2. Запуск API (FastAPI)

```bash
uvicorn src.api.main:app --reload
```

Після цього відкрийте в браузері:
- `http://localhost:8000/` — базова сторінка.
- `http://localhost:8000/docs` — Swagger UI для тестування `/api/analyze`, `/api/stats`, `/api/models`.

---

## 📡 API Документація та live-демо

- **API (Render, стабільне посилання для ментора/презентації):** `https://truthlens-ua.onrender.com`
- **Swagger (документація API):** `https://truthlens-ua.onrender.com/docs`
- **Health:** `https://truthlens-ua.onrender.com/health`
- **GitHub репозиторій:** `https://github.com/102012dl/TruthLens-UA`
- **GitLab mirror:** `https://gitlab.com/102012dl/truthlens-ua`

Деталі щодо деплою та посилань: `docs/MVP_DEPLOY_AND_LINKS.md`.

---

## 🧠 ML Pipeline, дані та модель

- Дані: **ISOT Fake News Dataset** (UVic), автоматичне завантаження описано в:
  - `scripts/download_datasets.py`
  - `docs/TRUTHLENS_REPO.md`
- Локальні файли:
  - `data/Fake.csv`
  - `data/True.csv`
- Модель:
  - `artifacts/best_model.joblib` — навчена модель (LinearSVC + TF-IDF) для класифікації FAKE/REAL.
- Надбудова:
  - 10+ правил ІПСО для пояснення, чому текст позначається як SUSPICIOUS / ризикований.

Ноутбуки з A/B-експериментами та MLflow — див. `notebooks/` (опис у `docs/REPORT_080326_2213.md`).

---

## ✅ Тести та валідація

Запуск усіх тестів:

```bash
pytest
```

Станом на 10.03.2026:
- `7` тестів зібрано.
- **6 passed, 1 skipped, 0 failed**.

Основний файл:
- `tests/unit/test_ml_validation.py` — перевіряє коректність роботи аналізатора та ІПСО-логіки.

Конфігурація pytest:
- `pytest.ini` з `pythonpath = .` (щоб модуль `src` коректно імпортувався в тестах).

---

## 📦 Deployment / Render

Сервіс розгорнуто на **Render** із підключенням до гілки `main` репозиторію GitHub:

- API доступне за адресою `https://truthlens-ua.onrender.com`.
- Точки доступу:
  - `/` — кореневий health/info.
  - `/health` — технічний статус.
  - `/docs` — Swagger.
  - `/api/analyze`, `/api/stats`, `/api/models` — основні ендпоінти MVP.

Докладніше про деплой та сценарії використання — у `docs/DEPLOYMENT.md`, `docs/MVP_DEPLOY_AND_LINKS.md`.

---

## 📱 Мобільна / Telegram версія та дашборд MVP

### Streamlit-дешборд (локальний Web/UI)

- **Дашборд MVP** (Analyze, History, Statistics, QR Code; кольорове кодування, автооновлення статистики, App URL):

```bash
pip install streamlit requests pandas qrcode[pil]
streamlit run scripts/truthlens_dashboard.py
```

- Відкрити в браузері: `http://localhost:8501`.
- Модулі:
  - **Analyze** — введення тексту, класифікація FAKE/REAL/SUSPICIOUS з поясненнями.
  - **History** — історія запитів.
  - **Statistics** — графіки та агрегати (автооновлення кожні 30 с).
  - **QR / Mobile Access** — QR-код для Telegram/Web-варіанту.

### Telegram Bot / мобільний доступ

- **Telegram Bot:** `https://t.me/truthlens_ai_bot`
- Використовується як мобільна версія MVP; QR-код для швидкого доступу доступний на сторінці дашборду.

Деталі: `docs/MVP_DEPLOY_AND_LINKS.md`.

---

## 🔄 CI/CD & Security

- **GitHub Actions:** при `push` у `main`:
  - lint (ruff),
  - unit-тести (pytest),
  - ML validation,
  - за потреби — Docker build та інші кроки.
- **GitLab mirror:** той самий код запускається в GitLab CI (див. `.gitlab-ci.yml`).
  - Щоб увімкнути mirror, додайте `GITLAB_SSH_KEY` у GitHub Secrets і дотримуйтесь інструкцій у `docs/GITLAB_MIRROR.md`.

CI/CD і деплой детально описані в `docs/MVP_DEPLOY_AND_LINKS.md`, `docs/GITLAB_MIRROR.md`.

---

## 📄 Ліцензія

Проєкт слідує тій самій ліцензійній моделі, що й оригінальний TruthLens (MIT).  
Деталі див. у вихідному репозиторії TruthLens та супровідній документації курсу Neoversity.

---

## 👨‍💻 Автор

- **Автор:** 102012dl  
- **Email:** 102012dl@gmail.com  
- **GitHub:** https://github.com/102012dl  


