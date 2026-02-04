# personalizer/loader.py

import json
import os

SEMANTIC_DIR = "../conversion/output/semantic"

def load_semantic(role_key: str) -> dict:
    path = os.path.join(SEMANTIC_DIR, f"{role_key}.semantic.json")

    if not os.path.exists(path):
        raise FileNotFoundError(f"Semantic roadmap not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
