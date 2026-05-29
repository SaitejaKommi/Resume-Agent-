from __future__ import annotations

import re

from ai.skill_extractor import extract_skills


def analyze_resume(raw_text: str) -> dict:
    words = re.findall(r"\w+", raw_text)
    return {
        "word_count": len(words),
        "line_count": len(raw_text.splitlines()),
        "bullet_count": len(re.findall(r"^[\-•*]", raw_text, re.MULTILINE)),
        "detected_skills": extract_skills(raw_text),
        "section_signals": {
            "experience": bool(re.search(r"experience|employment|work history", raw_text, re.IGNORECASE)),
            "education": bool(re.search(r"education|university|college|degree", raw_text, re.IGNORECASE)),
            "skills": bool(re.search(r"skills|technologies|stack", raw_text, re.IGNORECASE)),
            "projects": bool(re.search(r"projects|portfolio|case study", raw_text, re.IGNORECASE)),
        },
    }
