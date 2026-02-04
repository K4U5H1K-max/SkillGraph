# personalizer/personalizer.py

import json
from prompt import SYSTEM_PROMPT
from schemas import PERSONALIZATION_SCHEMA

def call_llm(system_prompt: str, payload: dict) -> dict:
    """
    Replace this function with:
    - OpenAI
    - Azure OpenAI
    - Local LLM
    """

    # ⚠️ MOCK RESPONSE (for now)
    return {
        "hide": payload["known_skills"],
        "boost": payload["weak_skills"],
        "deprioritize": [],
        "timeline": {
            "week_1": payload["weak_skills"][:2]
        }
    }

def generate_overlay(user_profile: dict, semantic_roadmap: dict) -> dict:
    skill_ids = [s["id"] for s in semantic_roadmap["skills"]]

    payload = {
        "semantic_skills": skill_ids,
        "known_skills": user_profile.get("known_skills", []),
        "weak_skills": user_profile.get("weak_skills", []),
        "weekly_hours": user_profile.get("weekly_hours"),
        "target_months": user_profile.get("target_months")
    }

    overlay = call_llm(SYSTEM_PROMPT, payload)

    # Basic validation (minimal but effective)
    for key in overlay:
        if key not in PERSONALIZATION_SCHEMA["properties"]:
            raise ValueError(f"Invalid personalization key: {key}")

    return overlay
