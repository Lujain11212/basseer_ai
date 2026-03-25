"""
طبقة التحقق الدلالي (Fallback) - Semantic Validation Layer (Mock/Heuristics)
تُستخدم عندما لا يتوفر مفتاح LLM API
"""


def _warn(rule, sev, field, msg_ar, msg_en):
    return {"rule": rule, "severity": sev, "field": field,
            "message_ar": msg_ar, "message_en": msg_en, "source": "semantic"}


def _rec(field, current, sug_ar, sug_en):
    return {"field": field, "current_value": str(current),
            "suggestion_ar": sug_ar, "suggestion_en": sug_en}


HIGH_EDU_JOBS = ["doctor", "طبيب", "surgeon", "جراح", "professor", "أستاذ",
                  "researcher", "باحث", "scientist", "عالم", "lawyer", "محامي"]


def semantic_education_job_check(d):
    w, r = [], []
    edu, job = d.get("education", "").lower(), d.get("job_title", "").lower()
    needs_high = any(hj in job for hj in HIGH_EDU_JOBS)
    low_edu = any(e in edu for e in ["high school", "ثانوية", "diploma", "دبلوم"])
    if needs_high and low_edu:
        w.append(_warn("semantic_edu_job", "high", "job_title",
                        f"تعارض دلالي: وظيفة ({d['job_title']}) تتطلب تعليم أعلى من ({d['education']})",
                        f"Semantic conflict: ({d['job_title']}) requires higher education than ({d['education']})"))
        r.append(_rec("education", d["education"],
                       f"وظيفة '{d['job_title']}' تتطلب بكالوريوس أو أعلى",
                       f"'{d['job_title']}' requires Bachelor's or higher"))
    return w, r


def semantic_employment_income_check(d):
    w, r = [], []
    status, income = d.get("employment_status", "").lower(), d.get("income", 0)
    if any(t in status for t in ["part-time", "part time", "دوام جزئي", "جزئي"]) and income > 30000:
        w.append(_warn("semantic_employment_income", "medium", "income",
                        f"الدخل ({income:,.0f}) مرتفع لحالة ({d['employment_status']})",
                        f"Income ({income:,.0f}) high for ({d['employment_status']})"))
        r.append(_rec("income", income,
                       "الدخل المتوقع للدوام الجزئي أقل من 15,000",
                       "Expected part-time income below 15,000"))
    if any(t in status for t in ["student", "طالب"]) and income > 15000:
        w.append(_warn("semantic_student_income", "medium", "income",
                        f"الدخل ({income:,.0f}) مرتفع لطالب",
                        f"Income ({income:,.0f}) high for a student"))
        r.append(_rec("income", income,
                       "الدخل المتوقع للطالب: 0 - 8,000",
                       "Expected student income: 0 - 8,000"))
    return w, r


def run_semantic_checks(data):
    all_w, all_r = [], []
    for fn in [semantic_education_job_check, semantic_employment_income_check]:
        w, r = fn(data)
        all_w.extend(w)
        all_r.extend(r)
    return all_w, all_r
