class UserProfile:
    def __init__(self, role: str):
        self.role = role
        self.skills = {}
        self.goals = {}
        self.time = {}
        self.preferences = {}
        self.raw_messages = []

    def update_from_llm(self, extracted: dict):
        self.skills.update(extracted.get("skills", {}))
        self.goals.update(extracted.get("goals", {}))
        self.time.update(extracted.get("time", {}))
        self.preferences.update(extracted.get("preferences", {}))

    def to_dict(self):
        return {
            "role": self.role,
            "skills": self.skills,
            "goals": self.goals,
            "time": self.time,
            "preferences": self.preferences
        }
