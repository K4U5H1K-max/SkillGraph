# test_llm.py

from conversation_engine import GeminiConversationEngine
from role_guides import ROLE_GUIDES


def main():
    print("\n=== LLM SYSTEM TEST ===\n")

    # Pick a role to test
    role_key = "game_development"   # change if needed
    print(f"Testing role: {ROLE_GUIDES[role_key]}\n")

    engine = GeminiConversationEngine(role_key)

    print("🤖 Conversation started.")
    print("Type 'done' to end the test.\n")

    # Kickstart the conversation
    bot_message = engine.step("Hi")
    print(f"🤖 {bot_message}\n")

    while True:
        user_input = input("👤 ")
        if user_input.lower() in ["done", "exit", "stop"]:
            break

        bot_reply = engine.step(user_input)
        print(f"\n🤖 {bot_reply}\n")

    print("\n=== FINAL EXTRACTED PROFILE ===\n")
    profile = engine.get_profile()

    for key, value in profile.items():
        print(f"{key.upper()}: {value}")


if __name__ == "__main__":
    main()
