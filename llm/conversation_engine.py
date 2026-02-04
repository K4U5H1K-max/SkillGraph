import json
from gemini_client import call_gemini
from system_prompt import SYSTEM_PROMPT
from role_guides import ROLE_GUIDES
from user_profile import UserProfile


class GeminiConversationEngine:
    def __init__(self, role_key: str):
        self.role_key = role_key
        self.profile = UserProfile(role_key)

        self.messages = [
            SYSTEM_PROMPT,
            f"The user has selected the role: {ROLE_GUIDES[role_key]}.",
            "Start by asking about their current skills, experience, and familiarity with this role."
        ]

    def step(self, user_input: str) -> str:
        """
        Takes user input, updates profile, returns next LLM message
        """
        self.profile.raw_messages.append(user_input)
        self.messages.append(f"User: {user_input}")

        # Ask Gemini for extraction
        extraction_prompt = (
            "Extract structured data from the user's last message. "
            "Return JSON only."
        )
        extraction = call_gemini(self.messages + [extraction_prompt])

        try:
            extracted_data = json.loads(extraction)
            self.profile.update_from_llm(extracted_data)
        except json.JSONDecodeError:
            pass  # fail silently, conversation continues

        self.messages.append(f"Assistant extracted: {extraction}")

        # Ask Gemini what to say next
        next_message = call_gemini(self.messages)
        self.messages.append(f"Assistant: {next_message}")

        return next_message

    def get_profile(self):
        return self.profile.to_dict()
