from service import personalize

user_profile = {
    "current_level": "intermediate",
    "known_skills": ["python_basics", "oop"],
    "weak_skills": ["system_design"],
    "weekly_hours": 6,
    "target_months": 5
}

if __name__ == "__main__":
    roadmap = personalize("software_architect", user_profile)

    print("\n=== PERSONALIZED ROADMAP ===")
    print("Role:", roadmap["role"])
    print("Total skills:", len(roadmap["skills"]))

    print("\nFirst 5 skills:\n")
    for skill in roadmap["skills"][:5]:
        print(skill)
