"""Сохранение и загрузка данных проекта в формате JSON."""

import json
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"


def load_json(filename: str, default: list | dict) -> list | dict:
    """Загрузить данные из JSON-файла в каталоге data/.

    Если файл не найден, возвращается default. Если файл повреждён
    (некорректный JSON), выводится предупреждение и также возвращается
    default — программа не завершается аварийно.
    """
    path = DATA_DIR / filename
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return default
    except json.JSONDecodeError:
        print(f"Файл {filename} повреждён, используются пустые данные.")
        return default


def save_json(filename: str, data: list | dict) -> None:
    """Сохранить данные в JSON-файл в каталоге data/."""
    DATA_DIR.mkdir(exist_ok=True)
    path = DATA_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
