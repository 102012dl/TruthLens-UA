# TruthLens UA — дані для тренування

## ISOT Fake News (англомовні статті)

- **Джерело:** Kaggle — [Fake and Real News Dataset](https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset)
- **Файли:** після завантаження покласти сюди:
  - `Fake.csv`
  - `True.csv`
- **Як завантажити:**
  1. Зареєструйтесь на [Kaggle](https://www.kaggle.com).
  2. Відкрийте посилання датасету вище → Download.
  3. Розархівуйте zip і скопіюйте `Fake.csv`, `True.csv` у цю папку `data/`.
- Альтернатива через CLI:
  ```bash
  pip install kaggle
  # Налаштуйте API key з Kaggle (Account -> Create New API Token)
  kaggle datasets download -d clmentbisaillon/fake-and-real-news-dataset -p data/
  # Розархівуйте вручну або скриптом у data/
  ```

## Українські дані (UA NLP / UNLP)

- **HuggingFace:** у ноутбуку `03_ua_nlp_training.ipynb` використовується спроба завантаження з `datasets` (наприклад `ukr-detect/ukr-twitter-2021`). Встановіть: `pip install datasets`.
- Якщо датасет недоступний, ноутбук використовує невеликий ручний набір UA текстів для перевірки пайплайну та A/B тестів.

## Після завантаження

Запустіть ноутбуки по черзі:
1. `notebooks/01_isot_fake_news_mlflow.ipynb` — тренування LinearSVC, збереження `artifacts/best_model.joblib`.
2. `notebooks/03_ua_nlp_training.ipynb` — A/B тести моделей, логування в MLflow.
