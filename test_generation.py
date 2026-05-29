from __future__ import annotations

import tempfile
from pathlib import Path

from ai.resume_generator import generate_pdf


def main() -> None:
    resume_json = {
        "personal": {
            "name": "Saiteja Kommi",
            "email": "kommisaiteja4437@gmail.com",
            "phone": "+91-9666376305",
            "github": "github.com/SaitejaKommi",
            "linkedin": "linkedin.com/in/saiteja-kommi-19a962313",
            "portfolio": "saitejakommi.dev",
        },
        "skills": {
            "Languages": ["Python", "Java", "JavaScript"],
            "Backend": ["FastAPI", "SQLAlchemy", "PostgreSQL"],
            "AI/ML": ["Groq", "sentence-transformers", "PyTorch"],
        },
        "projects": [
            {
                "name": "ResumeAgent",
                "year": "2026",
                "tech_tags": ["FastAPI", "Groq", "Tectonic", "Jinja2"],
                "bullets": [
                    "Built an AI-powered resume optimization workflow that generates tailored PDF resumes from structured JSON.",
                    "Integrated Groq and sentence-transformers to rank projects and optimize bullet points for ATS relevance.",
                    "Implemented LaTeX rendering with safe escaping and automatic fallback compilation for reliable PDF generation.",
                ],
                "link": "github.com/SaitejaKommi/Resume-Agent-",
            }
        ],
        "experience": [
            {
                "company": "ResumeAgent Labs",
                "title": "Software Engineer",
                "dates": "2026",
                "location": "Remote",
                "bullets": [
                    "Designed the resume generation pipeline and ensured the output remained ATS-friendly and single-page.",
                    "Created reusable backend routes for PDF generation and download workflows.",
                ],
            }
        ],
        "education": [
            {
                "institution": "Birla Institute of Technology and Science, Pilani",
                "degree": "B.S. Computer Science",
                "dates": "2024 -- 2027",
                "location": "Pilani, India",
            }
        ],
        "summary": "AI resume optimization platform focused on clean ATS-compatible output.",
    }

    with tempfile.TemporaryDirectory(prefix="resumeagent_test_") as temp_dir:
        output_path = Path(temp_dir) / "resume.pdf"
        generated = generate_pdf(resume_json, str(output_path))
        pdf_path = Path(generated)
        assert pdf_path.exists(), "PDF file was not created"
        assert pdf_path.stat().st_size > 0, "Generated PDF is empty"
        assert pdf_path.read_bytes().startswith(b"%PDF"), "Generated file is not a valid PDF"
        print(generated)


if __name__ == "__main__":
    main()