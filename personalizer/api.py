# personalizer/api.py

from loader import load_semantic
from personalizer import generate_overlay

def personalize(role_key: str, user_profile: dict) -> dict:
    semantic_roadmap = load_semantic(role_key)

    overlay = generate_overlay(
        user_profile=user_profile,
        semantic_roadmap=semantic_roadmap
    )

    return {
        "role": role_key,
        "overlay": overlay
    }
