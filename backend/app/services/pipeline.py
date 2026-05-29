from __future__ import annotations

from ai.pipeline import run_pipeline


def run_mock_resume_job_pipeline(resume_text: str, job_text: str, github_repos: list[str], github_token: str = "") -> dict:
    return run_pipeline(resume_text=resume_text, jd_text=job_text, github_repos=github_repos, github_token=github_token)
