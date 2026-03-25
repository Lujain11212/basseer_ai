# 📋 سجل التغييرات — Basseer AI Changelog

## v3.0.0 — POC Enhancement Release

### الإضافات الجديدة

**1. واجهات المستخدم — 3 تبويبات**
- 📝 **إدخال الاستبيان:** نموذج إدخال + تحقق فوري + درجة ثقة + توصيات
- 🔍 **الباحث الميداني:** قائمة سجلات مشبوهة + أزرار إجراءات (مراجعة/تأكيد/تصحيح/تصعيد)
- 📊 **لوحة الجهة المشرفة:** KPIs + خريطة حرارية + توصيات + أداء الباحثين + صحة النظام

**2. إعداد LLM من التطبيق (First-Run Setup)**
- صندوق إعداد يظهر عند أول تشغيل بدون تكوين LLM
- زر "إعدادات النظام" في الشريط الجانبي لتعديل الإعدادات لاحقاً
- حفظ تلقائي في ملف `.env`
- Fallback تلقائي للقواعد عند فشل LLM

**3. Explainable AI — حقول جديدة**
- `confidence_reason_en` — السبب بالإنجليزية
- `detected_by` — مصدر الكشف (rule / llm / hybrid)
- حقول كاملة في `/validate`: confidence_score, confidence_label, reason_ar, reason_en, detected_by, llm_used, latency_ms

**4. محرك التوصيات التلقائية**
- توصيات مبنية على أنماط الأخطاء المتكررة
- توصيات إعادة صياغة الأسئلة ذات المعدل العالي
- توصيات تدريب الباحثين حسب المنطقة
- توصيات مراجعة أداء الباحثين الأفراد
- Endpoint جديد: `GET /recommendations`

**5. الخريطة الحرارية — تحسينات جوهرية**
- 4 مقاييس: العدد، النسبة، متوسط الثقة، معدل اختلاف الذكاء (LLM Disagreement)
- محوران: المنطقة أو الباحث (Enumerator)
- لوحة تفاصيل الخلية محسّنة: القواعد الأكثر انتهاكاً + تفسير LLM + متوسط الثقة
- Endpoint محسّن: `GET /heatmap?metric=...&axis=...`

**6. مراقبة صحة النظام**
- Endpoint جديد: `GET /health`
- مؤشرات: حالة الخادم، LLM، عدد الاستدعاءات، متوسط الزمن، نسبة الكاش
- عرض مؤشرات الصحة في لوحة المراقبة والشريط الجانبي

**7. واجهة الباحث الميداني**
- Endpoint جديد: `GET /field_researcher`
- Endpoint جديد: `POST /review`
- حالات المراجعة: pending / reviewed / confirmed / escalated / correction_requested
- أزرار إجراءات تفاعلية

**8. إحصائيات LLM**
- تتبع عدد الاستدعاءات (ناجحة/فاشلة)
- متوسط زمن الاستجابة
- نسبة Cache Hit
- آخر خطأ

### الملفات المعدّلة
- `backend/main.py` — endpoints جديدة + حقول محسّنة
- `backend/validators/llm_layer.py` — إحصائيات + إدارة إعدادات + few-shot محسّن
- `services/pipeline.py` — محرك توصيات + detected_by + reason_en
- `dashboard/app.py` — 3 تبويبات + إعداد LLM + صحة النظام
- `storage/models.py` — حقول جديدة: detected_by, review_status, confidence_reason_en
- `tests/test_core.py` — اختبارات الحقول الجديدة

### الملفات المضافة
- `docs/JUDGES_DEMO.md` — سيناريو عرض 3-5 دقائق للجنة التحكيم

---

## v2.0.0 — Previous Release

- دمج ثلاثة مزودي LLM (OpenAI, Anthropic, Gemini)
- خط أنابيب التحقق: Rules → LLM → Merge → Scoring
- لوحة مراقبة Streamlit مع خريطة حرارية
- Few-shot prompting بالعربية
- Caching لتقليل تكلفة LLM
- 100 سجل تجريبي مع أخطاء مقصودة

## v1.0.0 — Initial POC

- محرك قواعد أساسي
- semantic_mock fallback
- FastAPI backend
- SQLite storage
