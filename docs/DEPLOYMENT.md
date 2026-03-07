# Render та Railway — що це, як працює, покроковий деплой

Цей документ описує **що таке Render і Railway**, **як вони працюють**, і **покрокові дії** для деплою TruthLens UA API в межах безкоштовних/пробних лімітів.

---

## 1. Загальне порівняння

| | **Render** | **Railway** |
|---|------------|-------------|
| **Що це** | Хостинг для веб-сервісів, статики, бекендів, БД | Платформа для деплою додатків (бекенди, сервіси, БД) |
| **Як працює** | Підключаєте Git-репо (GitHub/GitLab), при push запускає збірку та деплой | Підключаєте репо або Railway CLI; збірка з Dockerfile або Nixpacks |
| **Безкоштовний план** | Є (обмежені години, sleep після неактивності) | Є trial/credits; потім платний |
| **Підходить для** | Demo, MVP, курсові/дипломи | Швидкий MVP, демо, прототипи |

Обидва сервіси **автоматично** збирають додаток з вашого коду та дають **публічний URL** (наприклад `https://truthlens-xxx.onrender.com` або `https://xxx.railway.app`).

---

## 2. Render — покроково

### Що робить Render
- Підключає репозиторій з GitHub/GitLab.
- При кожному push на обрану гілку запускає **build** (наприклад `pip install -r requirements.txt`) і **start** (наприклад `uvicorn src.api.main:app --host 0.0.0.0 --port $PORT`).
- Дає HTTPS-URL. На безкоштовному плані сервіс може “засинати” після неактивності; перший запит після цього буде повільнішим (cold start).

### Покрокові дії
1. **Реєстрація:** https://render.com → Sign Up (через GitHub зручно).  
2. **New → Web Service.**  
3. **Connect repository:** виберіть **102012dl/TruthLens** (або ваш репо).  
4. **Settings:**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn src.api.main:app --host 0.0.0.0 --port $PORT`
   - **Root Directory:** залишити порожнім, якщо корінь репо — корінь проєкту.
5. **Environment:** додати змінні при потребі (наприклад `MODEL_PATH` якщо модель на Render).  
6. **Create Web Service** — Render зробить перший деплой.  
7. Після успішного деплою з’явиться URL типу `https://truthlens-xxx.onrender.com`.  
   - Перевірка: `https://...onrender.com/health` та `https://...onrender.com/docs`.

### Важливо для проєкту
- У корені проєкту має бути **requirements.txt** (воно вже є).  
- Якщо використовується `artifacts/best_model.joblib`, його потрібно або включити в репо (якщо не дуже великий), або підвантажувати при старті з зовнішнього сховища і вказати шлях у `MODEL_PATH`.

---

## 3. Railway — покроково

### Що робить Railway
- Деплой з **GitHub** або через **Railway CLI** (`railway up`).
- Визначає середовище (Python/Node тощо) або використовує **Dockerfile**.
- Дає URL та можливість додати змінні середовища, тома, БД.

### Покрокові дії
1. **Реєстрація:** https://railway.app → Login with GitHub.  
2. **New Project** → **Deploy from GitHub repo** → виберіть **102012dl/TruthLens**.  
3. Railway визначить Python-проєкт. Якщо є **Dockerfile** — використає його; якщо ні — збереть за замовчуванням (Nixpacks).  
4. **Settings → Deploy:**
   - **Start Command:** `uvicorn src.api.main:app --host 0.0.0.0 --port $PORT`
   - Або залишити автовизначення, якщо в проєкті є `Procfile` або скрипт старту.
5. **Variables:** додати при потребі (наприклад `MODEL_PATH`).  
6. **Deploy** — Railway збере і запустить сервіс.  
7. **Settings → Generate Domain** — отримаєте URL типу `https://xxx.railway.app`.  
   - Перевірка: `/health`, `/docs`.

### CLI (опційно)
```bash
npm install -g @railway/cli
railway login
railway link   # прив’язати до існуючого проєкту
railway up     # задеплоїти поточну папку
railway domain # показати/створити домен
```

---

## 4. Що потрібно в репо для деплою

- **requirements.txt** — є.  
- **Старт API:** у обох платформах використовується команда на кшталт:
  ```bash
  uvicorn src.api.main:app --host 0.0.0.0 --port $PORT
  ```
  `$PORT` платформа підставляє сама.  
- Опційно: **Procfile** або **Dockerfile** для явного керування збіркою/стартом (нижче — приклад).

---

## 5. Приклад Procfile (для Render / Railway)

У корені проєкту можна додати файл **Procfile** (одний рядок):

```
web: uvicorn src.api.main:app --host 0.0.0.0 --port $PORT
```

Тоді Render/Railway зможуть використати цю команду для запуску веб-сервісу.

---

## 6. Підсумок

- **Render:** репо → Web Service → Build/Start команди → отримуєте URL; зручно для MVP та демо.  
- **Railway:** репо або CLI → деплой → Generate Domain → URL; також зручно для швидкого MVP.  
- Для TruthLens UA достатньо **requirements.txt** та команди запуску **uvicorn** з `$PORT`; при потребі додайте **Procfile** або **Dockerfile** і змінні середовища для моделі.

Після налаштування Git (див. **GIT_SETUP.md**) ви можете підключити той самий репо до Render і Railway і використовувати один репо для обох платформ.

---

## 7. Перевірка після деплою (демо-тексти)

Після отримання URL (наприклад `https://truthlens-xxx.onrender.com`):

```bash
python scripts/demo_api.py https://truthlens-xxx.onrender.com
```

Локально (коли API запущено на порту 8000):

```bash
uvicorn src.api.main:app --reload
# В іншому терміналі:
python scripts/demo_api.py
```

Скрипт викликає `/health` та `/api/analyze` для 8 демо-текстів (FAKE/REAL) — зручно для перевірки перед захистом.
