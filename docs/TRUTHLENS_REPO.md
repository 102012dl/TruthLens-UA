# Аналіз репо TruthLens (github.com/102012dl/TruthLens)

**Репо:** https://github.com/102012dl/TruthLens  
**Проєкт TruthLens-UA** (цей) — https://github.com/102012dl/TruthLens-UA  

---

## Що перевірено

- Репо **TruthLens** існує, гілки: `main`, `master`, `cursor/development-environment-setup-04e7`.
- У репо **немає** файлів даних у репозиторії: `Fake.csv`, `True.csv` не комітяться (великі датасети).
- Ноутбук **notebooks_01_isot_fake_news_detection_mlflow.ipynb** у TruthLens містить **автозавантаження ISOT** з UVic:
  - URL: `https://onlineacademiccommunity.uvic.ca/isot/wp-content/uploads/sites/7295/2023/03/News-_dataset.zip`
  - Параметр `auto_download_uvic=True` — дані завантажуються без Kaggle/реєстрації.
- Структура TruthLens: `web-app/`, `src/nlp/`, `src/ml/`, `notebooks/`, `bot/`, `dashboard/`, Docker, CI.

---

## Що перенесено в TruthLens-UA

- У **scripts/download_datasets.py** додано завантаження ISOT з того ж UVic URL, щоб отримати `data/Fake.csv` та `data/True.csv` автоматично.
- Інструкція в **data/README.md** оновлена: рекомендовано спочатку запускати `python scripts/download_datasets.py`.

Це дає змогу мати необхідні дані без ручного завантаження з Kaggle.
