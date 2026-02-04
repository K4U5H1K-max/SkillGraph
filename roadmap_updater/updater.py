# roadmap_updater/updater.py

from gemini_client import call_gemini


SYSTEM_PROMPT = """You are an expert learning path designer. Your task is to update a preset roadmap 
based on the user's personalized preferences and learning profile.

You will receive:
1. A preset roadmap in text format (tree structure)
2. User preferences and personalized data

Generate an UPDATED roadmap in the EXACT SAME FORMAT as the preset roadmap. You have full autonomy 
to make SIGNIFICANT CHANGES if you believe they are necessary for the user's learning journey:
- Reorder sections/topics extensively based on user priorities and learning progression
- Add emphasis, notes, or explanations where user has high interest
- Skip, minimize, or remove topics where user already has expertise
- Add new topics or subtopics if they fill critical gaps for the user's goals
- Adjust depth/breadth based on user goals and experience level
- Restructure the roadmap hierarchy if a different organization better serves the user
- Keep the same tree structure and formatting style, but feel free to modify content significantly

Make bold, thoughtful changes when they will genuinely improve the learning experience for this specific user.

Return ONLY the updated roadmap text, nothing else.
"""


def update_roadmap(preset_roadmap: str, personalized_data: dict, user_profile: dict) -> str:
    """
    Takes preset roadmap text and personalized data, returns updated roadmap text.
    
    Args:
        preset_roadmap: The original roadmap text (from fake frontend)
        personalized_data: Output from personalizer (semantic with priorities, hours, etc.)
        user_profile: User's profile from conversation (skills, goals, experience)
    
    Returns:
        Updated roadmap in same text format
    """
    
    # Build the prompt for Gemini
    prompt_parts = [
        SYSTEM_PROMPT,
        "\n--- PRESET ROADMAP ---\n",
        preset_roadmap,
        "\n\n--- USER PROFILE ---\n",
        f"Skills: {user_profile.get('skills', [])}",
        f"Experience Level: {user_profile.get('experience_level', 'beginner')}",
        f"Goals: {user_profile.get('goals', [])}",
        f"Available Time: {user_profile.get('available_hours_per_week', 'not specified')} hours/week",
        f"Preferences: {user_profile.get('preferences', {})}",
        "\n\n--- PERSONALIZED PRIORITIES ---\n",
        _format_personalized_data(personalized_data),
        "\n\n--- TASK ---\n",
        "Generate the UPDATED ROADMAP in the exact same tree format as the preset roadmap above.",
        "Adjust based on user profile and priorities. Return ONLY the roadmap text."
    ]
    
    # Call Gemini
    response = call_gemini(prompt_parts)
    
    return response


def _format_personalized_data(personalized_data: dict) -> str:
    """Format personalized data for the prompt"""
    lines = []
    
    skills = personalized_data.get("skills", [])
    for skill in skills:
        skill_name = skill.get("name", skill.get("id", "Unknown"))
        priority = skill.get("priority", "medium")
        recommended = skill.get("recommended", True)
        hours = skill.get("adjusted_hours", skill.get("estimated_hours", 0))
        
        lines.append(
            f"- {skill_name}: Priority={priority}, "
            f"Recommended={recommended}, Hours={hours}"
        )
    
    return "\n".join(lines) if lines else "No specific priorities set."
