# personalizer/schemas.py

ALLOWED_FIELDS = {
    "priority",
    "recommended",
    "start_week",
    "adjusted_hours"
}

def validate_llm_output(output: dict):
    if "skills" not in output:
        raise ValueError("LLM output must contain 'skills'")

    for skill_id, updates in output["skills"].items():
        for key in updates:
            if key not in ALLOWED_FIELDS:
                raise ValueError(
                    f"Invalid field '{key}' for skill '{skill_id}'"
                )
