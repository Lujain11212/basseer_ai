"""
خط أنابيب التحقق - Validation Pipeline Orchestrator

تدفق العمل:
  1. Rules Layer (قواعد منطقية)
  2. LLM Semantic Layer (أو semantic_mock كـ fallback)
  3. Merge + Dedup
  4. Confidence Scoring
  5. Recommendations Engine
  6. إرجاع النتيجة
"""

import time
import logging
import os
from backend.validators.rules import run_all_rules
from backend.validators.semantic_mock import run_semantic_checks
from backend.validators.llm_layer import call_llm
from backend.validators.scoring import calculate_confidence, get_label_arabic, count_missing

logger = logging.getLogger("basseer.pipeline")


def _dedup_warnings(warnings: list[dict]) -> list[dict]:
    """إزالة التحذيرات المكررة حسب الحقل + القاعدة"""
    seen = set()
    unique = []
    for w in warnings:
        key = (w.get("field", ""), w.get("severity", ""), w.get("rule", ""))
        if key not in seen:
            seen.add(key)
            unique.append(w)
    return unique


def _determine_detected_by(rule_warnings: list, llm_warnings: list, llm_used: bool) -> str:
    """Determine detection method: rule / llm / hybrid"""
    has_rules = len(rule_warnings) > 0
    has_llm = len(llm_warnings) > 0 and llm_used
    if has_rules and has_llm:
        return "hybrid"
    elif has_llm:
        return "llm"
    else:
        return "rule"


def _build_reason_en(warnings: list[dict], data: dict) -> str:
    """Build an English reason summary from warnings."""
    if not warnings:
        return "No inconsistencies detected — data is consistent"
    reasons = []
    for w in warnings:
        msg = w.get("message_en", "")
        if msg:
            reasons.append(msg)
    if reasons:
        return "; ".join(reasons[:3])
    return f"{len(warnings)} inconsistencies detected"


def _generate_recommendations(warnings: list[dict], data: dict) -> list[dict]:
    """
    محرك التوصيات التلقائية
    Automatic Recommendations Engine — generates system-level recommendations
    based on detected error patterns.
    """
    recs = []
    field_counts = {}
    for w in warnings:
        f = w.get("field", "unknown")
        field_counts[f] = field_counts.get(f, 0) + 1

    field_labels = {
        "age": "العمر", "experience_years": "سنوات الخبرة",
        "education": "التعليم", "job_title": "المسمى الوظيفي",
        "income": "الدخل", "employment_status": "حالة التوظيف",
    }

    # Field-level recommendations
    for field, count in field_counts.items():
        label_ar = field_labels.get(field, field)
        if count >= 2:
            recs.append({
                "type": "question_rephrase",
                "field": field,
                "message_ar": f"يُنصح بإعادة صياغة سؤال '{label_ar}' بسبب ارتفاع نسبة التعارضات الدلالية",
                "message_en": f"Consider rephrasing the '{field}' question due to high semantic inconsistency",
                "priority": "high",
            })
        elif count == 1:
            recs.append({
                "type": "field_review",
                "field": field,
                "message_ar": f"يُنصح بمراجعة حقل '{label_ar}' — تم رصد تعارض محتمل",
                "message_en": f"Consider reviewing the '{field}' field — potential conflict detected",
                "priority": "medium",
            })

    # Region-based recommendation
    region = data.get("region", "")
    high_sev = sum(1 for w in warnings if w.get("severity") == "high")
    if high_sev >= 2 and region:
        recs.append({
            "type": "researcher_training",
            "field": "region",
            "message_ar": f"يُنصح بمراجعة تدريب الباحثين الميدانيين في منطقة {region}",
            "message_en": f"Consider reviewing field researcher training in the {region} region",
            "priority": "high",
        })

    # Enumerator-based recommendation
    enum_id = data.get("enumerator_id", "default")
    if enum_id != "default" and len(warnings) >= 3:
        recs.append({
            "type": "enumerator_review",
            "field": "enumerator_id",
            "message_ar": f"يُنصح بمراجعة أداء الباحث {enum_id} — عدد التعارضات مرتفع",
            "message_en": f"Consider reviewing enumerator {enum_id} performance — high conflict count",
            "priority": "high",
        })

    return recs


def run_pipeline(data: dict) -> dict:
    """
    تشغيل خط الأنابيب الكامل

    Args:
        data: dict مع حقول الاستبيان

    Returns:
        dict مع: warnings, recommendations, confidence_score, confidence_label,
              confidence_label_ar, confidence_reason_ar, confidence_reason_en,
              contradictions_count, missing_fields_count, detected_by,
              llm_used, llm_provider, latency_ms
    """
    t0 = time.perf_counter()

    # ─── الطبقة 1: القواعد المنطقية ───
    rule_warnings, rule_recs = run_all_rules(data)

    # ─── الطبقة 2: LLM أو Semantic Mock ───
    llm_warnings, llm_recs, llm_used, llm_note_en = call_llm(data)

    if llm_used:
        sem_warnings, sem_recs = [], []
        provider = os.environ.get("LLM_PROVIDER", "offline")
    else:
        # Fallback إلى semantic_mock
        sem_warnings, sem_recs = run_semantic_checks(data)
        provider = "offline"

    # ─── الطبقة 3: دمج وإزالة التكرار ───
    all_warnings = _dedup_warnings(rule_warnings + llm_warnings + sem_warnings)
    all_field_recs = rule_recs + llm_recs + sem_recs

    # ─── الطبقة 4: حساب درجة الثقة ───
    score, label, reason_ar = calculate_confidence(all_warnings, data)
    missing = count_missing(data)

    # ─── الطبقة 5: محرك التوصيات ───
    system_recs = _generate_recommendations(all_warnings, data)

    # Merge field-level and system-level recommendations
    all_recommendations = all_field_recs + system_recs

    # ─── Detected By ───
    detected_by = _determine_detected_by(rule_warnings, llm_warnings, llm_used)

    # ─── Reason EN ───
    reason_en = llm_note_en if llm_note_en else _build_reason_en(all_warnings, data)

    latency = round((time.perf_counter() - t0) * 1000, 1)

    return {
        "warnings": all_warnings,
        "recommendations": all_recommendations,
        "confidence_score": score,
        "confidence_label": label,
        "confidence_label_ar": get_label_arabic(label),
        "confidence_reason_ar": reason_ar,
        "confidence_reason_en": reason_en,
        "contradictions_count": len(all_warnings),
        "missing_fields_count": missing,
        "detected_by": detected_by,
        "llm_used": llm_used,
        "llm_provider": provider,
        "latency_ms": latency,
    }
