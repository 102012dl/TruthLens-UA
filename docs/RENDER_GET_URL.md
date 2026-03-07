# Як отримати https://ваш-url.onrender.com (Render)

**Проблема:** у документації написано «ваш-url» — це **плейсхолдер**. Потрібен **реальний URL**, який Render видасть після реєстрації та створення сервісу.

---

## Покрокова реєстрація та отримання URL

### 1. Реєстрація на Render

1. Відкрийте **https://render.com** у браузері.
2. Натисніть **Get Started** або **Sign Up**.
3. Оберіть **Sign up with GitHub** (зручно: Render побачить ваші репо).
4. Увійдіть у GitHub, якщо потрібно, і дозвольте Render доступ до облікового запису.

### 2. Створення Web Service

1. У панелі Render натисніть **New +** → **Web Service**.
2. У блоці **Connect a repository**:
   - Якщо репо вже підключено — виберіть **102012dl/TruthLens-UA** (або вашу назву репо).
   - Якщо ні — натисніть **Connect account** / **Configure account** і виберіть репо **TruthLens-UA**, потім знову виберіть його в списку.
3. Заповніть поля:
   - **Name:** `truthlens-ua` (або будь-яка назва латиницею — вона потрапить у URL).
   - **Region:** залишити за замовчуванням.
   - **Branch:** `main`.
   - **Root Directory:** порожньо.
   - **Runtime:** Python 3.
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn src.api.main:app --host 0.0.0.0 --port $PORT`
4. Натисніть **Create Web Service**.

### 3. Де взяти URL

1. Після створення сервісу Render почне збірку (Build) і потім запуск (Deploy).
2. Угорі сторінки сервісу є поле **URL** або посилання типу:
   ```text
   https://truthlens-ua.onrender.com
   ```
   (замість `truthlens-ua` буде **Name**, який ви вказали кроком раніше).
3. Скопіюйте цей URL — це і є **ваш реальний URL**.

### 4. Перевірка

- Відкрийте в браузері: `https://ВАШ-URL.onrender.com/health`  
  Має з’явитися JSON з `"status": "ok"` (після успішного деплою).
- Документація API: `https://ВАШ-URL.onrender.com/docs`

### 5. Запуск демо-скрипта з реальним URL

У терміналі (замініть на свій URL):

```powershell
python scripts/demo_api.py https://truthlens-ua.onrender.com
```

Або через змінну середовища:

```powershell
$env:TRUTHLENS_API_URL = "https://truthlens-ua.onrender.com"
python scripts/demo_api.py
```

---

## Важливо

- **Не підставляйте буквально «ваш-url»** — це лише приклад. Потрібен URL, який показує Render у дашборді.
- URL має містити **лише латиницю, цифри, крапку, двокрапку, слеш** (наприклад `https://truthlens-ua.onrender.com`). Якщо в URL будуть кириличні літери, скрипт покаже помилку та підказку.
- Перший запит після «засипання» сервісу на безкоштовному плані може тривати 30–60 секунд (cold start).

Детальніші налаштування деплою: **docs/DEPLOYMENT.md**.
