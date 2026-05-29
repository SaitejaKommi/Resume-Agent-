from __future__ import annotations

import re

from ai.ats_scorer import compute_ats_score
from ai.bullet_optimizer import optimize_bullets
from ai.github_analyzer import analyze_github_repos
from ai.jd_analyzer import analyze_jd
from ai.project_ranker import rank_projects


def _extract_personal_info(resume_text: str) -> dict:
    lines = [line.strip() for line in resume_text.splitlines() if line.strip()]
    name = lines[0] if lines else ""
    email_match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", resume_text)
    phone_match = re.search(r"(?:\+?\d{1,3}[\s-]?)?(?:\(?\d{3}\)?[\s-]?)\d{3}[\s-]?\d{4}", resume_text)
    github_match = re.search(r"github\.com/[A-Za-z0-9_.-]+", resume_text, re.IGNORECASE)
    linkedin_match = re.search(r"linkedin\.com/in/[A-Za-z0-9_.-]+", resume_text, re.IGNORECASE)
    return {
        "name": name,
        "email": email_match.group(0) if email_match else "",
        "phone": phone_match.group(0) if phone_match else "",
        "github": github_match.group(0) if github_match else "",
        "linkedin": linkedin_match.group(0) if linkedin_match else "",
    }


def _extract_section_block(resume_text: str, headings: list[str]) -> list[str]:
    pattern = r"(?ims)^({})(.*?)(?=^\s*[A-Z][A-Z &/()-]{2,}\s*$|\Z)"
    joined = "|".join(re.escape(heading) for heading in headings)
    match = re.search(pattern.format(joined), resume_text)
    if not match:
        return []
    block = match.group(2)
    items = [line.strip("-• \t") for line in block.splitlines() if line.strip()]
    return items


def _extract_resume_sections(resume_text: str) -> dict:
    return {
        "skills": _extract_section_block(resume_text, ["Skills", "Technical Skills", "Core Skills"]),
        "experience": _extract_section_block(resume_text, ["Experience", "Work Experience", "Professional Experience"]),
        "education": _extract_section_block(resume_text, ["Education", "Academic Background"]),
        "projects": _extract_section_block(resume_text, ["Projects", "Selected Projects"]),
    }


def run_pipeline(resume_text: str, jd_text: str, github_repos: list[str], github_token: str) -> dict:
    jd_analysis = analyze_jd(jd_text)
    github_projects = analyze_github_repos(github_repos, github_token) if github_repos else []
    ranked_projects = rank_projects(github_projects, jd_analysis)

    for project in ranked_projects:
        project["bullets"] = optimize_bullets(project, jd_analysis)

    resume_sections = _extract_resume_sections(resume_text)
    ats_score = compute_ats_score(
        {
            "personal_info": _extract_personal_info(resume_text),
            "skills": resume_sections.get("skills", []),
            "projects": ranked_projects,
            "experience": resume_sections.get("experience", []),
            "education": resume_sections.get("education", []),
            "raw_text": resume_text,
        },
        jd_analysis,
    )

    skills = list(dict.fromkeys([*resume_sections.get("skills", []), *jd_analysis.get("required_skills", []), *jd_analysis.get("preferred_skills", [])]))
    project_items = ranked_projects or [
        {
            "name": "Resume optimization project",
            "url": "",
            "project_type": "project",
            "summary": "Resume optimization work tailored to the target job description.",
            "tech_stack": skills[:8],
            "relevance_score": 0.0,
            "bullets": [
                "Tailored resume content to align with role requirements and ATS keywords.",
                "Optimized project descriptions to highlight measurable impact and relevant technologies.",
                "Structured sections for strong ATS parsing and recruiter readability.",
            ],
        }
    ]

    return {
        "personal_info": _extract_personal_info(resume_text),
        "skills": skills,
        "projects": project_items,
        "experience": resume_sections.get("experience", []),
        "education": resume_sections.get("education", []),
        "ats_score": ats_score,
    }
