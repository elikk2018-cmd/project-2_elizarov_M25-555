"""
Вспомогательные функции для работы с файловой системой.
Обеспечивают сохранение и загрузку данных в формате JSON.
"""

import json
import os

from .constants import DATA_DIR, META_FILE


def load_metadata(filepath=META_FILE):
    """
    Загружает метаданные базы данных из JSON файла.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError as e:
        print(f"Ошибка чтения файла метаданных: {e}")
        return {}


def save_metadata(data, filepath=META_FILE):
    """
    Сохраняет метаданные базы данных в JSON файл.
    """
    try:
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Ошибка сохранения метаданных: {e}")


def ensure_data_dir():
    """
    Создает директорию для данных, если она не существует.
    """
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def load_table_data(table_name):
    """
    Загружает данные таблицы из JSON файла.
    """
    ensure_data_dir()
    filepath = f"{DATA_DIR}/{table_name}.json"
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as e:
        print(f"Ошибка чтения данных таблицы {table_name}: {e}")
        return []


def save_table_data(table_name, data):
    """
    Сохраняет данные таблицы в JSON файл.
    """
    ensure_data_dir()
    filepath = f"{DATA_DIR}/{table_name}.json"
    try:
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Ошибка сохранения данных таблицы {table_name}: {e}")
