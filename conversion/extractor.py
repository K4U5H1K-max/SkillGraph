# conversion/extractor.py

import json

IGNORED_NODE_TYPES = {"horizontal", "vertical"}

def extract(ui_json_path: str):
    with open(ui_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    nodes = data.get("nodes", [])
    edges = data.get("edges", [])

    skills = {}
    raw_edges = []

    for node in nodes:
        node_type = node.get("type")
        label = node.get("data", {}).get("label", "").strip()

        if not label or node_type in IGNORED_NODE_TYPES:
            continue

        skills[node["id"]] = {
            "ui_id": node["id"],
            "name": label
        }

    for edge in edges:
        src = edge.get("source")
        tgt = edge.get("target")

        if src in skills and tgt in skills:
            raw_edges.append((src, tgt))

    return {
        "skills": skills,
        "edges": raw_edges
    }
