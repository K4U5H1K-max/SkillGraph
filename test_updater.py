#!/usr/bin/env python3
"""Test the roadmap updater"""

import sys
from pathlib import Path
import json

sys.path.insert(0, str(Path(__file__).parent / "roadmap_updater"))

from updater import update_roadmap

# Load test data
preset = "Test Roadmap\n├── Item 1\n└── Item 2"
personalized = json.load(open("output/ai_data_scientist_personalized.json"))
profile = json.load(open("output/ai_data_scientist_profile.json"))

print("Testing roadmap updater...")
result = update_roadmap(preset, personalized, profile)
print(f"✅ Success! Generated {len(result)} characters")
print("\nFirst 200 chars of result:")
print(result[:200])
