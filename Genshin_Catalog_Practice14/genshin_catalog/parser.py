"""Перетворення зовнішнього JSON на нормалізовані моделі Character."""
import re
from .models import Character

BASE_URL = "https://genshin.jmp.blue"

def text_value(value, default="Невідомо"):
    return value.strip() if isinstance(value, str) and value.strip() else default

def rarity_value(value):
    try:
        rarity = int(value)
        return rarity if 1 <= rarity <= 5 else 0
    except (ValueError, TypeError, OverflowError):
        return 0

def parse_character(character_id, data):
    if not isinstance(character_id, str) or not isinstance(data, dict):
        return None
    character_id = character_id.strip().lower()
    if not re.fullmatch(r"[a-z0-9-]+", character_id):
        return None
    name = text_value(data.get("name"), "")
    if not name:
        return None
    return Character(
        id=character_id,
        name=name,
        title=text_value(data.get("title"), ""),
        element=text_value(data.get("vision")),
        weapon=text_value(data.get("weapon")),
        region=text_value(data.get("nation")),
        rarity=rarity_value(data.get("rarity")),
        description=text_value(data.get("description"), ""),
        image_url=f"{BASE_URL}/characters/{character_id}/card",
    )

def parse_characters(payload):
    """API /characters/all повертає {id: {...}}; тестово підтримує і список."""
    if isinstance(payload, dict):
        entries = payload.items()
    elif isinstance(payload, list):
        entries = ((item.get("id", ""), item) for item in payload if isinstance(item, dict))
    else:
        raise ValueError("Формат даних має бути словником або списком JSON-об'єктів")
    result = []
    seen = set()
    for character_id, data in entries:
        character = parse_character(character_id, data)
        if character is not None and character.id not in seen:
            result.append(character)
            seen.add(character.id)
    return result
