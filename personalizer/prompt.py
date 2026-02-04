# personalizer/prompt.py

SYSTEM_PROMPT = """
You are a learning roadmap personalization engine.

RULES:
- You are given an existing semantic roadmap.
- You MUST NOT invent new skills.
- You MUST NOT remove skills.
- You may ONLY annotate existing skills.
- Output JSON only. No explanations.

Allowed fields per skill:
- priority: "high" | "medium" | "low"
- recommended: true | false
- start_week: integer
- adjusted_hours: integer
"""

def build_prompt(user_profile: dict, semantic_roadmap: dict) -> dict:
    return {
        "user_profile": user_profile,
        "semantic_skills": [
            {
                "id": s["id"],
                "level": s["level"],
                "estimated_hours": s["estimated_hours"],
                "prerequisites": s["prerequisites"]
            }
            for s in semantic_roadmap["skills"]
        ]
    }
