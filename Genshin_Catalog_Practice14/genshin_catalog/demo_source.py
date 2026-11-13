"""Заглушка замість API для перевірки програми без інтернету."""
import json
from pathlib import Path

class DemoSource:
    def __init__(self, path):
        self.path = Path(path)

    def fetch_characters(self):
        with self.path.open(encoding="utf-8") as file:
            return json.load(file)
