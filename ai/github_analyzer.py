from __future__ import annotations

import base64
import configparser
import json
import re
from datetime import datetime, timezone
from urllib.parse import urlparse

from github import Github
from pydantic import BaseModel, Field, ValidationError

from ai._common import call_groq_json, normalize_text, safe_lower_set


SYSTEM_PROMPT = """You summarize GitHub projects for resume optimization.
Return ONLY JSON with keys:
- summary: string
- project_type: string
Do not include markdown or commentary."""


class GitHubProject(BaseModel):
    name: str
    url: str
    description: str = ""
    readme: str = ""
    languages: list[str] = Field(default_factory=list)
    dependencies: list[str] = Field(default_factory=list)
    stars: int = 0
    last_updated: str = ""
    tech_stack: list[str] = Field(default_factory=list)
    project_type: str = "project"
    summary: str = ""
    complexity_score: int = 1


def _parse_repo_url(repo_url: str) -> tuple[str, str]:
    parsed = urlparse(repo_url)
    path = parsed.path.strip("/")
    if not path or "/" not in path:
        raise ValueError(f"Invalid GitHub repo URL: {repo_url}")
    owner, repo = path.split("/", 1)
    repo = repo.removesuffix(".git")
    return owner, repo


def _read_text_file(repo, path: str, ref: str | None = None) -> str:
    try:
        contents = repo.get_contents(path, ref=ref)
    except Exception:
        return ""
    if isinstance(contents, list):
        return ""
    decoded = contents.decoded_content or b""
    return decoded.decode("utf-8", errors="ignore")


def _collect_repo_files(repo, ref: str | None = None) -> tuple[str, list[str]]:
    readme = ""
    dependencies: list[str] = []

    def walk(path: str = "") -> None:
        nonlocal readme, dependencies
        try:
            contents = repo.get_contents(path, ref=ref)
        except Exception:
            return
        if not isinstance(contents, list):
            if contents.name.lower().startswith("readme") and not readme:
                readme = contents.decoded_content.decode("utf-8", errors="ignore")[:2000]
            return

        for item in contents:
            if item.type == "dir":
                walk(item.path)
            elif item.type == "file":
                lower_name = item.name.lower()
                if lower_name.startswith("readme") and not readme:
                    readme = item.decoded_content.decode("utf-8", errors="ignore")[:2000]
                elif lower_name == "package.json":
                    try:
                        package_data = json.loads(item.decoded_content.decode("utf-8", errors="ignore"))
                        for section in ["dependencies", "devDependencies", "peerDependencies"]:
                            dependencies.extend(list((package_data.get(section) or {}).keys()))
                    except Exception:
                        pass
                elif lower_name in {"requirements.txt", "pyproject.toml", "poetry.lock"}:
                    text = item.decoded_content.decode("utf-8", errors="ignore")
                    if lower_name == "requirements.txt":
                        for line in text.splitlines():
                            line = line.strip()
                            if line and not line.startswith("#"):
                                dependencies.append(re.split(r"[<>=~ ]+", line)[0])
                    elif lower_name == "pyproject.toml":
                        for match in re.findall(r'(?m)^\s*[A-Za-z0-9_.-]+\s*=\s*["\']([^"\']+)["\']', text):
                            dependencies.append(match)

    walk("")
    return readme, sorted(set(dependencies))


def _summarize_repo(readme: str, dependencies: list[str], tech_stack: list[str]) -> tuple[str, str]:
    try:
        payload = call_groq_json(
            SYSTEM_PROMPT,
            f"README:\n{readme[:2000]}\n\nDependencies:\n{dependencies}\n\nTech stack:\n{tech_stack}",
        )
        summary = str(payload.get("summary", "")).strip()
        project_type = str(payload.get("project_type", "project")).strip() or "project"
        if summary:
            return summary, project_type
    except Exception:
        pass

    summary = normalize_text(readme)[:300]
    if not summary:
        summary = "Project repository with documented implementation details."
    project_type = "application" if any(token in " ".join(tech_stack).lower() for token in ["react", "next.js", "fastapi", "django", "flask"]) else "library"
    return summary, project_type


def _complexity_score(stars: int, languages: list[str], dependencies: list[str], readme: str) -> int:
    score = 1
    score += 1 if len(languages) >= 2 else 0
    score += 1 if len(dependencies) >= 5 else 0
    score += 1 if len(readme) > 500 else 0
    score += 1 if stars >= 10 else 0
    score += 1 if any(token in readme.lower() for token in ["authentication", "pipeline", "database", "deployment", "docker"]) else 0
    score += 1 if len(dependencies) >= 15 else 0
    score += 1 if len(languages) >= 4 else 0
    return max(1, min(score, 10))


def analyze_github_repos(repo_urls: list[str], github_token: str) -> list[dict]:
    client = Github(github_token) if github_token else Github()
    projects: list[dict] = []

    for repo_url in repo_urls:
        owner, repo_name = _parse_repo_url(repo_url)
        repo = client.get_repo(f"{owner}/{repo_name}")
        readme, dependencies = _collect_repo_files(repo)
        languages = sorted([language for language in (repo.get_languages() or {}).keys()])
        tech_stack = sorted(set([*languages, *dependencies]))
        summary, project_type = _summarize_repo(readme, dependencies, tech_stack)
        project = GitHubProject(
            name=repo.name,
            url=repo.html_url,
            description=repo.description or "",
            readme=readme[:2000],
            languages=languages,
            dependencies=dependencies,
            stars=int(repo.stargazers_count or 0),
            last_updated=repo.updated_at.astimezone(timezone.utc).isoformat() if repo.updated_at else "",
            tech_stack=tech_stack,
            project_type=project_type,
            summary=summary,
            complexity_score=_complexity_score(int(repo.stargazers_count or 0), languages, dependencies, readme),
        )
        projects.append(project.model_dump())

    return projects
