"""
نموذج درجة الثقة المحسّن - Enhanced Confidence Score Model

يحسب الدرجة بناءً على:
  1. عدد المخالفات وأنواعها
  2. نتيجة LLM (severity)
  3. اكتمال البيانات (missing fields)
"""

SEVERITY_PENALTY = {"high": 25, "medium": 12, "low": 6}

REQUIRED_FIELDS = ["age", "experience_years", "education", "job_title",
                    "income", "region", "employment_status"]


def count_missing(data: dict) -> int:
    missing = 0
    for f in REQUIRED_FIELDS:
        val = data.get(f)
        if val is None or (isinstance(val, str) and val.strip() == ""):
            missing += 1
    return missing


def calculate_confidence(warnings: list[dict], data: dict | None = None) -> tuple[float, str, str]:
    """
    Returns: (score, label_en, reason_ar)
    """
    score = 100.0
    reasons_ar = []

    # خصم بسبب المخالفات
    high_c = sum(1 for w in warnings if w.get("severity") == "high")
    med_c = sum(1 for w in warnings if w.get("severity") == "medium")
    low_c = sum(1 for w in warnings if w.get("severity") == "low")

    for w in warnings:
        score -= SEVERITY_PENALTY.get(w.get("severity", "low"), 6)

    if high_c:
        reasons_ar.append(f"{high_c} مخالفة حرجة (-{high_c * 25})")
    if med_c:
        reasons_ar.append(f"{med_c} مخالفة متوسطة (-{med_c * 12})")
    if low_c:
        reasons_ar.append(f"{low_c} مخالفة خفيفة (-{low_c * 6})")

    # خصم بسبب نقص البيانات
    if data:
        missing = count_missing(data)
        if missing > 0:
            penalty = missing * 8
            score -= penalty
            reasons_ar.append(f"{missing} حقل ناقص (-{penalty})")

    score = max(0.0, min(100.0, score))

    if score >= 75:
        label = "High confidence"
    elif score >= 45:
        label = "Medium confidence"
    else:
        label = "Low confidence"

    reason = "، ".join(reasons_ar) if reasons_ar else "لا توجد مخالفات — بيانات متسقة"

    return round(score, 1), label, reason


def get_label_arabic(label: str) -> str:
    return {"High confidence": "ثقة عالية",
            "Medium confidence": "ثقة متوسطة",
            "Low confidence": "ثقة منخفضة"}.get(label, label)
