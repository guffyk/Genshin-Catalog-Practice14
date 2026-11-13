"""Простий CLI, який використовує готову бізнес-логіку."""
import argparse
import json
from pathlib import Path
from genshin_catalog import CharacterCatalog, GenshinApiClient, ApiError
from genshin_catalog.demo_source import DemoSource

def main():
    parser = argparse.ArgumentParser(description="Каталог персонажів Genshin Impact")
    parser.add_argument("command", choices=["list", "search", "info", "stats"])
    parser.add_argument("text", nargs="?", default="")
    parser.add_argument("--element", default="")
    parser.add_argument("--weapon", default="")
    parser.add_argument("--min-rarity", type=int, default=0)
    parser.add_argument("--sort", choices=["name", "rarity"], default="name")
    parser.add_argument("--demo", action="store_true", help="Використати тестові дані")
    args = parser.parse_args()

    path = Path(__file__).resolve().parent / "examples" / "characters.json"
    source = DemoSource(path) if args.demo else GenshinApiClient()
    catalog = CharacterCatalog(source)
    try:
        catalog.refresh()
        if args.command == "list":
            output = catalog.get_view_models(element=args.element, weapon=args.weapon,
                min_rarity=args.min_rarity, sort_by=args.sort)
        elif args.command == "search":
            output = catalog.get_view_models(query=args.text, element=args.element,
                weapon=args.weapon, min_rarity=args.min_rarity, sort_by=args.sort)
        elif args.command == "info":
            character = catalog.get(args.text)
            if character is None:
                matches = catalog.search(query=args.text)
                character = matches[0] if len(matches) == 1 else None
            output = character.to_view_model() if character else {"error": "Персонажа не знайдено"}
        else:
            output = catalog.get_statistics()
        print(json.dumps(output, ensure_ascii=False, indent=2))
    except (ApiError, ValueError, OSError) as error:
        parser.exit(1, f"Помилка: {error}\n")

if __name__ == "__main__":
    main()
