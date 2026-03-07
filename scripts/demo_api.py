#!/usr/bin/env python3
"""
TruthLens UA — демо-перевірка API: /health та /api/analyze на 8 демо-текстах.
Запуск: python scripts/demo_api.py [BASE_URL]
Приклад: python scripts/demo_api.py
         python scripts/demo_api.py https://truthlens-xxx.onrender.com
"""
import os
import sys
import urllib.request
import json

DEFAULT_BASE = "http://127.0.0.1:8000"

# 8 демо-текстів для захисту (FAKE / REAL / підозрілі)
DEMO_TEXTS = [
    ("FAKE", "ТЕРМІНОВО!!! ЗСУ ЗДАЛИ Харків! Зеленський підписав капітуляцію! Поширте до видалення!"),
    ("REAL", "НБУ підвищив облікову ставку до 16% річних. Рішення ухвалено на засіданні Правління."),
    ("FAKE", "Breaking: Scientists discover coffee makes you live forever and cures cancer!"),
    ("FAKE", "Прокидайтесь люди! Уряд приховує правду! Поширте до видалення!"),
    ("DEEPFAKE", "Зеленський у відеозверненні заявив про капітуляцію. Відео набрало 2 млн переглядів."),
    ("REAL", "Кабінет Міністрів затвердив програму підтримки бізнесу на наступний рік."),
    ("FAKE", "Уряд ПРИХОВУЄ правду! Прокидайтесь люди!!!"),
    ("REAL", "За даними Держстату, ВВП у третьому кварталі зріс на 3% у порівнянні з минулим роком."),
]


def request(base: str, path: str, method: str = "GET", body: dict | None = None) -> dict:
    url = base.rstrip("/") + path
    req = urllib.request.Request(url, method=method)
    req.add_header("Content-Type", "application/json")
    if body:
        req.data = json.dumps(body).encode("utf-8")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def _url_has_non_ascii(url: str) -> bool:
    try:
        url.encode("ascii")
        return False
    except UnicodeEncodeError:
        return True


def main() -> None:
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    base = (sys.argv[1] if len(sys.argv) > 1 else os.environ.get("TRUTHLENS_API_URL", DEFAULT_BASE)).rstrip("/")

    if _url_has_non_ascii(base) or "ваш-url" in base.lower() or "your-url" in base.lower():
        print("Помилка: вказано плейсхолдер або URL з не-латинськими символами.")
        print("Потрібен реальний URL вашого сервісу (лише латиниця та цифри).")
        print("Як отримати URL на Render: див. docs/RENDER_GET_URL.md")
        print("Приклад: python scripts/demo_api.py https://truthlens-ua.onrender.com")
        sys.exit(1)

    print(f"=== TruthLens UA — демо API ===\nBase URL: {base}\n")

    # 1. Health
    try:
        health = request(base, "/health")
        print("GET /health:", json.dumps(health, indent=2, ensure_ascii=False))
        print("model_loaded:", health.get("model_loaded"))
    except Exception as e:
        print("GET /health FAILED:", e)
        if base == DEFAULT_BASE:
            print("Переконайтесь, що API запущено: .venv\\Scripts\\python -m uvicorn src.api.main:app --reload")
        else:
            print("Перевірте URL (лише ASCII). Як отримати URL на Render: docs/RENDER_GET_URL.md")
        sys.exit(1)

    # 2. Analyze demo texts
    print("\n--- POST /api/analyze (8 демо-текстів) ---\n")
    for expected, text in DEMO_TEXTS:
        try:
            out = request(base, "/api/analyze", "POST", {"text": text})
            label = out.get("label", "?")
            score = out.get("fake_score", 0)
            verdict = out.get("verdict", "")
            print(f"[{expected}] -> {label} (fake_score={score:.2f}) {verdict[:50]}...")
        except Exception as e:
            print(f"[{expected}] ERROR: {e}")

    print("\n--- Готово. Використовуйте /docs для повного Swagger. ---")


if __name__ == "__main__":
    main()
