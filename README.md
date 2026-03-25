# 🛡️ بصير AI – الحارس الدلالي
## Basseer AI – Semantic Guardian

**نظام ذكي للكشف التلقائي عن التناقضات المنطقية والدلالية في بيانات الاستبيانات الحكومية**

> مسار التحدي: المعالجة الذكية والتصنيف الآلي المدعوم بالذكاء الاصطناعي  
> Track: AI-Driven Intelligent Processing and Automated Classification

---

## 📋 نظرة عامة

بصير AI هو نظام إثبات مفهوم (POC) يوفر طبقة تحقق ذكية متعددة المستويات لضمان جودة بيانات المسوحات الإحصائية:

1. **محرك القواعد المنطقية** — تحقق فوري من التعارضات الواضحة (العمر مقابل الخبرة، التعليم مقابل الوظيفة...)
2. **طبقة الذكاء الاصطناعي (LLM)** — تحليل دلالي عميق باستخدام Few-Shot Prompting بالعربية
3. **محرك التوصيات** — توليد تلقائي لتوصيات تحسين الاستبيانات وتدريب الباحثين
4. **درجة الثقة** — نموذج تسجيل محسّن يجمع بين جميع الطبقات

---

## 🚀 التشغيل السريع

### المتطلبات
- Python 3.10+
- pip

### الخطوات

```bash
# 1. استنساخ المشروع
cd basseer_ai_poc_v2

# 2. إنشاء البيئة الافتراضية
python -m venv venv
source venv/bin/activate        # Linux/Mac
# .\venv\Scripts\Activate.ps1   # Windows

# 3. تثبيت المتطلبات
pip install -r requirements.txt

# 4. إعداد ملف البيئة
cp .env.example .env

# 5. توليد البيانات التجريبية
python scripts/generate_dataset.py

# 6. تشغيل الخادم الخلفي
uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload

# 7. (في نافذة طرفية جديدة) إدخال البيانات
python scripts/ingest_dataset.py

# 8. تشغيل لوحة المراقبة
streamlit run dashboard/app.py --server.port 8501
```

أو استخدم السكريبت الشامل:
```bash
bash scripts/run.sh          # Linux/Mac
.\scripts\run_windows.ps1    # Windows
```

### الوصول
- **الخادم:** http://127.0.0.1:8000
- **التوثيق:** http://127.0.0.1:8000/docs
- **لوحة المراقبة:** http://127.0.0.1:8501

---

## ⚙️ إعداد مزود الذكاء الاصطناعي (LLM)

### الطريقة 1: من داخل التطبيق (موصى بها)
عند تشغيل التطبيق لأول مرة بدون إعداد LLM:
- يظهر صندوق إعداد تلقائي لإدخال المزود والمفتاح
- يمكن تعديل الإعدادات لاحقاً من زر "⚙️ إعدادات النظام" في الشريط الجانبي

### الطريقة 2: من ملف .env
```env
LLM_PROVIDER=openai          # openai | anthropic | gemini | offline
LLM_API_KEY=sk-your-key      # مفتاح API
LLM_MODEL=gpt-4o-mini        # اسم النموذج (اختياري)
```

### المزودون المدعومون
| المزود | النموذج الافتراضي | متغير المفتاح |
|--------|-------------------|---------------|
| OpenAI | gpt-4o-mini | sk-... |
| Anthropic | claude-sonnet-4-20250514 | sk-ant-... |
| Gemini | gemini-1.5-flash | AIza... |

> إذا لم يتم إعداد مفتاح أو فشل الاتصال، يعمل النظام تلقائياً بوضع القواعد (offline) بدون توقف.

---

## 🏗️ هيكل المشروع

```
basseer_ai_poc_v2/
├── backend/
│   ├── main.py                 # FastAPI endpoints
│   └── validators/
│       ├── rules.py            # محرك القواعد المنطقية
│       ├── semantic_mock.py    # التحقق الدلالي (fallback)
│       ├── llm_layer.py        # طبقة LLM + Few-Shot + Cache
│       └── scoring.py          # نموذج درجة الثقة
├── services/
│   └── pipeline.py             # منظم خط الأنابيب
├── dashboard/
│   └── app.py                  # Streamlit Dashboard (3 tabs)
├── storage/
│   ├── db.py                   # إدارة SQLite
│   └── models.py               # نماذج البيانات
├── scripts/
│   ├── generate_dataset.py     # توليد 100 سجل تجريبي
│   ├── ingest_dataset.py       # إدخال البيانات عبر API
│   ├── run.sh                  # سكريبت تشغيل Linux
│   └── run_windows.ps1         # سكريبت تشغيل Windows
├── data/
│   └── anonymized_sample_100.csv
├── docs/
│   ├── ARCHITECTURE_BRIEF.md
│   ├── CHANGES.md
│   ├── POC_DEMO_SCRIPT.md
│   └── JUDGES_DEMO.md         # سيناريو العرض للجنة
├── tests/
│   └── test_core.py
├── .env.example
├── requirements.txt
└── README.md
```

---

## 📡 واجهات API الرئيسية

| Endpoint | Method | الوصف |
|----------|--------|-------|
| `/validate` | POST | تحقق فوري بدون تخزين |
| `/ingest` | POST | تحقق + تخزين |
| `/stats` | GET | إحصائيات جودة البيانات |
| `/heatmap` | GET | بيانات الخريطة الحرارية |
| `/cell_detail` | GET | تفاصيل خلية محددة |
| `/health` | GET | صحة النظام |
| `/llm_settings` | GET/POST | إعدادات LLM |
| `/field_researcher` | GET | سجلات تحتاج مراجعة |
| `/review` | POST | تحديث حالة مراجعة |
| `/recommendations` | GET | التوصيات المجمّعة |

### مثال على استجابة `/validate`
```json
{
  "confidence_score": 72,
  "confidence_label": "Medium confidence",
  "confidence_reason_ar": "1 مخالفة حرجة (-25), 1 مخالفة متوسطة (-12)",
  "confidence_reason_en": "Mismatch between age and years of experience",
  "detected_by": "hybrid",
  "llm_used": true,
  "latency_ms": 430
}
```

---

## 🗺️ الخريطة الحرارية

تدعم 4 مقاييس:
- **العدد (Count)** — عدد التناقضات المكتشفة
- **النسبة % (Conflict Rate)** — نسبة التعارض من إجمالي السجلات
- **متوسط الثقة (Avg Confidence)** — متوسط درجة الثقة لكل خلية
- **معدل اختلاف الذكاء (LLM Disagreement)** — الفرق بين نتائج القواعد والذكاء الاصطناعي

محوران: **المنطقة (Region)** أو **الباحث (Enumerator)**

عند النقر على خلية يظهر:
- عدد الأخطاء ونسبة التعارض
- أكثر القواعد انتهاكاً
- تفسير الذكاء الاصطناعي
- التوصية

---

## 🧪 تشغيل الاختبارات

```bash
pytest tests/test_core.py -v
```

---

## 📖 المزيد

- [سيناريو العرض للجنة التحكيم](docs/JUDGES_DEMO.md)
- [الهيكل المعماري](docs/ARCHITECTURE_BRIEF.md)
- [سجل التغييرات](docs/CHANGES.md)
