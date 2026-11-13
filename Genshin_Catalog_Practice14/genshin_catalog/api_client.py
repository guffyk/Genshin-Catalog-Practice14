"""Інфраструктура мережевих запитів, відокремлена від бізнес-логіки."""
import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

class ApiError(Exception):
    pass

class GenshinApiClient:
    BASE_URL = "https://genshin.jmp.blue"

    def __init__(self, base_url: str = BASE_URL, timeout: int = 15):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def fetch_characters(self):
        request = Request(
            f"{self.base_url}/characters/all?lang=en",
            headers={"Accept": "application/json", "User-Agent": "GenshinCatalogPractice14/1.0"},
        )
        try:
            with urlopen(request, timeout=self.timeout) as response:
                return json.load(response)
        except HTTPError as error:
            raise ApiError(f"API повернув HTTP {error.code}") from error
        except (URLError, TimeoutError, OSError) as error:
            raise ApiError(f"Помилка з'єднання: {error}") from error
        except (json.JSONDecodeError, UnicodeDecodeError) as error:
            raise ApiError("API повернув неправильний JSON") from error
