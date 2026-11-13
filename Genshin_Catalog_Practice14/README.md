# Каталог персонажів — практичне заняття №14

Python 3.10+. Реалізація бізнес-логіки для теми **«Каталог персонажів»** за даними [Genshin API](https://genshin.jmp.blue/). Графічний інтерфейс можна додати пізніше: готові словники ViewModel вже повертає метод `get_view_models()`.

## Запуск

Відкрийте термінал у папці проєкту та виконайте:

```bash
python main.py list --demo
python main.py search amber --demo
python main.py info albedo --demo
python main.py stats --demo
```

Прапорець `--demo` використовує локальні тестові дані і **не потребує інтернету**. Без нього використовується реальний API:

```bash
python main.py list
python main.py search amber
python main.py info albedo
python main.py list --element Pyro --min-rarity 5 --sort rarity
```

Залежностей, які потрібно встановлювати через `pip`, немає — використовуються стандартні бібліотеки Python.

## Тести

```bash
python -m unittest discover -s tests -v
```

## Структура

| Файл | Призначення |
| --- | --- |
| `genshin_catalog/models.py` | Клас `Character` і перетворення на ViewModel |
| `genshin_catalog/parser.py` | Парсер зовнішнього JSON |
| `genshin_catalog/service.py` | Бізнес-логіка: пошук, фільтри, сортування та статистика |
| `genshin_catalog/api_client.py` | Інфраструктура: запит до API |
| `genshin_catalog/demo_source.py` | Заглушка для перевірки без мережі |
| `main.py` | Демонстрація в консольному інтерфейсі |
| `examples/characters.json` | Приклад тестових даних |
| `tests/` | Автоматичні тести |
| `DESIGN.md` | Дизайн-документ із розділом «Бізнес-логіка» |

## Як здати

1. Створіть **власний** репозиторій GitHub і завантажте в нього файли з цього архіву.
2. Передайте викладачеві посилання на репозиторій.
3. Окреме посилання на дизайн-документ — це URL на `DESIGN.md` у вашому репозиторії.

Важливо: https://github.com/genshindev/api — це джерело **чужого API**, а не ваш репозиторій з виконаною роботою.

Проєкт має демонстраційний CLI, але повноцінний GUI не входить до цієї практичної. Зовнішня доступність API залежить від його сервера.
