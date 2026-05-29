from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape


LATEX_SPECIAL_CHARS = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}


def escape_latex(text: str) -> str:
    escaped = text
    for character, replacement in LATEX_SPECIAL_CHARS.items():
        escaped = escaped.replace(character, replacement)
    return escaped


def _escape_value(value: Any) -> Any:
    if isinstance(value, str):
        return escape_latex(value)
    if isinstance(value, dict):
        return {key: _escape_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_escape_value(item) for item in value]
    return value


def _normalize_resume_json(resume_json: dict) -> dict:
    personal = _escape_value(resume_json.get("personal") or resume_json.get("personal_info") or {})
    skills = _escape_value(resume_json.get("skills") or {})
    projects = _escape_value(resume_json.get("projects") or [])
    experience = _escape_value(resume_json.get("experience") or [])
    education = _escape_value(resume_json.get("education") or [])
    summary = _escape_value(resume_json.get("summary") or resume_json.get("headline") or "")
    return {
        "personal": personal,
        "skills": skills,
        "projects": projects,
        "experience": experience,
        "education": education,
        "summary": summary,
    }


def _find_tectonic() -> str | None:
    return shutil.which("tectonic")


def _find_pdflatex() -> str | None:
    return shutil.which("pdflatex")


def _build_pdf_with_tectonic(tex_path: Path, work_dir: Path) -> Path:
    executable = _find_tectonic()
    if executable is None:
        raise FileNotFoundError("tectonic is not installed")
    result = subprocess.run(
        [executable, tex_path.name],
        cwd=str(work_dir),
        check=True,
        capture_output=True,
        text=True,
    )
    pdf_path = tex_path.with_suffix(".pdf")
    if not pdf_path.exists():
        raise RuntimeError(f"tectonic completed but did not produce {pdf_path.name}: {result.stdout}\n{result.stderr}")
    return pdf_path


def _build_pdf_with_pdflatex(tex_path: Path, work_dir: Path) -> Path:
    executable = _find_pdflatex()
    if executable is None:
        raise FileNotFoundError("pdflatex is not installed")
    subprocess.run(
        [executable, "-interaction=nonstopmode", "-halt-on-error", tex_path.name],
        cwd=str(work_dir),
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        [executable, "-interaction=nonstopmode", "-halt-on-error", tex_path.name],
        cwd=str(work_dir),
        check=True,
        capture_output=True,
        text=True,
    )
    pdf_path = tex_path.with_suffix(".pdf")
    if not pdf_path.exists():
        raise RuntimeError(f"pdflatex completed but did not produce {pdf_path.name}")
    return pdf_path


def _render_template(resume_json: dict) -> str:
    project_root = Path(__file__).resolve().parents[1]
    templates_dir = project_root / "templates"
    if not templates_dir.exists():
        templates_dir = project_root.parent / "templates"
    env = Environment(
        loader=FileSystemLoader(str(templates_dir)),
        autoescape=select_autoescape(enabled_extensions=()),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template("resume.tex.j2")
    return template.render(**_normalize_resume_json(resume_json))


def generate_pdf(resume_json: dict, output_path: str) -> str:
    output_file = Path(output_path).expanduser().resolve()
    output_file.parent.mkdir(parents=True, exist_ok=True)

    rendered_tex = _render_template(resume_json)

    with tempfile.TemporaryDirectory(prefix="resumeagent_pdf_") as temp_dir:
        temp_path = Path(temp_dir)
        tex_path = temp_path / "resume.tex"
        tex_path.write_text(rendered_tex, encoding="utf-8")

        try:
            pdf_path = _build_pdf_with_tectonic(tex_path, temp_path)
        except FileNotFoundError:
            pdf_path = _build_pdf_with_pdflatex(tex_path, temp_path)

        shutil.move(str(pdf_path), str(output_file))

    return str(output_file)
