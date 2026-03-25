"""
طبقة التحقق بالنموذج اللغوي الكبير - LLM Validation Layer

يدعم أربعة مزودين: OpenAI / Anthropic / Google Gemini / Groq
مع fallback تلقائي إلى semantic_mock عند فشل الاتصال

المميزات:
  - Few-shot prompting باللغة العربية
  - مخرجات JSON منظمة مع parsing صارم
  - Caching لتقليل التكلفة
  - إعادة محاولة عند فشل JSON
  - إحصائيات استدعاءات LLM
"""

import os
import json
import hashlib
import logging
import time
import threading
import httpx
from cachetools import TTLCache

logger = logging.getLogger("basseer.llm")

# ─── Cache ───
_cache_ttl = int(os.environ.get("LLM_CACHE_TTL", "300"))
_cache = TTLCache(maxsize=512, ttl=_cache_ttl)

# ─── LLM Call Statistics ───
_stats_lock = threading.Lock()
_llm_stats = {
    "total_calls": 0,
    "successful_calls": 0,
    "failed_calls": 0,
    "cache_hits": 0,
    "total_latency_ms": 0.0,
    "last_error": None,
    "last_call_time": None,
}


def get_llm_stats() -> dict:
    """Return current LLM usage statistics."""
    with _stats_lock:
        stats = dict(_llm_stats)
        stats["average_latency_ms"] = round(
            stats["total_latency_ms"] / max(stats["successful_calls"], 1), 1
        )
        stats["cache_hit_rate"] = round(
            (stats["cache_hits"] / max(stats["total_calls"], 1)) * 100, 1
        )
        stats["cache_size"] = len(_cache)
        return stats


def _record_call(success: bool, latency_ms: float = 0, error: str = None, cache_hit: bool = False):
    with _stats_lock:
        _llm_stats["total_calls"] += 1
        if cache_hit:
            _llm_stats["cache_hits"] += 1
        if success:
            _llm_stats["successful_calls"] += 1
            _llm_stats["total_latency_ms"] += latency_ms
        else:
            _llm_stats["failed_calls"] += 1
            _llm_stats["last_error"] = error
        _llm_stats["last_call_time"] = time.time()


