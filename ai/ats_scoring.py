from __future__ import annotations

from ai.skill_extractor import extract_skills


def score_resume_against_job(resume_text: str, job_skills: list[str]) -> float:
    if not job_skills:
        return 50.0

    resume_skills = set(extract_skills(resume_text))
    job_skill_set = set(job_skills)
    overlap = resume_skills.intersection(job_skill_set)

    coverage = len(overlap) / max(len(job_skill_set), 1)
    resume_strength = min(len(resume_text.split()) / 800.0, 1.0)
    score = 35.0 + (coverage * 55.0) + (resume_strength * 10.0)
    return round(min(score, 100.0), 2)
