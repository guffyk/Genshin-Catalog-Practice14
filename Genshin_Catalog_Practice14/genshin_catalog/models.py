from dataclasses import dataclass

@dataclass(frozen=True)
class Character:
    """Внутрішня модель персонажа."""
    id: str
    name: str
    title: str
    element: str
    weapon: str
    region: str
    rarity: int
    description: str
    image_url: str

    def to_view_model(self) -> dict:
        """Готові дані для відображення в майбутньому GUI."""
        return {
            "id": self.id,
            "name": self.name,
            "title": self.title,
            "element": self.element,
            "weapon": self.weapon,
            "region": self.region,
            "rarity": self.rarity,
            "stars": "★" * self.rarity,
            "description": self.description,
            "image_url": self.image_url,
        }
