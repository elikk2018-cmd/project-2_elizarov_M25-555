"""
Конфигурация для pytest.
"""

import pytest
import os
import json
import shutil
from unittest.mock import patch
from src.primitive_db.core import create_table, drop_table, insert, select
from src.primitive_db.utils import load_metadata, save_metadata, load_table_data, save_table_data


@pytest.fixture
def temp_metadata_file(tmp_path):
    """Создает временный файл метаданных для тестов."""
    metadata_file = tmp_path / "test_meta.json"
    # Сохраняем пустые метаданные
    with open(metadata_file, 'w') as f:
        json.dump({}, f)
    return str(metadata_file)


@pytest.fixture
def temp_data_dir(tmp_path):
    """Создает временную директорию для данных."""
    data_dir = tmp_path / "test_data"
    data_dir.mkdir()
    return str(data_dir)


@pytest.fixture
def sample_metadata():
    """Возвращает sample метаданные для тестов."""
    return {
        "users": {
            "ID": "int",
            "name": "str", 
            "age": "int",
            "is_active": "bool"
        }
    }


@pytest.fixture
def sample_table_data():
    """Возвращает sample данные таблицы для тестов."""
    return [
        {"ID": 1, "name": "Иван", "age": 25, "is_active": True},
        {"ID": 2, "name": "Мария", "age": 30, "is_active": False}
    ]


@pytest.fixture(autouse=True)
def clean_test_environment():
    """
    Автоматически очищает тестовую среду перед каждым тестом.
    """
    # Очищаем данные перед тестом
    if os.path.exists("data"):
        shutil.rmtree("data")
    
    # Очищаем файл метаданных
    if os.path.exists("db_meta.json"):
        os.remove("db_meta.json")
    
    yield
    
    # Очищаем после теста (на всякий случай)
    if os.path.exists("data"):
        shutil.rmtree("data")
    
    if os.path.exists("db_meta.json"):
        os.remove("db_meta.json")
