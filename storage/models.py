"""
نماذج قاعدة البيانات - Database Models
"""
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Boolean
from sqlalchemy.orm import declarative_base
from datetime import datetime, timezone

Base = declarative_base()


class SurveyResponse(Base):
    __tablename__ = "survey_responses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # حقول الاستبيان
    age = Column(Integer, nullable=False)
    experience_years = Column(Integer, nullable=False)
    education = Column(String(100), nullable=False)
    job_title = Column(String(200), nullable=False)
    income = Column(Float, nullable=False)
    region = Column(String(100), nullable=False)
    employment_status = Column(String(50), nullable=False)
    enumerator_id = Column(String(50), default="default")

    # نتائج التحقق
    confidence_score = Column(Float, default=100.0)
    confidence_label = Column(String(50), default="High confidence")
    confidence_reason_ar = Column(Text, default="")
    confidence_reason_en = Column(Text, default="")
    warnings_json = Column(Text, default="[]")
    recommendations_json = Column(Text, default="[]")
    contradictions_count = Column(Integer, default=0)
    missing_fields_count = Column(Integer, default=0)

    # معلومات التحقق
    detected_by = Column(String(20), default="rule")  # rule | llm | hybrid
    llm_used = Column(Boolean, default=False)
    llm_provider = Column(String(30), default="offline")
    latency_ms = Column(Float, default=0.0)

    # حالة المراجعة (للباحث الميداني)
    review_status = Column(String(30), default="pending")  # pending | reviewed | confirmed | escalated | correction_requested
    reviewer_note = Column(Text, default="")

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class ValidationLog(Base):
    __tablename__ = "validation_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    response_id = Column(Integer, nullable=False)
    rule_name = Column(String(200), nullable=False)
    severity = Column(String(20), nullable=False)
    field = Column(String(100), nullable=False)
    message = Column(Text, nullable=False)
    source = Column(String(20), default="rules")  # rules | semantic | llm
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
