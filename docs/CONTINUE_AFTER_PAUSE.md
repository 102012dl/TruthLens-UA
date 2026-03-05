# Продовження роботи після паузи чи перезавантаження

Цей документ описує **найкращий спосіб** продовжити виконання проєкту TruthLens-UA після вимкнення/вмикання комп'ютера або довгої паузи.

---

## 1. Що зберігається автоматично

- **Код і документація** — у Git (GitHub + GitLab). Після `git pull` у вас завжди актуальний код.
- **Стан проєкту** — у файлах **docs/PROJECT_STATE.md** та **docs/PROJECT_STATE.json**. Їх оновлює скрипт `python scripts/update_project_state.py` (або ви вручну після важливих кроків).
- **Файли даних і модель** (Fake.csv, True.csv, best_model.joblib) **не комітяться** в репо (великі, у .gitignore). Вони лише **локально** на вашому диску. Якщо ви клонували репо на іншому ПК — потрібно знову завантажити дані та/або натренувати модель (див. нижче).

---

## 2. Кроки після перезавантаження (на тому ж комп’ютері)

1. Відкрийте проєкт у Cursor (або термінал у корені проєкту).
2. Запустіть перевірку стану:
   ```bash
   python scripts/next_step.py
   ```
3. Відкрийте **docs/PROJECT_STATE.md** — там поточний чеклист і рекомендований наступний крок.
4. Якщо потрібно оновити запис стану (наприклад, після push або тренування):
   ```bash
   python scripts/update_project_state.py
   ```
5. Синхронізація репо (якщо були локальні зміни):
   ```bash
   git add -A
   git status
   git commit -m "опис змін"
   git push origin main
   git push gitlab main
   ```

---

## 3. Якщо ви клонували репо на новому ПК

- У репо **немає** файлів даних і моделі (вони в .gitignore). Тому:
  1. Завантажте дані: `python scripts/download_datasets.py`
  2. Запустіть ноутбук 01: `notebooks/01_isot_fake_news_mlflow.ipynb` (Run All) — з’явиться `artifacts/best_model.joblib`
  3. Далі: `python scripts/next_step.py` та **docs/NEXT_STEP.md**

---

## 4. Регулярні коміти (рекомендовано)

- Після кожної логічної зміни: `git add -A`, `git commit -m "..."`, `git push origin main` та при потребі `git push gitlab main`.
- Періодично оновлюйте стан: `python scripts/update_project_state.py`, потім закомітьте `docs/PROJECT_STATE.md` та `docs/PROJECT_STATE.json`, щоб прогрес був зафіксований у репо.

---

## 5. Перевірка репо GitHub/GitLab на наявність файлів

- У **репо** завжди мають бути: код (src/, scripts/, notebooks/, tests/), документація (docs/), README, .gitignore, CI (.github/workflows/).
- У репо **немає** і не має бути: `data/Fake.csv`, `data/True.csv`, `artifacts/best_model.joblib` (вони в .gitignore). Це правильна політика — дані та модель відновлюються локально за інструкціями вище.

Перевірити, що в репо є все необхідне для збірки та деплою:
- На GitHub: https://github.com/102012dl/TruthLens-UA
- На GitLab: https://gitlab.com/102012dl/truthlens-ua
