import unittest
from genshin_catalog.parser import parse_character, parse_characters
from genshin_catalog.service import CharacterCatalog

SAMPLE = {
    "amber": {"name": "Amber", "vision": "Pyro", "weapon": "Bow", "nation": "Mondstadt", "rarity": 4},
    "albedo": {"name": "Albedo", "vision": "Geo", "weapon": "Sword", "nation": "Mondstadt", "rarity": 5},
    "lisa": {"name": "Lisa", "vision": "Electro", "weapon": "Catalyst", "nation": "Mondstadt", "rarity": 4},
}

class FakeSource:
    def __init__(self, data):
        self.data = data
    def fetch_characters(self):
        return self.data

class TestCatalog(unittest.TestCase):
    def setUp(self):
        self.catalog = CharacterCatalog(FakeSource(SAMPLE))
        self.catalog.refresh()

    def test_parse_dictionary(self):
        self.assertEqual(len(parse_characters(SAMPLE)), 3)

    def test_parse_single_character(self):
        character = parse_character("amber", SAMPLE["amber"])
        self.assertEqual((character.element, character.rarity), ("Pyro", 4))

    def test_missing_optional_fields(self):
        character = parse_character("amber", {"name": "Amber"})
        self.assertEqual(character.region, "Невідомо")
        self.assertEqual(character.rarity, 0)

    def test_malformed_records_are_skipped(self):
        data = {"broken": {"rarity": 4}, "none": None, "amber": SAMPLE["amber"]}
        self.assertEqual(len(parse_characters(data)), 1)

    def test_parse_list(self):
        self.assertEqual(parse_characters([{"id": "amber", "name": "Amber"}])[0].id, "amber")

    def test_invalid_root(self):
        with self.assertRaises(ValueError):
            parse_characters("wrong")

    def test_search_is_case_insensitive(self):
        self.assertEqual(self.catalog.search(query="ALB")[0].id, "albedo")

    def test_filter_by_element(self):
        self.assertEqual([c.id for c in self.catalog.search(element="PYRO")], ["amber"])

    def test_filter_with_rarity(self):
        self.assertEqual(self.catalog.search(weapon="Bow", min_rarity=5), [])

    def test_sort_by_rarity(self):
        self.assertEqual([c.id for c in self.catalog.search(sort_by="rarity")],
                         ["albedo", "amber", "lisa"])

    def test_view_model(self):
        model = self.catalog.get_view_models(query="amber")[0]
        self.assertEqual(model["stars"], "★★★★")
        self.assertIn("/characters/amber/card", model["image_url"])

    def test_statistics(self):
        stats = self.catalog.get_statistics()
        self.assertEqual(stats["total"], 3)
        self.assertEqual(stats["by_rarity"], {4: 2, 5: 1})

    def test_invalid_sort_is_error(self):
        with self.assertRaises(ValueError):
            self.catalog.search(sort_by="hp")

    def test_invalid_rarity_is_error(self):
        with self.assertRaises(ValueError):
            self.catalog.search(min_rarity=6)

    def test_unknown_character(self):
        self.assertIsNone(self.catalog.get("unknown"))

    def test_failed_refresh_preserves_old_data(self):
        self.catalog.source = FakeSource("not-json-object")
        with self.assertRaises(ValueError):
            self.catalog.refresh()
        self.assertEqual(len(self.catalog.characters), 3)

if __name__ == "__main__":
    unittest.main()
