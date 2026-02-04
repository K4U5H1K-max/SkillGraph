# personalizer/schemas.py

PERSONALIZATION_SCHEMA = {
    "type": "object",
    "properties": {
        "hide": {
            "type": "array",
            "items": {"type": "string"}
        },
        "boost": {
            "type": "array",
            "items": {"type": "string"}
        },
        "deprioritize": {
            "type": "array",
            "items": {"type": "string"}
        },
        "timeline": {
            "type": "object",
            "additionalProperties": {
                "type": "array",
                "items": {"type": "string"}
            }
        }
    },
    "additionalProperties": False
}