def _cache_key(data: dict) -> str:
    raw = json.dumps(data, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(raw.encode()).hexdigest()[:24]


# ─── LLM Settings Management ───

def get_llm_config() -> dict:
    """Get current LLM configuration from environment."""
    return {
        "provider": os.environ.get("LLM_PROVIDER", "offline").lower().strip(),
        "api_key": os.environ.get("LLM_API_KEY", "").strip(),
        "model": os.environ.get("LLM_MODEL", "").strip(),
    }


def save_llm_config(provider: str, api_key: str, model: str = ""):
    """Save LLM configuration to .env file and update environment."""
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))), ".env")

    # Update environment variables in-process
    os.environ["LLM_PROVIDER"] = provider
    os.environ["LLM_API_KEY"] = api_key
    os.environ["LLM_MODEL"] = model

    # Read existing .env or create new
    lines = []
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

    # Update or add keys
    keys_to_set = {
        "LLM_PROVIDER": provider,
        "LLM_API_KEY": api_key,
        "LLM_MODEL": model,
    }
    found_keys = set()
    new_lines = []
    for line in lines:
        stripped = line.strip()
        matched = False
        for key in keys_to_set:
            if stripped.startswith(f"{key}=") or stripped.startswith(f"# {key}="):
                new_lines.append(f"{key}={keys_to_set[key]}\n")
                found_keys.add(key)
                matched = True
                break
        if not matched:
            new_lines.append(line)

    # Add missing keys
    for key, val in keys_to_set.items():
        if key not in found_keys:
            new_lines.append(f"{key}={val}\n")

    with open(env_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

    logger.info(f"LLM config saved: provider={provider}, model={model}")
    return True


def is_llm_configured() -> bool:
    """Check if LLM is properly configured."""
    cfg = get_llm_config()
    return (
        cfg["provider"] not in ("offline", "")
        and cfg["api_key"] not in ("", "your-api-key-here")
    )


# ─── Few-shot Prompt ───

SYSTEM_PROMPT = """أنت "بصير AI" — نظام ذكي للكشف عن التناقضات المنطقية والدلالية في بيانات الاستبيانات الحكومية.

مهمتك: تحليل سجل استبيان واكتشاف أي تعارضات منطقية أو دلالية بين الحقول.

أجب **فقط** بكائن JSON واحد بدون أي نص إضافي. الصيغة المطلوبة:
{
  "violations": [
    {
      "field": "اسم الحقل بالإنجليزية",
      "severity": "high أو medium أو low",
      "message_ar": "وصف التعارض بالعربية بأسلوب لبق",
      "message_en": "وصف التعارض بالإنجليزية",
      "suggestion_ar": "التوصية بالعربية",
      "suggestion_en": "التوصية بالإنجليزية"
    }
  ],
  "overall_note_ar": "ملاحظة عامة بالعربية عن جودة السجل",
  "overall_note_en": "General note in English about record quality"
}

إذا لم تجد أي تعارض، أرجع: {"violations": [], "overall_note_ar": "البيانات متسقة ومنطقية", "overall_note_en": "Data is consistent and logical"}
"""

FEW_SHOT_EXAMPLES = [
    {
        "role": "user",
        "content": json.dumps({
            "age": 19, "experience_years": 15, "education": "PhD",
            "job_title": "Doctor", "income": 80000,
            "region": "الرياض", "employment_status": "Full-time"
        }, ensure_ascii=False)
    },
    {
        "role": "assistant",
        "content": json.dumps({
            "violations": [
                {
                    "field": "experience_years",
                    "severity": "high",
                    "message_ar": "مرحباً، يبدو أن هناك تعارضاً بين سنوات الخبرة (15) والعمر (19). أقصى خبرة ممكنة لهذا العمر: 9 سنوات",
                    "message_en": "Experience years (15) conflict with age (19). Max possible: 9",
                    "suggestion_ar": "نطاق الخبرة المقترح: 0-9 سنوات",
                    "suggestion_en": "Suggested range: 0-9 years"
                },
                {
                    "field": "education",
                    "severity": "high",
                    "message_ar": "الحصول على شهادة الدكتوراه في عمر 19 غير منطقي. الحد الأدنى المتوقع: 26 سنة",
                    "message_en": "PhD at age 19 is implausible. Minimum expected age: 26",
                    "suggestion_ar": "يرجى مراجعة العمر أو المؤهل التعليمي",
                    "suggestion_en": "Please review age or education level"
                }
            ],
            "overall_note_ar": "يوجد تعارضات حرجة متعددة — يرجى المراجعة",
            "overall_note_en": "Multiple critical conflicts found — review required"
        }, ensure_ascii=False)
    },
    {
        "role": "user",
        "content": json.dumps({
            "age": 35, "experience_years": 10, "education": "Bachelor",
            "job_title": "Data Analyst", "income": 18000,
            "region": "جدة", "employment_status": "Full-time"
        }, ensure_ascii=False)
    },
    {
        "role": "assistant",
        "content": json.dumps({
            "violations": [],
            "overall_note_ar": "البيانات متسقة ومنطقية",
            "overall_note_en": "Data is consistent and logical"
        }, ensure_ascii=False)
    },
    {
        "role": "user",
        "content": json.dumps({
            "age": 25, "experience_years": 3, "education": "High School",
            "job_title": "Surgeon", "income": 45000,
            "region": "مكة", "employment_status": "Full-time"
        }, ensure_ascii=False)
    },
    {
        "role": "assistant",
        "content": json.dumps({
            "violations": [
                {
                    "field": "job_title",
                    "severity": "high",
                    "message_ar": "وظيفة 'جراح' تتطلب شهادة طبية عليا وليس شهادة ثانوية فقط",
                    "message_en": "Surgeon role requires advanced medical degree, not just High School",
                    "suggestion_ar": "يرجى مراجعة المؤهل التعليمي أو المسمى الوظيفي",
                    "suggestion_en": "Review education level or job title"
                }
            ],
            "overall_note_ar": "تعارض دلالي بين التعليم والمسمى الوظيفي",
            "overall_note_en": "Semantic conflict between education and job title"
        }, ensure_ascii=False)
    }
]


# ─── Provider-specific callers ───

def _call_openai(messages: list[dict], model: str, api_key: str) -> str:
    resp = httpx.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"model": model or "gpt-4o-mini", "messages": messages,
              "temperature": 0.1, "max_tokens": 1500},
        timeout=30.0,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


def _call_anthropic(messages: list[dict], model: str, api_key: str) -> str:
    system = messages[0]["content"] if messages[0]["role"] == "system" else ""
    api_msgs = [m for m in messages if m["role"] != "system"]
    resp = httpx.post(
        "https://api.anthropic.com/v1/messages",
        headers={"x-api-key": api_key, "Content-Type": "application/json",
                 "anthropic-version": "2023-06-01"},
        json={"model": model or "claude-sonnet-4-20250514", "max_tokens": 1500,
              "system": system, "messages": api_msgs, "temperature": 0.1},
        timeout=30.0,
    )
    resp.raise_for_status()
    return resp.json()["content"][0]["text"]


