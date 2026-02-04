# conversion/normalize.py

import re

def _make_id(name: str):
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")

def normalize(enriched, role_name):
    semantic_skills = {}
    ui_to_semantic = {}

    for ui_id, skill in enriched["skills"].items():
        semantic_id = _make_id(skill["name"])

        semantic_skills[semantic_id] = {
            "id": semantic_id,
            "name": skill["name"],
            "level": skill["level"],
            "category": skill["category"],
            "estimated_hours": skill["estimated_hours"],
            "prerequisites": []
        }

        ui_to_semantic[ui_id] = semantic_id

    for src, tgt in enriched["edges"]:
        src_id = ui_to_semantic[src]
        tgt_id = ui_to_semantic[tgt]
        semantic_skills[tgt_id]["prerequisites"].append(src_id)

    return {
        "role": role_name,
        "skills": list(semantic_skills.values())
    }, ui_to_semantic
