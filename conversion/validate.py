# conversion/validate.py

def validate(semantic_roadmap):
    skill_ids = {s["id"] for s in semantic_roadmap["skills"]}

    for skill in semantic_roadmap["skills"]:
        for prereq in skill["prerequisites"]:
            if prereq not in skill_ids:
                raise ValueError(
                    f"Invalid prerequisite '{prereq}' in skill '{skill['id']}'"
                )

    return True
