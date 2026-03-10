#!/usr/bin/env python3
"""
TruthLens UA — AI Fact Checker (v1.1).
Навігація: Analyze | History | Statistics | QR Code.
Запуск: streamlit run scripts/truthlens_dashboard.py
"""
import base64
import io
import os
import re
from datetime import datetime, timedelta
from typing import Optional, Tuple

import pandas as pd
import requests
import streamlit as st

API_BASE = os.getenv("TRUTHLENS_API_URL", "https://truthlens-ua.onrender.com")
TELEGRAM_BOT = "https://t.me/truthlens_ai_bot"
EXTERNAL_DEMO = "https://truthlens-ua.onrender.com"
EXTERNAL_DOCS = "https://truthlens-ua.onrender.com/docs"

# Зовнішні QR (fallback якщо qrcode не встановлено)
TELEGRAM_QR_URL = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={TELEGRAM_BOT}"
WEB_APP_QR_URL = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={EXTERNAL_DEMO}"

COLOR_REAL = "#22c55e"
COLOR_SUSPICIOUS = "#eab308"
COLOR_FAKE = "#ef4444"

EXAMPLE_1 = (
    "Breaking: Scientists discover that drinking coffee can make you live forever, "
    "according to a study funded by a major coffee corporation."
)
EXAMPLE_2 = (
    "The World Health Organization confirmed today that global vaccination rates "
    "have reached 75% in most developed nations, citing data from their annual report."
)


def make_qr_png(data: str, size: int = 200) -> bytes:
    """Генерує QR-код у вигляді PNG (локально). Якщо qrcode недоступний — повертає None."""
    try:
        import qrcode
        qr = qrcode.QRCode(version=1, box_size=10, border=2)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img = img.resize((size, size))
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return buf.getvalue()
    except Exception:
        return None


