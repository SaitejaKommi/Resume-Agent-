from __future__ import annotations

import re

from ai._common import safe_lower_set


SECTION_PATTERNS = {
    "education": [r"^education\b", r"^academic background\b"],
    "experience": [r"^experience\b", r"^work experience\b", r"^employment\b"],
    "skills": [r"^skills\b", r"^technical skills\b"],
    "projects": [r"^projects\b", r"^selected projects\b"],
}


def _flatten_resume_text(resume_json: dict) -> str:
    parts: list[str] = []
    for key, value in resume_json.items():
        if isinstance(value, str):
            parts.append(value)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, str):
                    parts.append(item)
                elif isinstance(item, dict):
                    parts.extend(str(v) for v in item.values() if isinstance(v, str))
        elif isinstance(value, dict):
            parts.extend(str(v) for v in value.values() if isinstance(v, str))
    return "\n".join(parts)


def _section_completeness(resume_text: str) -> float:
    lowered = resume_text.lower()
    present = 0
    for patterns in SECTION_PATTERNS.values():
        if any(re.search(pattern, lowered, re.MULTILINE) for pattern in patterns):
            present += 1
    return round((present / len(SECTION_PATTERNS)) * 100.0, 2)


def compute_ats_score(resume_json: dict, jd_analysis: dict) -> dict:
    resume_text = _flatten_resume_text(resume_json)
    resume_skills = safe_lower_set(resume_json.get("skills", []))
    required_skills = safe_lower_set(jd_analysis.get("required_skills", []))

    matched = sorted(required_skills.intersection(resume_skills))
    missing = sorted(required_skills.difference(resume_skills))
    keyword_coverage = round((len(matched) / max(len(required_skills), 1)) * 100.0, 2)
    section_completeness = _section_completeness(resume_text)
    formatting_score = 90.0
    total_score = round((0.55 * keyword_coverage) + (0.15 * section_completeness) + (0.3 * formatting_score), 2)

    suggestions = []
    if missing:
        suggestions.append(f"Add the following required skills where accurate: {', '.join(missing[:8])}.")
    if section_completeness < 100:
        suggestions.append("Add or strengthen education, experience, skills, and projects section headings.")
    if formatting_score < 95:
        suggestions.append("Use a clean LaTeX template layout to preserve consistent ATS parsing.")

    if not suggestions:
        suggestions.append("Resume structure and keyword coverage are strong; tailor bullets to the target role.")

    return {
        "total_score": total_score,
        "keyword_coverage": keyword_coverage,
        "missing_keywords": missing,
        "suggestions": suggestions,
        "formatting_score": formatting_score,
        "section_completeness": section_completeness,
    }
