# personalizer/loader.py

import json
from pathlib import Path

# Use absolute path from project root
PROJECT_ROOT = Path(__file__).parent.parent
SEMANTIC_DIR = PROJECT_ROOT / "conversion" / "output" / "semantic"

def load_semantic(role_key: str) -> dict:
    path = SEMANTIC_DIR / f"{role_key}.semantic.json"

    if not path.exists():
        raise FileNotFoundError(f"Semantic roadmap not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
