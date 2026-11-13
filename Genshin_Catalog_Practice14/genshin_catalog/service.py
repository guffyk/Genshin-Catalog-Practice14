"""Бізнес-логіка каталогу: пошук, фільтрація, сортування та статистика."""
from collections import Counter
from .parser import parse_characters

class CharacterCatalog:
    def __init__(self, source):
        # source може бути API-клієнтом або тестовою заглушкою.
        self.source = source
        self.characters = []

    def refresh(self):
        # Старі дані залишаються, якщо API або парсер завершиться помилкою.
        new_characters = parse_characters(self.source.fetch_characters())
        self.characters = new_characters
        return len(self.characters)

    def get(self, character_id):
        wanted = character_id.strip().casefold()
        for character in self.characters:
            if character.id == wanted:
                return character
        return None

    def search(self, query="", element="", weapon="", min_rarity=0, sort_by="name"):
        if not isinstance(min_rarity, int) or not 0 <= min_rarity <= 5:
            raise ValueError("min_rarity: число від 0 до 5")
        if sort_by not in ("name", "rarity"):
            raise ValueError("sort_by: name або rarity")
        q, e, w = query.strip().casefold(), element.strip().casefold(), weapon.strip().casefold()
        result = []
        for c in self.characters:
            if q and q not in c.name.casefold() and q not in c.id.casefold():
                continue
            if e and c.element.casefold() != e:
                continue
            if w and c.weapon.casefold() != w:
                continue
            if c.rarity < min_rarity:
                continue
            result.append(c)
        if sort_by == "rarity":
            return sorted(result, key=lambda c: (-c.rarity, c.name.casefold()))
        return sorted(result, key=lambda c: c.name.casefold())

    def get_view_models(self, **filters):
        return [c.to_view_model() for c in self.search(**filters)]

    def get_statistics(self):
        return {
            "total": len(self.characters),
            "by_element": dict(sorted(Counter(c.element for c in self.characters).items())),
            "by_rarity": dict(sorted(Counter(c.rarity for c in self.characters).items())),
        }
