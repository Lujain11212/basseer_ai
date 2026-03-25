"""
اختبارات وحدوية - Unit Tests
pytest tests/test_core.py
"""
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ═══════════════════════════════════════
# Tests: Rules Layer
# ═══════════════════════════════════════

class TestRules:
    def test_experience_vs_age_conflict(self):
        from backend.validators.rules import validate_experience_vs_age
        w, r = validate_experience_vs_age({"age": 22, "experience_years": 15})
        assert len(w) == 1
        assert w[0]["severity"] == "high"
        assert w[0]["field"] == "experience_years"

    def test_experience_vs_age_clean(self):
        from backend.validators.rules import validate_experience_vs_age
        w, r = validate_experience_vs_age({"age": 35, "experience_years": 10})
        assert len(w) == 0

    def test_education_vs_age_phd(self):
        from backend.validators.rules import validate_education_vs_age
        w, r = validate_education_vs_age({"age": 20, "education": "PhD"})
        assert len(w) == 1
        assert w[0]["severity"] == "high"

    def test_education_vs_age_clean(self):
        from backend.validators.rules import validate_education_vs_age
        w, r = validate_education_vs_age({"age": 30, "education": "PhD"})
        assert len(w) == 0

    def test_income_vs_job_high_income_entry(self):
        from backend.validators.rules import validate_income_vs_job
        w, r = validate_income_vs_job({"income": 50000, "job_title": "Intern"})
        assert len(w) >= 1

    def test_employment_vs_income(self):
        from backend.validators.rules import validate_employment_vs_income
        w, r = validate_employment_vs_income({"employment_status": "عاطل", "income": 50000})
        assert len(w) == 1
        assert w[0]["severity"] == "high"

    def test_run_all_rules_multiple(self):
        from backend.validators.rules import run_all_rules
        w, r = run_all_rules({
            "age": 19, "experience_years": 15, "education": "PhD",
            "job_title": "Doctor", "income": 80000,
            "region": "الرياض", "employment_status": "Full-time"
        })
        assert len(w) >= 2


# ═══════════════════════════════════════
# Tests: Scoring
# ═══════════════════════════════════════

class TestScoring:
    def test_perfect_score(self):
        from backend.validators.scoring import calculate_confidence
        score, label, reason = calculate_confidence([], {"age": 30, "experience_years": 5,
            "education": "Bachelor", "job_title": "Dev", "income": 15000,
            "region": "الرياض", "employment_status": "Full-time"})
        assert score == 100.0
        assert label == "High confidence"

    def test_high_violations(self):
        from backend.validators.scoring import calculate_confidence
        warnings = [{"severity": "high"}, {"severity": "high"}, {"severity": "high"}]
        score, label, reason = calculate_confidence(warnings)
        assert score == 25.0
        assert label == "Low confidence"

    def test_mixed_violations(self):
        from backend.validators.scoring import calculate_confidence
        warnings = [{"severity": "high"}, {"severity": "medium"}]
        score, label, reason = calculate_confidence(warnings)
        assert score == 63.0  # 100 - 25 - 12
        assert label == "Medium confidence"

    def test_missing_fields_penalty(self):
        from backend.validators.scoring import calculate_confidence
        data = {"age": 30, "experience_years": 5, "education": "", "job_title": "",
                "income": 10000, "region": "الرياض", "employment_status": "Full-time"}
        score, label, reason = calculate_confidence([], data)
        assert score < 100

    def test_reason_arabic(self):
        from backend.validators.scoring import calculate_confidence
        warnings = [{"severity": "high"}]
        _, _, reason = calculate_confidence(warnings)
        assert "حرجة" in reason


# ═══════════════════════════════════════
# Tests: LLM JSON Parsing
# ═══════════════════════════════════════

class TestLLMParsing:
    def test_clean_json(self):
        from backend.validators.llm_layer import _parse_llm_json
        raw = '{"violations": [], "overall_note_ar": "بيانات جيدة"}'
        result = _parse_llm_json(raw)
        assert result["violations"] == []

    def test_json_with_backticks(self):
        from backend.validators.llm_layer import _parse_llm_json
        raw = '```json\n{"violations": [{"field": "age", "severity": "high"}]}\n```'
        result = _parse_llm_json(raw)
        assert len(result["violations"]) == 1

    def test_json_with_surrounding_text(self):
        from backend.validators.llm_layer import _parse_llm_json
        raw = 'Here is the result:\n{"violations": []}\nEnd of response.'
        result = _parse_llm_json(raw)
        assert result["violations"] == []

    def test_invalid_json_raises(self):
        from backend.validators.llm_layer import _parse_llm_json
        import pytest
        with pytest.raises(json.JSONDecodeError):
            _parse_llm_json("This is not JSON at all")

    def test_call_llm_offline(self):
        """يجب أن يرجع فارغ في وضع offline"""
        os.environ["LLM_PROVIDER"] = "offline"
        from backend.validators.llm_layer import call_llm
        w, r, used, note = call_llm({"age": 22, "experience_years": 15})
        assert used is False
        assert w == []

    def test_llm_stats(self):
        from backend.validators.llm_layer import get_llm_stats
        stats = get_llm_stats()
        assert "total_calls" in stats
        assert "cache_hit_rate" in stats

    def test_llm_config(self):
        from backend.validators.llm_layer import get_llm_config, is_llm_configured
        os.environ["LLM_PROVIDER"] = "offline"
        cfg = get_llm_config()
        assert cfg["provider"] == "offline"
        assert not is_llm_configured()


# ═══════════════════════════════════════
# Tests: Pipeline
# ═══════════════════════════════════════

class TestPipeline:
    def test_pipeline_returns_all_fields(self):
        os.environ["LLM_PROVIDER"] = "offline"
        from services.pipeline import run_pipeline
        result = run_pipeline({
            "age": 22, "experience_years": 15, "education": "PhD",
            "job_title": "Engineer", "income": 45000,
            "region": "الرياض", "employment_status": "Full-time"
        })
        assert "confidence_score" in result
        assert "warnings" in result
        assert "recommendations" in result
        assert "latency_ms" in result
        assert "llm_used" in result
        assert "detected_by" in result
        assert "confidence_reason_en" in result
        assert result["contradictions_count"] >= 2
        assert result["detected_by"] == "rule"

    def test_pipeline_clean_data(self):
        os.environ["LLM_PROVIDER"] = "offline"
        from services.pipeline import run_pipeline
        result = run_pipeline({
            "age": 35, "experience_years": 10, "education": "Bachelor",
            "job_title": "Analyst", "income": 18000,
            "region": "جدة", "employment_status": "Full-time"
        })
        assert result["confidence_score"] == 100.0
        assert result["contradictions_count"] == 0
        assert result["confidence_reason_en"] == "No inconsistencies detected — data is consistent"

    def test_pipeline_recommendations_engine(self):
        os.environ["LLM_PROVIDER"] = "offline"
        from services.pipeline import run_pipeline
        result = run_pipeline({
            "age": 19, "experience_years": 15, "education": "PhD",
            "job_title": "Doctor", "income": 80000,
            "region": "الرياض", "employment_status": "Full-time"
        })
        # Should have system-level recommendations
        sys_recs = [r for r in result["recommendations"] if "message_ar" in r]
        assert len(sys_recs) >= 1