def _call_gemini(messages: list[dict], model: str, api_key: str) -> str:
    model_name = model or "gemini-1.5-flash"
    system_text = ""
    parts = []
    for m in messages:
        if m["role"] == "system":
            system_text = m["content"]
        else:
            role = "user" if m["role"] == "user" else "model"
            parts.append({"role": role, "parts": [{"text": m["content"]}]})
    body = {"contents": parts, "generationConfig": {"temperature": 0.1, "maxOutputTokens": 1500}}
    if system_text:
        body["systemInstruction"] = {"parts": [{"text": system_text}]}
    resp = httpx.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}",
        headers={"Content-Type": "application/json"},
        json=body,
        timeout=30.0,
    )
    resp.raise_for_status()
    return resp.json()["candidates"][0]["content"]["parts"][0]["text"]


def _call_groq(messages: list[dict], model: str, api_key: str) -> str:
    """Groq Cloud — OpenAI-compatible chat completions endpoint."""
    resp = httpx.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"model": model or "llama-3.3-70b-versatile", "messages": messages,
              "temperature": 0.1, "max_tokens": 1500},
        timeout=30.0,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


PROVIDERS = {
    "openai": _call_openai,
    "anthropic": _call_anthropic,
    "gemini": _call_gemini,
    "groq": _call_groq,
}


def _parse_llm_json(raw: str) -> dict:
    """Parse JSON من مخرج LLM — يتعامل مع backticks و text حوله"""
    text = raw.strip()
    # إزالة markdown code fences
    if "```" in text:
        parts = text.split("```")
        for part in parts:
            clean = part.strip()
            if clean.startswith("json"):
                clean = clean[4:].strip()
            if clean.startswith("{"):
                text = clean
                break
    # محاولة إيجاد أول { وآخر }
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1:
        text = text[start:end + 1]
    return json.loads(text)


def call_llm(data: dict) -> tuple[list[dict], list[dict], bool, str]:
    """
    استدعاء LLM للتحقق الدلالي

    Returns: (warnings, recommendations, llm_was_used, overall_note_en)
    """
    provider = os.environ.get("LLM_PROVIDER", "offline").lower().strip()
    api_key = os.environ.get("LLM_API_KEY", "").strip()
    model = os.environ.get("LLM_MODEL", "").strip()

    if provider == "offline" or not api_key or api_key == "your-api-key-here":
        return [], [], False, ""

    if provider not in PROVIDERS:
        logger.warning(f"Unknown LLM provider: {provider}, falling back to offline")
        return [], [], False, ""

    # التحقق من الكاش
    ck = _cache_key(data)
    if ck in _cache:
        cached = _cache[ck]
        _record_call(success=True, cache_hit=True)
        return cached[0], cached[1], True, cached[2] if len(cached) > 2 else ""

    # بناء الرسائل مع few-shot examples
    record_json = json.dumps({
        "age": data.get("age"), "experience_years": data.get("experience_years"),
        "education": data.get("education"), "job_title": data.get("job_title"),
        "income": data.get("income"), "region": data.get("region"),
        "employment_status": data.get("employment_status"),
    }, ensure_ascii=False)

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(FEW_SHOT_EXAMPLES)
    messages.append({"role": "user", "content": record_json})

    caller = PROVIDERS[provider]

    # محاولتان لاستخراج JSON
    for attempt in range(2):
        try:
            t0 = time.perf_counter()
            raw = caller(messages, model, api_key)
            call_latency = (time.perf_counter() - t0) * 1000

            parsed = _parse_llm_json(raw)

            warnings = []
            recommendations = []
            overall_note_en = parsed.get("overall_note_en", "")

            for v in parsed.get("violations", []):
                warnings.append({
                    "rule": f"llm_{v.get('field', 'unknown')}",
                    "severity": v.get("severity", "medium"),
                    "field": v.get("field", "unknown"),
                    "message_ar": v.get("message_ar", ""),
                    "message_en": v.get("message_en", ""),
                    "source": "llm",
                })
                recommendations.append({
                    "field": v.get("field", "unknown"),
                    "current_value": str(data.get(v.get("field", ""), "")),
                    "suggestion_ar": v.get("suggestion_ar", ""),
                    "suggestion_en": v.get("suggestion_en", ""),
                })

            # حفظ في الكاش
            _cache[ck] = (warnings, recommendations, overall_note_en)
            _record_call(success=True, latency_ms=call_latency)
            return warnings, recommendations, True, overall_note_en

        except json.JSONDecodeError:
            if attempt == 0:
                logger.warning("LLM JSON parse failed, retrying...")
                messages.append({"role": "user",
                                 "content": "الرجاء إرجاع JSON صالح فقط بدون أي نص إضافي."})
                continue
            else:
                logger.error("LLM JSON parse failed after retry")
                _record_call(success=False, error="JSON parse failed")
                return [], [], False, ""

        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            _record_call(success=False, error=str(e))
            return [], [], False, ""

    return [], [], False, ""
