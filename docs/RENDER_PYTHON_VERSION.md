# Render: як вказати Python 3.12 (усунення помилки збірки)

Якщо збірка падає з помилкою **pydantic-core** / **maturin** / **Read-only file system**, Render використовує **Python 3.14**, для якого немає готових пакетів. Потрібно примусово вказати **Python 3.12**.

---

## Що зробити в Render Dashboard (обовʼязково)

1. Відкрийте **https://dashboard.render.com** і виберіть сервіс **truthlens-ua**.
2. У лівій панелі натисніть **Environment** (або вкладку **Environment**).
3. Натисніть **Add Environment Variable** (або **Add Variable**).
4. Введіть:
   - **Key:** `PYTHON_VERSION`
   - **Value:** `3.12.7`
5. Натисніть **Save Changes**.
6. Перейдіть на головну сторінку сервісу і натисніть **Manual Deploy** → **Deploy latest commit**.

Після цього Render встановить Python 3.12.7 під час збірки, і `pydantic-core` встановиться з готових пакетів без помилки.

---

## Чому це потрібно

- Сервіс створено як **Python 3 Web Service** (не Docker). У такому режимі Render **не використовує Dockerfile** з репо, а запускає свій Python (за замовчуванням 3.14).
- Змінна середовища **PYTHON_VERSION** — офіційний спосіб вказати версію Python на Render: [render.com/docs/python-version](https://render.com/docs/python-version).

---

## Після успішного деплою

- Перевірка: https://truthlens-ua.onrender.com/health  
- Демо: `python scripts/demo_api.py https://truthlens-ua.onrender.com`
