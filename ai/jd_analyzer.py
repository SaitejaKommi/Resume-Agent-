from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, ValidationError

from ai._common import call_groq_json, normalize_text


class JDAnalysis(BaseModel):
    required_skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)
    role_category: str = ""
    seniority: str = "mid"
    responsibilities: list[str] = Field(default_factory=list)


SYSTEM_PROMPT = """You extract structured hiring data from job descriptions.
Return ONLY valid JSON with these keys:
- required_skills: array of strings
- preferred_skills: array of strings
- keywords: array of strings
- role_category: string
- seniority: one of junior, mid, senior
- responsibilities: array of strings
Do not include markdown, explanations, or trailing text."""


def _fallback_analyze_jd(jd_text: str) -> dict[str, Any]:
    text = normalize_text(jd_text)
    lowered = text.lower()
    seniority = "senior" if any(token in lowered for token in ["senior", "lead", "principal", "staff"]) else "junior" if any(token in lowered for token in ["junior", "entry", "graduate", "new grad"]) else "mid"
    role_category = "software engineering" if any(token in lowered for token in ["python", "fastapi", "react", "backend", "frontend", "full stack"]) else "technology"
    keywords = []
    for token in ["python", "fastapi", "sql", "postgresql", "docker", "aws", "react", "typescript", "llm", "ai", "api", "microservices"]:
        if token in lowered:
            keywords.append(token)
    return {
        "required_skills": keywords[:6],
        "preferred_skills": keywords[6:],
        "keywords": keywords,
        "role_category": role_category,
        "seniority": seniority,
        "responsibilities": [line.strip("-• ") for line in text.split(".") if line.strip()][:5],
    }


def analyze_jd(jd_text: str) -> dict:
    text = normalize_text(jd_text)
    system_prompt = SYSTEM_PROMPT
    user_prompt = f"Analyze this job description and return JSON only:\n\n{text}"

    try:
        payload = call_groq_json(system_prompt, user_prompt)
        analysis = JDAnalysis.model_validate(payload)
        return analysis.model_dump()
    except (RuntimeError, ValidationError, ValueError, TypeError):
        analysis = JDAnalysis.model_validate(_fallback_analyze_jd(text))
        return analysis.model_dump()
