"""
محرك التحقق القائم على القواعد - Rule-Based Validation Engine
"""
from typing import Any


def _warn(rule: str, severity: str, field: str, msg_ar: str, msg_en: str) -> dict:
    return {"rule": rule, "severity": severity, "field": field,
            "message_ar": msg_ar, "message_en": msg_en, "source": "rules"}


def _rec(field: str, current: Any, sug_ar: str, sug_en: str) -> dict:
    return {"field": field, "current_value": str(current),
            "suggestion_ar": sug_ar, "suggestion_en": sug_en}


def validate_experience_vs_age(d: dict):
    w, r = [], []
    age, exp = d.get("age", 0), d.get("experience_years", 0)
    mx = max(0, age - 10)
    if exp > mx:
        w.append(_warn("experience_vs_age", "high", "experience_years",
                        f"تعارض: سنوات الخبرة ({exp}) غير متوافقة مع العمر ({age}). الحد الأقصى المتوقع: {mx} سنة",
                        f"Conflict: Experience ({exp}) incompatible with age ({age}). Max expected: {mx}"))
        r.append(_rec("experience_years", exp,
                       f"نطاق الخبرة المقترح لهذا العمر: 0-{mx} سنة",
                       f"Suggested experience range for age {age}: 0-{mx} years"))
    return w, r


def validate_education_vs_age(d: dict):
    w, r = [], []
    age, edu = d.get("age", 0), d.get("education", "").lower()
    thresholds = {"phd": 26, "doctorate": 26, "دكتوراه": 26,
                  "master": 24, "masters": 24, "ماجستير": 24,
                  "bachelor": 21, "bachelors": 21, "بكالوريوس": 21,
                  "diploma": 19, "دبلوم": 19}
    for k, min_age in thresholds.items():
        if k in edu and age < min_age:
            w.append(_warn("education_vs_age", "high", "education",
                            f"تعارض: الحصول على {d['education']} في عمر {age} غير منطقي. الحد الأدنى: {min_age}",
                            f"Conflict: {d['education']} at age {age} implausible. Min age: {min_age}"))
            r.append(_rec("age", age,
                           f"العمر الأدنى المتوقع لحامل شهادة {d['education']}: {min_age} سنة",
                           f"Min expected age for {d['education']}: {min_age} years"))
            break
    return w, r


def validate_income_vs_job(d: dict):
    w, r = [], []
    income, job = d.get("income", 0), d.get("job_title", "").lower()
    high_jobs = ["manager", "director", "ceo", "cto", "مدير", "رئيس", "doctor", "طبيب", "engineer", "مهندس"]
    entry_jobs = ["intern", "متدرب", "junior", "مبتدئ", "student", "طالب", "cashier", "كاشير"]
    if any(j in job for j in entry_jobs) and income > 25000:
        w.append(_warn("income_vs_job", "medium", "income",
                        f"الدخل ({income:,.0f}) مرتفع جداً لوظيفة ({d['job_title']})",
                        f"Income ({income:,.0f}) too high for ({d['job_title']})"))
        r.append(_rec("income", income,
                       f"النطاق المتوقع لوظيفة {d['job_title']}: 3,000 - 15,000",
                       f"Expected range for {d['job_title']}: 3,000 - 15,000"))
    if any(j in job for j in high_jobs) and income < 5000:
        w.append(_warn("income_vs_job", "medium", "income",
                        f"الدخل ({income:,.0f}) منخفض جداً لوظيفة ({d['job_title']})",
                        f"Income ({income:,.0f}) too low for ({d['job_title']})"))
        r.append(_rec("income", income,
                       f"النطاق المتوقع لوظيفة {d['job_title']}: 15,000 - 80,000+",
                       f"Expected range for {d['job_title']}: 15,000 - 80,000+"))
    return w, r


def validate_employment_vs_income(d: dict):
    w, r = [], []
    status, income = d.get("employment_status", "").lower(), d.get("income", 0)
    if any(t in status for t in ["unemployed", "عاطل", "غير موظف", "بدون عمل"]) and income > 10000:
        w.append(_warn("employment_vs_income", "high", "employment_status",
                        f"تعارض: حالة التوظيف ({d['employment_status']}) لا تتوافق مع الدخل ({income:,.0f})",
                        f"Conflict: Status ({d['employment_status']}) incompatible with income ({income:,.0f})"))
        r.append(_rec("employment_status", d["employment_status"],
                       "يرجى مراجعة حالة التوظيف أو تعديل الدخل",
                       "Review employment status or adjust income"))
    return w, r


def validate_age_range(d: dict):
    w, r = [], []
    age = d.get("age", 0)
    if age < 15 or age > 100:
        w.append(_warn("age_range", "low", "age",
                        f"العمر ({age}) خارج النطاق المتوقع (15-100)",
                        f"Age ({age}) outside expected range (15-100)"))
        r.append(_rec("age", age, "العمر المتوقع: 15-100 سنة", "Expected age: 15-100"))
    return w, r


def run_all_rules(data: dict) -> tuple[list[dict], list[dict]]:
    all_w, all_r = [], []
    for fn in [validate_experience_vs_age, validate_education_vs_age,
               validate_income_vs_job, validate_employment_vs_income, validate_age_range]:
        w, r = fn(data)
        all_w.extend(w)
        all_r.extend(r)
    return all_w, all_r
