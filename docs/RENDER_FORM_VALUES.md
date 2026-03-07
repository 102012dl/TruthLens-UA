# Render — дані для форми New Web Service (TruthLens-UA)

Скопіюйте ці значення у форму **New Web Service** на Render. У поточному вигляді форма пропонує **gunicorn** — для FastAPI потрібен **uvicorn**.

---

## Заповнені поля (по порядку)

| Поле | Значення | Примітка |
|------|----------|----------|
| **Source Code** | `102012dl / TruthLens-UA` | Вже обрано. |
| **Name** | `TruthLens-UA` або `truthlens-ua` | Унікальна назва; потрапляє в URL. Рекомендовано: `truthlens-ua` (малими). |
| **Language** | `Python 3` | Вже обрано. |
| **Branch** | `main` | Вже обрано. |
| **Region** | `Oregon (US West)` або будь-який | За бажанням. |
| **Root Directory** | *(порожньо)* | Залишити порожнім — корінь репо = корінь проєкту. |
| **Build Command** | `pip install -r requirements.txt` | Вже заповнено. |
| **Start Command** | **Замінити на:** `uvicorn src.api.main:app --host 0.0.0.0 --port $PORT` | **Не залишати** `gunicorn your_application.wsgi` — це для Django; у проєкті FastAPI. |
| **Instance Type** | `Free` | Для демо достатньо. |
| **Environment Variables** | Опційно додати (якщо потрібно): `MODEL_PATH` = `artifacts/best_model.joblib` | Модель у репо не комітиться; на Free без диску можна не додавати — працюватиме rule-based fallback. |

---

## Що обовʼязково змінити

У полі **Start Command** замість:

```text
gunicorn your_application.wsgi
```

вставити:

```text
uvicorn src.api.main:app --host 0.0.0.0 --port $PORT
```

Після цього натиснути **Deploy web service**. Після успішного деплою зʼявиться URL типу `https://truthlens-ua.onrender.com` (або як ви назвали сервіс).

---

## Якщо збірка падає (Exited with status 1, pydantic-core / maturin / Read-only file system)

Render може використати **Python 3.14**, ігноруючи `runtime.txt` — тоді pip намагається зібрати `pydantic-core` з вихідників (Rust) і падає.

**Рішення: у репо додано Dockerfile.** Якщо в корені є **Dockerfile**, Render автоматично збирає образ через Docker (базовий образ `python:3.12-slim`) і не використовує Python 3.14. Після push і **Manual Deploy** збірка має пройти.

Якщо сервіс було створено як "Python 3" (Build Command / Start Command), Render все одно підхопить Dockerfile при наступному деплої. Переконайтесь, що **Dockerfile** і **.dockerignore** закомічені, потім **Manual Deploy** → **Deploy latest commit**.

---

## Render MCP Server (опційно)

Керування сервісами Render з Cursor/Claude: [Render MCP](https://render.com/docs/mcp). Підключення MCP дає можливість запускати деплой, переглядати логи, змінні середовища з AI-середовища. Для деплою TruthLens-UA достатньо веб-дашборду Render; MCP — для автоматизації.

Детальніше: **docs/RENDER_GET_URL.md**, **docs/DEPLOYMENT.md**.
