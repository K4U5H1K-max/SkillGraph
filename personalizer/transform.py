# personalizer/transform.py

from copy import deepcopy

def apply_personalization(semantic_roadmap: dict, llm_output: dict) -> dict:
    updated = deepcopy(semantic_roadmap)

    updates = llm_output.get("skills", {})

    for skill in updated["skills"]:
        skill_id = skill["id"]

        if skill_id in updates:
            skill.update(updates[skill_id])

    return updated
