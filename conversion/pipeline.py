# conversion/pipeline.py

import json
import os
from extractor import extract
from enrich import enrich
from normalize import normalize
from validate import validate
from roles import ROLES

# Since you run FROM conversion/
SEMANTIC_DIR = "output/semantic/"
MAP_DIR = "output/node_maps/"

# 🔑 Ensure directories exist
os.makedirs(SEMANTIC_DIR, exist_ok=True)
os.makedirs(MAP_DIR, exist_ok=True)

def run_all():
    for role_key, role in ROLES.items():
        print(f"🔄 Processing role: {role['name']}")

        extracted = extract(role["input"])
        enriched = enrich(extracted)

        semantic_roadmap, node_map = normalize(
            enriched,
            role["name"]
        )

        validate(semantic_roadmap)

        with open(f"{SEMANTIC_DIR}{role_key}.semantic.json", "w", encoding="utf-8") as f:
            json.dump(semantic_roadmap, f, indent=2)

        with open(f"{MAP_DIR}{role_key}.map.json", "w", encoding="utf-8") as f:
            json.dump(node_map, f, indent=2)

        print(f"✅ {role['name']} completed")

    print("🎉 All role roadmaps precomputed successfully")

if __name__ == "__main__":
    run_all()
