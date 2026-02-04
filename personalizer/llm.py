# personalizer/llm.py

def call_llm(system_prompt: str, payload: dict) -> dict:
    """
    MOCK implementation.
    Replace with OpenAI / Azure later.
    """

    skills = payload["semantic_skills"]

    result = {"skills": {}}

    for i, skill in enumerate(skills):
        skill_id = skill["id"]

        result["skills"][skill_id] = {
            "priority": "high" if i < 5 else "medium",
            "recommended": True if i < 10 else False,
            "start_week": i // 2 + 1,
            "adjusted_hours": max(5, skill["estimated_hours"] - 10)
        }

    return result
