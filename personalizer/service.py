# personalizer/service.py

from loader import load_semantic
from prompt import SYSTEM_PROMPT, build_prompt
from llm import call_llm
from transform import apply_personalization
from schemas import validate_llm_output

def personalize(role_key: str, user_profile: dict) -> dict:
    # 1. Load semantic roadmap
    semantic = load_semantic(role_key)

    # 2. Build LLM input
    payload = build_prompt(user_profile, semantic)

    # 3. Call LLM
    llm_output = call_llm(SYSTEM_PROMPT, payload)

    # 4. Validate output
    validate_llm_output(llm_output)

    # 5. Apply personalization
    personalized = apply_personalization(semantic, llm_output)

    return personalized
