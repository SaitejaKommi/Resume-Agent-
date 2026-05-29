from __future__ import annotations

from pydantic import BaseModel, Field, ValidationError

from ai._common import call_groq_json, normalize_text


SYSTEM_PROMPT = """You rewrite project experience into ATS-optimized resume bullet points.
Return ONLY JSON: {"bullets": ["...", "...", "..."]} or 4 bullets.
Rules:
- each bullet must start with a strong action verb
- include metrics or impact if available or inferred
- mention relevant technology stack
- mirror job keywords naturally
- no fluff, no first person, no markdown"""


class BulletResponse(BaseModel):
    bullets: list[str] = Field(default_factory=list)


def _fallback_bullets(project: dict, jd_analysis: dict) -> list[str]:
    tech_stack = ", ".join(project.get("tech_stack", [])[:5]) or "the project stack"
    project_name = project.get("name", "the project")
    project_type = project.get("project_type", "project")
    keywords = ", ".join(jd_analysis.get("keywords", [])[:3]) or "role-specific requirements"
    complexity = project.get("complexity_score", 5)
    return [
        f"Built {project_name}, a {project_type}, using {tech_stack} to deliver production-ready functionality with a complexity score of {complexity}/10.",
        f"Optimized core workflows in {project_name} by aligning the implementation with {keywords} and improving maintainability across modules.",
        f"Integrated relevant technologies from the stack to support scalable delivery, clean architecture, and measurable project impact.",
    ]


def optimize_bullets(project: dict, jd_analysis: dict) -> list[str]:
    project_text = normalize_text(project.get("summary") or project.get("readme") or project.get("description") or project.get("name") or "")
    user_prompt = f"Project:\n{project_text}\n\nProject data:\n{project}\n\nJD analysis:\n{jd_analysis}"

    try:
        payload = call_groq_json(SYSTEM_PROMPT, user_prompt)
        response = BulletResponse.model_validate(payload)
        bullets = [bullet.strip() for bullet in response.bullets if bullet and bullet.strip()]
        if 3 <= len(bullets) <= 4:
            return bullets[:4]
    except (RuntimeError, ValidationError, ValueError, TypeError):
        pass

    return _fallback_bullets(project, jd_analysis)
