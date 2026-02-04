#!/usr/bin/env python3
"""
Main Orchestrator for Personalized Learning Roadmap CLI
Coordinates: role selection → roadmap display → conversation → personalization → roadmap update
"""

import os
import sys
import json
from pathlib import Path

# Add modules to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "llm"))
sys.path.insert(0, str(project_root / "personalizer"))
sys.path.insert(0, str(project_root / "roadmap_updater"))

from conversation_engine import GeminiConversationEngine
from role_guides import ROLE_GUIDES
from service import personalize
from updater import update_roadmap


# Mapping from role keys to preset roadmap files
PRESET_ROADMAPS = {
    "ai_data_scientist": "fake frontend/ai-ds",
    "full_stack": "fake frontend/fs",
    "machine_learning": "fake frontend/ml",
    "game_developer": "fake frontend/gd",
    "software_architect": "fake frontend/sa"
}


def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_banner():
    """Print welcome banner"""
    print("\n" + "="*70)
    print(" 🚀  PERSONALIZED LEARNING ROADMAP GENERATOR  🚀 ".center(70))
    print("="*70 + "\n")


def display_role_menu() -> str:
    """Display role selection menu and return selected role key"""
    print("\n📋 SELECT YOUR ROLE:\n")
    
    roles_list = list(ROLE_GUIDES.items())
    for idx, (key, name) in enumerate(roles_list, 1):
        print(f"  {idx}. {name}")
    
    print()
    
    while True:
        try:
            choice = input("Enter your choice (1-5): ").strip()
            choice_idx = int(choice) - 1
            
            if 0 <= choice_idx < len(roles_list):
                selected_key = roles_list[choice_idx][0]
                selected_name = roles_list[choice_idx][1]
                print(f"\n✅ You selected: {selected_name}\n")
                return selected_key
            else:
                print("❌ Invalid choice. Please enter a number between 1 and 5.")
        except (ValueError, KeyboardInterrupt):
            print("\n❌ Invalid input. Please enter a number.")


def load_preset_roadmap(role_key: str) -> str:
    """Load the preset roadmap text for a role"""
    roadmap_file = PRESET_ROADMAPS.get(role_key)
    if not roadmap_file:
        raise ValueError(f"No preset roadmap found for role: {role_key}")
    
    roadmap_path = Path(__file__).parent / roadmap_file
    
    with open(roadmap_path, "r", encoding="utf-8") as f:
        return f.read()


def display_roadmap(roadmap_text: str, title: str = "PRESET ROADMAP"):
    """Display a roadmap with formatting"""
    print("\n" + "="*70)
    print(f" 📚 {title} ".center(70))
    print("="*70 + "\n")
    print(roadmap_text)
    print("\n" + "="*70 + "\n")


def run_conversation(role_key: str) -> dict:
    """Run LLM conversation with user and return profile"""
    print("\n" + "="*70)
    print(" 💬 CONVERSATION - Tell us about yourself ".center(70))
    print("="*70 + "\n")
    
    print("Let's have a conversation to understand your background and goals.")
    print("Type 'done' when you're finished answering questions.\n")
    
    engine = GeminiConversationEngine(role_key)
    
    # Start conversation
    first_message = engine.step("")  # Engine asks first question
    print(f"🤖 Assistant: {first_message}\n")
    
    turn_count = 0
    max_turns = 10  # Limit conversation length
    
    while turn_count < max_turns:
        try:
            user_input = input("👤 You: ").strip()
            
            if user_input.lower() in ['done', 'exit', 'quit', 'finish']:
                print("\n✅ Conversation completed!\n")
                break
            
            if not user_input:
                continue
            
            response = engine.step(user_input)
            print(f"\n🤖 Assistant: {response}\n")
            
            turn_count += 1
            
        except KeyboardInterrupt:
            print("\n\n✅ Conversation interrupted. Moving to next step...\n")
            break
    
    if turn_count >= max_turns:
        print("\n✅ Conversation limit reached. Moving to next step...\n")
    
    return engine.get_profile()


