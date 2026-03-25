# 🏗️ البنية التقنية المختصرة — Architecture Brief

```
┌─────────────────────────────────────────────────────────────────┐
│                    بصير AI — Semantic Guardian                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   📱 Streamlit Dashboard (:8501)                                │
│   ├── تبويب الإدخال → POST /ingest                              │
│   └── تبويب التحليلات → GET /stats, /heatmap, /cell_detail     │
│                                                                 │
├───────────────────── FastAPI (:8000) ───────────────────────────┤
│                                                                 │
│   POST /validate ─→ Pipeline (لا يخزّن)                         │
│   POST /ingest   ─→ Pipeline → SQLite (يخزّن)                  │
│                                                                 │
│   ┌─── Pipeline (services/pipeline.py) ──────────────────────┐ │
│   │                                                           │ │
│   │  ① Rules Layer (backend/validators/rules.py)             │ │
│   │     └── 5 قواعد منطقية (age/exp, edu/age, income/job…)  │ │
│   │                                                           │ │
│   │  ② LLM Layer (backend/validators/llm_layer.py)           │ │
│   │     ├── Online: OpenAI / Anthropic / Gemini              │ │
│   │     ├── Few-shot Arabic prompting → JSON output          │ │
│   │     ├── Cache (TTLCache, 5 min)                          │ │
│   │     └── Offline fallback → semantic_mock.py              │ │
│   │                                                           │ │
│   │  ③ Merge + Dedup                                         │ │
│   │  ④ Confidence Scoring (violations + completeness)        │ │
│   │                                                           │ │
│   └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│   SQLite (data/basseer.db)                                     │
│   ├── survey_responses (+ llm_used, latency_ms, enumerator_id)│
│   └── validation_logs (+ source: rules|semantic|llm)          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## التقنيات

| الطبقة | التقنية |
|--------|---------|
| API | FastAPI 0.110 + Uvicorn |
| Dashboard | Streamlit 1.33 + Plotly 5.21 |
| LLM | httpx → OpenAI/Anthropic/Gemini (اختياري) |
| Storage | SQLite + SQLAlchemy 2.0 |
| Cache | cachetools TTLCache |
| Tests | pytest |

## تدفق البيانات

1. المستخدم يُدخل سجل → Dashboard يرسل `POST /ingest`
2. Pipeline يشغّل Rules → LLM (أو fallback) → يدمج ويزيل التكرار → يحسب درجة الثقة
3. النتيجة تُخزّن في SQLite وتُرجع فوراً مع `latency_ms`
4. Dashboard يعرض التحذيرات + التوصيات + درجة الثقة مع السبب
5. Heatmap تتحدث تلقائياً من `/heatmap` — تُظهر أي سؤال وأي منطقة فيها مشاكل
