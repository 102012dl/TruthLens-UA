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
| **Environment Variables** | **Обовʼязково додати:** `PYTHON_VERSION` = `3.12.7` (щоб уникнути збірки pydantic на Python 3.14). Опційно: `MODEL_PATH` = `artifacts/best_model.joblib` | Див. **docs/RENDER_PYTHON_VERSION.md**. |

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

Render використовує **Python 3.14** за замовчуванням. Сервіс типу «Python 3 Web Service» **не використовує Dockerfile** з репо — тільки Build Command. Тому потрібно вказати версію Python через змінну середовища.

**Рішення (зробіть у Render Dashboard):**

1. Відкрийте сервіс **truthlens-ua** → **Environment**.
2. Додайте змінну: **Key** = `PYTHON_VERSION`, **Value** = `3.12.7`.
3. Збережіть і натисніть **Manual Deploy** → **Deploy latest commit**.

Детально: **docs/RENDER_PYTHON_VERSION.md**.

---

## Render MCP Server (опційно)

Керування сервісами Render з Cursor/Claude: [Render MCP](https://render.com/docs/mcp). Підключення MCP дає можливість запускати деплой, переглядати логи, змінні середовища з AI-середовища. Для деплою TruthLens-UA достатньо веб-дашборду Render; MCP — для автоматизації.

Детальніше: **docs/RENDER_GET_URL.md**, **docs/DEPLOYMENT.md**.
