from __future__ import annotations

import re

SKILL_LIBRARY = [
    "Python",
    "FastAPI",
    "SQLAlchemy",
    "PostgreSQL",
    "Docker",
    "Kubernetes",
    "AWS",
    "Azure",
    "GCP",
    "TypeScript",
    "React",
    "Next.js",
    "Tailwind CSS",
    "GitHub",
    "OAuth",
    "REST",
    "GraphQL",
    "Redis",
    "Celery",
    "PyTorch",
    "TensorFlow",
    "OpenAI",
    "Groq",
    "LangChain",
    "LLM",
    "NLP",
    "CI/CD",
    "pytest",
    "Git",
    "Linux",
    "Vector Search",
    "MongoDB",
]


def extract_skills(text: str) -> list[str]:
    normalized = text.lower()
    matches: list[str] = []
    for skill in SKILL_LIBRARY:
        pattern = re.escape(skill.lower()).replace(r"\.js", r"\.?js")
        if re.search(rf"\b{pattern}\b", normalized):
            matches.append(skill)
    return sorted(set(matches))
