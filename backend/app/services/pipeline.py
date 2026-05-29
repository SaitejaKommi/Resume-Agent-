from __future__ import annotations


def run_mock_resume_job_pipeline(resume_text: str, job_text: str, github_repos: list[str]) -> dict:
    resume_words = set(word.lower() for word in resume_text.split())
    job_words = set(word.lower() for word in job_text.split())
    overlap = sorted(resume_words.intersection(job_words))
    ats_score = round(min(100.0, 45.0 + len(overlap) * 4.0 + min(len(github_repos), 5) * 3.0), 2)
    return {
        "matched_terms": overlap,
        "suggestions": ["Add measurable impact bullets", "Mirror job keywords in the summary"],
        "ats_score": ats_score,
        "keyword_coverage": round((len(overlap) / max(len(job_words), 1)) * 100.0, 2),
    }