st.set_page_config(
    page_title="TruthLens — AI Fact Checker",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "history" not in st.session_state:
    st.session_state["history"] = []

# --- Sidebar: Navigation ---
with st.sidebar:
    st.markdown("## 🔍 TruthLens")
    st.markdown("**AI Fact Checker**")
    st.caption("v1.1 Draft")
    st.markdown("---")
    st.markdown("### Navigation")
    page = st.radio(
        "Оберіть розділ",
        ["Analyze", "History", "Statistics", "QR Code"],
        label_visibility="collapsed",
        key="nav",
    )
    st.markdown("---")
    st.caption("API: truthlens-ua.onrender.com")

# --- API stats: оновлюється при натисканні Refresh або TTL 30 с ---
if "stats_refresh" not in st.session_state:
    st.session_state["stats_refresh"] = 0

@st.cache_data(ttl=30)
def get_stats(_refresh: int):
    try:
        r = requests.get(f"{API_BASE}/api/stats", timeout=15)
        return r.json() if r.ok else {}
    except Exception:
        return {}

# Для сторінок History та інших використовуємо кешовані stats; Statistics оновлює сам себе через fragment
api_stats = get_stats(st.session_state["stats_refresh"])
total_from_api = api_stats.get("total_analyzed", 0)
verified_count = api_stats.get("real", 0)
suspicious_count = api_stats.get("suspicious", 0)
fake_count = api_stats.get("fake", 0)


def _compute_agent_scores(fake_score: float, credibility: int, ipso: list) -> Tuple[int, int, int]:
    """Простий multi-agent скоринг для UI (Bias / Facts / Credibility)."""
    cred_score = max(0, min(100, credibility))
    facts_penalty = min(len(ipso) * 10, 40)
    facts_score = max(20, min(100, cred_score - facts_penalty))
    bias_base = int(fake_score * 100)
    bias_boost = min(len(ipso) * 8, 40)
    bias_score = max(40, min(100, bias_base + bias_boost))
    return bias_score, facts_score, cred_score


def _render_analysis_chain(text: str, fake_score: float, credibility: int, ipso: list) -> None:
    length = len(text.split())
    st.markdown(
        "1. **Попередня обробка тексту** — отримано "
        f"{length} слів, нормалізовано для аналізу.\n"
        "2. **Пошук емоційних тригерів та ІПСО-патернів** — "
        f"виявлено {len(ipso)} ключових технік ({', '.join(ipso) if ipso else 'не виявлено'}).\n"
        "3. **ML-класифікація (LinearSVC + TF-IDF)** — обчислено базовий fake-score "
        f"{fake_score:.2f}.\n"
        "4. **Гібридний постпроцесинг** — скориговано оцінку з урахуванням ІПСО та правил.\n"
        f"5. **Фінальний вердикт** — перетворено score на клас FAKE/REAL/SUSPICIOUS, "
        f"credibility={credibility}."
    )


def _render_business_insights(text: str, label: str) -> None:  # noqa: ARG001
    lo = text.lower()
    if any(w in lo for w in ["сон", "здоров", "health", "medicine", "сон "]):
        topic = "Здоров'я / Health"
        trend = "Стабільно"
        relevance = 0.95
        tam, sam, som = "12.5B", "3.2B", "180M"
        products = [
            "MedVerify SaaS — перевірка медичних тверджень",
            "HealthGuard API — фільтрація медичних новин",
            "PharmaTrust App — верифікація ліків та порад",
        ]
    else:
        topic = "Загальне / General"
        trend = "Стабільно"
        relevance = 0.6
        tam, sam, som = "10.1B", "2.8B", "150M"
        products = [
            "TruthEngine SaaS — універсальний фактчек-платформ",
            "ContentGuard API — сервіс модерації контенту",
            "VerifyBot — AI-агент для редакторів та аналітиків",
        ]

    st.write(f"**🎯 Тема:** {topic}")
    st.write(f"**➡️ Тренд:** {trend}")
    st.write(f"**💰 Релевантність ринку:** {int(relevance * 100)}%")
    st.write(f"**🌐 Обсяг ринку:** TAM: ${tam} \\| SAM: ${sam} \\| SOM: ${som}")

    st.markdown("**💡 Потенційні цифрові продукти:**")
    for p in products:
        st.markdown(f"- {p}")

    st.markdown("**🛡 Валідація ідеї (MVP-рівень):**")
    st.markdown(
        "- Потрібні додаткові дані для повної валідації.\n"
        "- Рекомендовано A/B-тести інтерфейсу (простий вердикт vs. розширений звіт)."
    )


# ---------- PAGE: Analyze ----------
if page == "Analyze":
    # 1) Заповнення тексту з прикладу ДО створення віджета (уникнення StreamlitAPIException)
    if "load_example" in st.session_state:
        ex_num = st.session_state["load_example"]
        st.session_state["analyze_input"] = EXAMPLE_1 if ex_num == 1 else EXAMPLE_2
        del st.session_state["load_example"]

    st.title("Analyze Content")
    st.markdown(
        "Paste any news article, social media post, or claim, "
        "or provide a URL. Use separate buttons to analyze **text** or **URL**."
    )

    # Кнопки прикладів — перед text_area, щоб при кліку лише встановити load_example і rerun
    col_btns, _ = st.columns([2, 4])
    with col_btns:
        ex1_btn = st.button("Try an example (1)", key="ex1")
        ex2_btn = st.button("Try an example (2)", key="ex2")
    if ex1_btn:
        st.session_state["load_example"] = 1
        st.rerun()
    if ex2_btn:
        st.session_state["load_example"] = 2
        st.rerun()

    # --- Text input ---
    text = st.text_area(
        "Paste text, news headline, or claim to verify...",
        placeholder="Paste text here...",
        height=160,
        key="analyze_input",
    )
    n = len((text or "").strip())
    st.caption(f"{n} characters")

    # --- URL input ---
    st.markdown("### URL analysis")
    url_value = st.text_input(
        "Paste URL to analyze (news article, blog, etc.)",
        placeholder="https://...",
        key="analyze_url",
    )
    st.caption("MVP: page HTML is fetched and stripped to plain text for analysis. "
               "You can override extracted text below if needed.")
    url_override = st.text_area(
        "Optional: override extracted text for URL",
        placeholder="Leave empty to use text auto-extracted from URL.",
        height=120,
        key="analyze_url_override",
    )

    col_actions = st.columns(2)
    with col_actions[0]:
        analyze_text_btn = st.button("Analyze text", type="primary", key="analyze_text_btn")
    with col_actions[1]:
        analyze_url_btn = st.button("Analyze URL", key="analyze_url_btn")

    # --- Analyze TEXT ---
    if analyze_text_btn:
        t = (text or "").strip()
        if len(t) < 5:
            st.warning("Enter at least 5 characters for text analysis.")
        else:
            with st.spinner("Analyzing text…"):
                try:
                    r = requests.post(
                        f"{API_BASE}/api/analyze",
                        json={"text": t},
                        timeout=60,
                    )
                    r.raise_for_status()
                    d = r.json()
                except requests.RequestException as e:
                    st.error(f"Service unavailable: {e}. Try again later.")
                    st.stop()

            label = d.get("label", "?")
            fake_score = float(d.get("fake_score", 0) or 0)
            credibility = int(d.get("credibility", 0) or 0)
            verdict = d.get("verdict", "")
            ipso = d.get("ipso_techniques") or []
            conf_pct = int((1 - fake_score) * 100) if label == "REAL" else int(fake_score * 100)

            st.session_state["history"].insert(
                0,
                {
                    "text": t,
                    "timestamp": datetime.now(),
                    "label": label,
                    "fake_score": fake_score,
                    "credibility": credibility,
                    "verdict": verdict,
                    "ipso_techniques": ipso,
                    "conf_pct": conf_pct,
                },
            )
            st.session_state["history"] = st.session_state["history"][:50]

            # Верхній вердикт
            if label == "REAL":
                color = COLOR_REAL
                title = "🟢 Verified (REAL)"
            elif label == "SUSPICIOUS":
                color = COLOR_SUSPICIOUS
                title = "🟡 Suspicious (SUSPICIOUS)"
            else:
                color = COLOR_FAKE
                title = "🔴 Fake (FAKE)"

            st.markdown(
                f'<div style="padding:1rem; border-radius:8px; background-color:{color}22; '
                f'border-left:4px solid {color};"><strong>{title}</strong> — {conf_pct}% conf. '
                f'| credibility: {credibility}</div>',
                unsafe_allow_html=True,
            )
            st.write("**Verdict:**", verdict)
            if ipso:
                st.write("**IPSO techniques:**", ", ".join(ipso))

            st.markdown("### 🧩 Multi-agent breakdown")
            bias_score, facts_score, cred_score = _compute_agent_scores(fake_score, credibility, ipso)
            col_b, col_f, col_c = st.columns(3)
            with col_b:
                st.caption("Упередженість / Bias")
                st.progress(bias_score / 100.0)
                st.write(f"{bias_score}%")
            with col_f:
                st.caption("Факти / Facts")
                st.progress(facts_score / 100.0)
                st.write(f"{facts_score}%")
            with col_c:
                st.caption("Достовірність / Credibility")
                st.progress(cred_score / 100.0)
                st.write(f"{cred_score}%")

            st.markdown("### 🔗 Ланцюг аналізу")
            _render_analysis_chain(t, fake_score, credibility, ipso)

            st.markdown("### 📊 Бізнес-інсайти та рекомендації")
            _render_business_insights(t, label)

            with st.expander("Full API response (JSON)"):
                st.json(d)

    # --- Analyze URL ---
    if analyze_url_btn:
        url_clean = (url_value or "").strip()
        if not url_clean:
            st.warning("Enter URL to analyze.")
            st.stop()

        t = (url_override or "").strip()
        if not t:
            with st.spinner("Fetching URL and extracting text…"):
                try:
                    resp = requests.get(url_clean, timeout=20)
                    resp.raise_for_status()
                    html = resp.text
                    extracted = re.sub(r"<[^>]+>", " ", html)
                    extracted = re.sub(r"\s+", " ", extracted).strip()
                    t = extracted[:8000]
                    if not t:
                        st.warning("Could not extract text from page; please paste text manually.")
                        st.stop()
                except Exception as e:  # noqa: BLE001
                    st.error(f"Failed to fetch URL: {e}")
                    st.stop()

        if len(t) < 5:
            st.warning("Extracted text is too short; please provide more content.")
        else:
            with st.spinner("Analyzing URL content…"):
                try:
                    r = requests.post(
                        f"{API_BASE}/api/analyze",
                        json={"text": t},
                        timeout=60,
                    )
                    r.raise_for_status()
                    d = r.json()
                except requests.RequestException as e:
                    st.error(f"Service unavailable: {e}. Try again later.")
                    st.stop()

            label = d.get("label", "?")
            fake_score = float(d.get("fake_score", 0) or 0)
            credibility = int(d.get("credibility", 0) or 0)
            verdict = d.get("verdict", "")
            ipso = d.get("ipso_techniques") or []
            conf_pct = int((1 - fake_score) * 100) if label == "REAL" else int(fake_score * 100)

            st.session_state["history"].insert(
                0,
                {
                    "text": t,
                    "timestamp": datetime.now(),
                    "label": label,
                    "fake_score": fake_score,
                    "credibility": credibility,
                    "verdict": verdict,
                    "ipso_techniques": ipso,
                    "conf_pct": conf_pct,
                },
            )
            st.session_state["history"] = st.session_state["history"][:50]

            if label == "REAL":
                color = COLOR_REAL
                title = "🟢 Verified (REAL)"
            elif label == "SUSPICIOUS":
                color = COLOR_SUSPICIOUS
                title = "🟡 Suspicious (SUSPICIOUS)"
            else:
                color = COLOR_FAKE
                title = "🔴 Fake (FAKE)"

            st.markdown(
                f'<div style="padding:1rem; border-radius:8px; background-color:{color}22; '
                f'border-left:4px solid {color};"><strong>{title}</strong> — {conf_pct}% conf. '
                f'| credibility: {credibility}</div>',
                unsafe_allow_html=True,
            )
            st.write("**Verdict:**", verdict)
            if ipso:
                st.write("**IPSO techniques:**", ", ".join(ipso))

            st.markdown("### 🧩 Multi-agent breakdown")
            bias_score, facts_score, cred_score = _compute_agent_scores(fake_score, credibility, ipso)
            col_b, col_f, col_c = st.columns(3)
            with col_b:
                st.caption("Упередженість / Bias")
                st.progress(bias_score / 100.0)
                st.write(f"{bias_score}%")
            with col_f:
                st.caption("Факти / Facts")
                st.progress(facts_score / 100.0)
                st.write(f"{facts_score}%")
            with col_c:
                st.caption("Достовірність / Credibility")
                st.progress(cred_score / 100.0)
                st.write(f"{cred_score}%")

            st.markdown("### 🔗 Ланцюг аналізу")
            _render_analysis_chain(t, fake_score, credibility, ipso)

            st.markdown("### 📊 Бізнес-інсайти та рекомендації")
            _render_business_insights(t, label)

            with st.expander("Full API response (JSON)"):
                st.json(d)

            label = d.get("label", "?")
            fake_score = float(d.get("fake_score", 0) or 0)
            credibility = int(d.get("credibility", 0) or 0)
            verdict = d.get("verdict", "")
            ipso = d.get("ipso_techniques") or []
            conf_pct = int((1 - fake_score) * 100) if label == "REAL" else int(fake_score * 100)

            st.session_state["history"].insert(
                0,
                {
                    "text": t,
                    "timestamp": datetime.now(),
                    "label": label,
                    "fake_score": fake_score,
                    "credibility": credibility,
                    "verdict": verdict,
                    "ipso_techniques": ipso,
                    "conf_pct": conf_pct,
                },
            )
            st.session_state["history"] = st.session_state["history"][:50]

            # Верхній вердикт
            if label == "REAL":
                color = COLOR_REAL
                title = "🟢 Verified (REAL)"
            elif label == "SUSPICIOUS":
                color = COLOR_SUSPICIOUS
                title = "🟡 Suspicious (SUSPICIOUS)"
            else:
                color = COLOR_FAKE
                title = "🔴 Fake (FAKE)"

            st.markdown(
                f'<div style="padding:1rem; border-radius:8px; background-color:{color}22; '
                f'border-left:4px solid {color};"><strong>{title}</strong> — {conf_pct}% conf. '
                f'| credibility: {credibility}</div>',
                unsafe_allow_html=True,
            )
            st.write("**Verdict:**", verdict)
            if ipso:
                st.write("**IPSO techniques:**", ", ".join(ipso))

            # Деталізований аналіз у стилі multi-agent
            st.markdown("### 🧩 Multi-agent breakdown")
            bias_score, facts_score, cred_score = _compute_agent_scores(fake_score, credibility, ipso)
            col_b, col_f, col_c = st.columns(3)
            with col_b:
                st.caption("Упередженість / Bias")
                st.progress(bias_score / 100.0)
                st.write(f"{bias_score}%")
            with col_f:
                st.caption("Факти / Facts")
                st.progress(facts_score / 100.0)
                st.write(f"{facts_score}%")
            with col_c:
                st.caption("Достовірність / Credibility")
                st.progress(cred_score / 100.0)
                st.write(f"{cred_score}%")

            st.markdown("### 🔗 Ланцюг аналізу")
            _render_analysis_chain(t, fake_score, credibility, ipso)

            st.markdown("### 📊 Бізнес-інсайти та рекомендації")
            _render_business_insights(t, label)

            with st.expander("Full API response (JSON)"):
                st.json(d)

# ---------- PAGE: History ----------
elif page == "History":
    st.title("Analysis History")
    session_count = len(st.session_state["history"])
    total_display = total_from_api if total_from_api else session_count
    st.metric("Total", total_display)
    if total_from_api:
        st.caption("Total from API. Below: this session's analyses.")
    if session_count == 0 and not total_from_api:
        st.caption("No history yet. Run analyses on the Analyze page.")

    filter_label = st.radio("Filter", ["All", "REAL", "SUSPICIOUS", "FAKE"], horizontal=True, key="hist_filter")
    search = st.text_input("Search analyses...", key="hist_search", placeholder="Search...")

    history = list(st.session_state["history"])
    if filter_label != "All":
        history = [h for h in history if h["label"] == filter_label]
    if search:
        search_lower = search.lower()
        history = [h for h in history if search_lower in (h.get("text") or "").lower()]

    for h in history:
        ts = h["timestamp"].strftime("%b %d, %Y, %I:%M %p") if hasattr(h["timestamp"], "strftime") else str(h["timestamp"])
        conf = h.get("conf_pct", int(h["fake_score"] * 100))
        label = h["label"]
        snippet = (h["text"] or "")[:200] + ("…" if len(h["text"] or "") > 200 else "")
        st.markdown(f"**{snippet}**")
        st.caption(f"{ts} | {conf}% conf. | **{label}**")
        st.markdown("---")

    if not history:
        st.info("No analyses match the filter.")

# ---------- PAGE: Statistics ----------
# Автооновлення кожні 30 с (st.fragment) + ручний Refresh
elif page == "Statistics":
    st.title("Statistics")

    @st.fragment(run_every=timedelta(seconds=30))
    def _statistics_content():
        # Кожен запуск фрагмента (у т.ч. кожні 30 с) — свіжі дані з API (кеш TTL 30 с)
        _api = get_stats(st.session_state["stats_refresh"])
        _total = _api.get("total_analyzed", 0)
        _verified = _api.get("real", 0)
        _suspicious = _api.get("suspicious", 0)
        _fake = _api.get("fake", 0)
        hist = st.session_state["history"]
        session_real = sum(1 for h in hist if h["label"] == "REAL")
        session_fake = sum(1 for h in hist if h["label"] == "FAKE")
        session_susp = sum(1 for h in hist if h["label"] == "SUSPICIOUS")

        if st.button("Refresh statistics from API", key="refresh_stats"):
            st.session_state["stats_refresh"] = st.session_state.get("stats_refresh", 0) + 1
            try:
                get_stats.clear()
            except Exception:
                pass
            st.rerun()

        st.caption("Auto-refresh every 30 seconds. Or click Refresh for immediate update.")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Total (API)", _total or len(hist))
        with c2:
            st.metric("Verified", _verified or session_real)
        with c3:
            st.metric("Suspicious", _suspicious or session_susp)
        with c4:
            st.metric("Fake", _fake or session_fake)

        if hist:
            st.caption("Session counts: Verified %d, Suspicious %d, Fake %d." % (session_real, session_susp, session_fake))

        st.subheader("Verdict Distribution")
        use_total = _total or len(hist)
        if use_total:
            vr = _verified if _total else session_real
            su = _suspicious if _total else session_susp
            fk = _fake if _total else session_fake
            df = pd.DataFrame({"Verdict": ["Verified", "Suspicious", "Fake"], "Count": [vr, su, fk]})
            st.bar_chart(df.set_index("Verdict"))
        else:
            st.caption("Run analyses or click Refresh to load stats.")

        st.subheader("Score Breakdown (Recent)")
        recent = st.session_state["history"][:10]
        if recent:
            df_recent = pd.DataFrame([
                {"#": i + 1, "Label": h["label"], "Fake score": h["fake_score"], "Credibility": h["credibility"]}
                for i, h in enumerate(recent)
            ])
            st.dataframe(df_recent.set_index("#"), use_container_width=True)
            st.bar_chart(df_recent.set_index("Label")[["Fake score", "Credibility"]])
        else:
            st.caption("No recent analyses. Use the Analyze page.")

    _statistics_content()

# ---------- PAGE: QR Code ----------
else:
    # Розмір QR: 200–240 px рекомендовано для сканування (ISO/IEC 18004, UX best practices)
    QR_DISPLAY_SIZE_PX = 240
    st.title("Mobile Access")
    st.markdown("Scan QR codes to access TruthLens on your phone or open the Telegram bot.")
    st.markdown("")  # відступ

    def _load_qr_image(url: str, timeout: int = 10) -> Optional[bytes]:
        try:
            r = requests.get(url, timeout=timeout)
            return r.content if r.ok and r.content else None
        except Exception:
            return None

    telegram_qr_bytes = make_qr_png(TELEGRAM_BOT)
    if not telegram_qr_bytes:
        telegram_qr_bytes = _load_qr_image(TELEGRAM_QR_URL)

    web_qr_bytes = make_qr_png(EXTERNAL_DEMO)
    if not web_qr_bytes:
        web_qr_bytes = _load_qr_image(WEB_APP_QR_URL)

    col_telegram, col_web = st.columns(2)

    with col_telegram:
        with st.container():
            st.subheader("Telegram Bot")
            st.markdown("")
            if telegram_qr_bytes:
                b64_tg = base64.b64encode(telegram_qr_bytes).decode()
                st.markdown(
                    f'<div style="text-align:center;"><img src="data:image/png;base64,{b64_tg}" width="{QR_DISPLAY_SIZE_PX}" height="{QR_DISPLAY_SIZE_PX}" alt="Telegram Bot QR" style="display:block;margin:0 auto;" /></div>',
                    unsafe_allow_html=True,
                )
                st.caption("Telegram Bot QR Code")
                st.download_button("Save QR", data=telegram_qr_bytes, file_name="truthlens_telegram_qr.png", mime="image/png", key="dl_tg")
            else:
                st.caption("QR-код не завантажився. Відкрийте посилання нижче.")
                st.markdown(f"[Відкрити генератор QR у новій вкладці]({TELEGRAM_QR_URL})")
            st.markdown("**Bot Username**")
            st.code("@truthlens_ai_bot", language=None)
            st.markdown(f"[Open in Telegram]({TELEGRAM_BOT})")

    with col_web:
        with st.container():
            st.subheader("Web App (API)")
            st.markdown("")
            st.markdown("**App URL**")
            st.code(EXTERNAL_DEMO, language=None)
            st.markdown(f"[Open in browser]({EXTERNAL_DEMO})")
            st.markdown("")
            if web_qr_bytes:
                b64_web = base64.b64encode(web_qr_bytes).decode()
                st.markdown(
                    f'<div style="text-align:center;"><img src="data:image/png;base64,{b64_web}" width="{QR_DISPLAY_SIZE_PX}" height="{QR_DISPLAY_SIZE_PX}" alt="Web App QR" style="display:block;margin:0 auto;" /></div>',
                    unsafe_allow_html=True,
                )
                st.caption("Web App QR Code")
                st.download_button("Download QR Code", data=web_qr_bytes, file_name="truthlens_web_qr.png", mime="image/png", key="dl_web")
            else:
                st.caption("QR-код не завантажився. Скористайтесь посиланням вище.")
                st.markdown(f"[Відкрити генератор QR у новій вкладці]({WEB_APP_QR_URL})")
            st.markdown("")

    st.markdown("---")
    st.subheader("How to Use")
    with st.container():
        st.markdown("**1.** Відскануйте QR-код камерою телефону.")
        st.markdown("**2.** **Telegram** — відкриється бот; надішліть текст для перевірки.")
        st.markdown("**3.** **Web App** — відкриється додаток у браузері. На iPhone: Share → «Додати на екран „Дім“» для PWA.")
