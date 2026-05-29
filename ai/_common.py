from __future__ import annotations

import json
import os
import re
from functools import lru_cache
from typing import Any

from groq import Groq


GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")


@lru_cache(maxsize=1)
def get_groq_client() -> Groq | None:
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        return None
    return Groq(api_key=api_key)


def extract_json_block(text: str) -> Any:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        match = re.search(r"\[.*\]", cleaned, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        raise


def call_groq_json(system_prompt: str, user_prompt: str) -> Any:
    client = get_groq_client()
    if client is None:
        raise RuntimeError("GROQ_API_KEY is not configured")

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        temperature=0.2,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    content = response.choices[0].message.content or "{}"
    return extract_json_block(content)


def safe_lower_set(items: list[str] | None) -> set[str]:
    return {item.strip().lower() for item in (items or []) if item and item.strip()}


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()
