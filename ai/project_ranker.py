from __future__ import annotations

from functools import lru_cache
from typing import Any

import numpy as np

from ai._common import safe_lower_set


@lru_cache(maxsize=1)
def _get_model() -> Any:
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError as exc:
        raise RuntimeError("sentence-transformers is required for project ranking") from exc

    return SentenceTransformer("all-MiniLM-L6-v2")


def _cosine_similarity(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
    denominator = (np.linalg.norm(vec_a) * np.linalg.norm(vec_b)) or 1e-9
    return float(np.dot(vec_a, vec_b) / denominator)


def rank_projects(projects: list[dict], jd_analysis: dict) -> list[dict]:
    if not projects:
        return []

    model = _get_model()
    jd_keywords = " ".join(jd_analysis.get("keywords", []) + jd_analysis.get("required_skills", []) + jd_analysis.get("preferred_skills", []))
    jd_embedding = np.asarray(model.encode(jd_keywords or "job description"), dtype=float)
    required_skills = safe_lower_set(jd_analysis.get("required_skills", []))

    ranked: list[dict] = []
    for project in projects:
        summary = project.get("summary") or project.get("readme") or project.get("name") or "project"
        project_embedding = np.asarray(model.encode(summary), dtype=float)
        semantic_similarity = (_cosine_similarity(project_embedding, jd_embedding) + 1.0) / 2.0

        tech_stack = safe_lower_set(project.get("tech_stack", []))
        overlap_count = len(required_skills.intersection(tech_stack))
        skill_overlap_ratio = overlap_count / max(len(required_skills), 1)

        relevance_score = round((0.6 * semantic_similarity + 0.4 * skill_overlap_ratio) * 100.0, 2)
        updated = dict(project)
        updated["relevance_score"] = relevance_score
        ranked.append(updated)

    ranked.sort(key=lambda item: item["relevance_score"], reverse=True)
    return ranked[:3]
