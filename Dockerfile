# TruthLens-UA API — Python 3.12 для уникнення збірки pydantic-core на Render
FROM python:3.12-slim

WORKDIR /app

# Збираємо лише runtime-залежності (без pytest, ruff) для швидшої збірки
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ENV PYTHONPATH=/app
ENV PORT=10000
EXPOSE 10000

# Render підставляє $PORT під час запуску
CMD uvicorn src.api.main:app --host 0.0.0.0 --port ${PORT:-10000}
