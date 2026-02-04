# conversion/enrich.py

def enrich(extracted):
    enriched = {}

    for ui_id, skill in extracted["skills"].items():
        name = skill["name"].lower()

        if "advanced" in name:
            level = "advanced"
            hours = 40
        elif "basic" in name or "fundamental" in name:
            level = "beginner"
            hours = 20
        else:
            level = "intermediate"
            hours = 30

        if any(k in name for k in ["python", "java", "c++"]):
            category = "programming"
        elif any(k in name for k in ["model", "llm", "learning"]):
            category = "machine-learning"
        else:
            category = "general"

        enriched[ui_id] = {
            **skill,
            "level": level,
            "estimated_hours": hours,
            "category": category
        }

    return {
        "skills": enriched,
        "edges": extracted["edges"]
    }