def run_personalization(role_key: str, user_profile: dict) -> dict:
    """Run personalizer to update roadmap semantics"""
    print("\n" + "="*70)
    print(" ⚙️  PERSONALIZING ROADMAP ".center(70))
    print("="*70 + "\n")
    
    print("Analyzing your profile and adjusting roadmap priorities...\n")
    
    try:
        personalized_data = personalize(role_key, user_profile)
        print("✅ Personalization complete!\n")
        return personalized_data
    except Exception as e:
        print(f"⚠️  Warning: Personalization failed: {e}")
        print("Proceeding with default roadmap...\n")
        return {}


def generate_updated_roadmap(preset_roadmap: str, personalized_data: dict, user_profile: dict) -> str:
    """Generate updated roadmap using LLM"""
    print("\n" + "="*70)
    print(" 🎨 GENERATING YOUR PERSONALIZED ROADMAP ".center(70))
    print("="*70 + "\n")
    
    print("Creating a customized roadmap based on your profile...\n")
    
    try:
        updated_roadmap = update_roadmap(preset_roadmap, personalized_data, user_profile)
        print("✅ Roadmap generation complete!\n")
        return updated_roadmap
    except Exception as e:
        print(f"⚠️  Error generating updated roadmap: {e}")
        print("Showing preset roadmap instead...\n")
        return preset_roadmap


def save_results(role_key: str, user_profile: dict, personalized_data: dict, updated_roadmap: str):
    """Save results to output folder"""
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    
    # Save user profile
    profile_path = output_dir / f"{role_key}_profile.json"
    with open(profile_path, "w", encoding="utf-8") as f:
        json.dump(user_profile, f, indent=2)
    
    # Save personalized data
    personalized_path = output_dir / f"{role_key}_personalized.json"
    with open(personalized_path, "w", encoding="utf-8") as f:
        json.dump(personalized_data, f, indent=2)
    
    # Save updated roadmap
    roadmap_path = output_dir / f"{role_key}_roadmap.txt"
    with open(roadmap_path, "w", encoding="utf-8") as f:
        f.write(updated_roadmap)
    
    print(f"\n💾 Results saved to: {output_dir}/")
    print(f"   - {profile_path.name}")
    print(f"   - {personalized_path.name}")
    print(f"   - {roadmap_path.name}\n")


def main():
    """Main orchestration flow"""
    try:
        # Banner
        clear_screen()
        print_banner()
        
        # Step 1: Role Selection
        role_key = display_role_menu()
        
        # Step 2: Display Preset Roadmap
        preset_roadmap = load_preset_roadmap(role_key)
        input("\nPress Enter to view the preset roadmap...")
        clear_screen()
        display_roadmap(preset_roadmap, f"PRESET ROADMAP: {ROLE_GUIDES[role_key]}")
        
        input("\nPress Enter to start the conversation...")
        
        # Step 3: Conversation with LLM
        clear_screen()
        user_profile = run_conversation(role_key)
        
        # Step 4: Personalize Roadmap
        personalized_data = run_personalization(role_key, user_profile)
        
        # Step 5: Generate Updated Roadmap
        updated_roadmap = generate_updated_roadmap(preset_roadmap, personalized_data, user_profile)
        
        # Step 6: Display Updated Roadmap
        input("\nPress Enter to view your personalized roadmap...")
        clear_screen()
        display_roadmap(updated_roadmap, f"YOUR PERSONALIZED ROADMAP: {ROLE_GUIDES[role_key]}")
        
        # Step 7: Save Results
        save_results(role_key, user_profile, personalized_data, updated_roadmap)
        
        print("\n" + "="*70)
        print(" 🎉 ALL DONE! Happy Learning! 🎉 ".center(70))
        print("="*70 + "\n")
        
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
