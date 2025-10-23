"""
Тесты для вспомогательных функций.
"""

import os

from src.primitive_db.utils import (
    load_metadata,
    load_table_data,
    save_metadata,
    save_table_data,
)


class TestUtils:
    """Тесты для утилит работы с файлами."""
    
    def test_load_metadata_file_not_found(self, tmp_path):
        """Тест загрузки метаданных когда файл не существует."""
        non_existent_file = tmp_path / "nonexistent.json"
        result = load_metadata(str(non_existent_file))
        assert result == {}
    
    def test_save_and_load_metadata(self, tmp_path):
        """Тест сохранения и загрузки метаданных."""
        test_file = tmp_path / "test_meta.json"
        test_data = {"test_table": {"ID": "int", "name": "str"}}
        
        save_metadata(test_data, str(test_file))
        loaded_data = load_metadata(str(test_file))
        
        assert loaded_data == test_data
        assert os.path.exists(test_file)
    
    def test_load_metadata_invalid_json(self, tmp_path):
        """Тест загрузки некорректного JSON файла."""
        invalid_file = tmp_path / "invalid.json"
        with open(invalid_file, 'w') as f:
            f.write("invalid json content")
        
        result = load_metadata(str(invalid_file))
        assert result == {}
    
    def test_save_and_load_table_data(self, tmp_path):
        """Тест сохранения и загрузки данных таблицы."""
        test_data = [
            {"ID": 1, "name": "Test", "age": 25},
            {"ID": 2, "name": "Test2", "age": 30}
        ]
        
        save_table_data("test_table", test_data)
        loaded_data = load_table_data("test_table")
        
        assert loaded_data == test_data
    
    def test_load_table_data_not_found(self):
        """Тест загрузки данных несуществующей таблицы."""
        result = load_table_data("nonexistent_table")
        assert result == []
