"""
Тесты для основной бизнес-логики.
"""

import pytest
from unittest.mock import patch
from src.primitive_db.core import (
    create_table, drop_table, list_tables, 
    insert, select, update, delete, info
)
from src.primitive_db.utils import load_metadata, save_metadata, load_table_data, save_table_data


class TestCore:
    """Тесты для основной бизнес-логики."""
    
    def test_create_table_success(self, tmp_path):
        """Тест успешного создания таблицы."""
        metadata_file = tmp_path / "test_meta.json"
        save_metadata({}, str(metadata_file))
        
        metadata = load_metadata(str(metadata_file))
        result = create_table(metadata, "users", ["name:str", "age:int"])
        
        assert "users" in result
        assert result["users"]["ID"] == "int"
        assert result["users"]["name"] == "str"
        assert result["users"]["age"] == "int"
    
    def test_create_table_already_exists(self, tmp_path, capsys):
        """Тест создания таблицы которая уже существует."""
        metadata_file = tmp_path / "test_meta.json"
        initial_metadata = {"users": {"ID": "int", "name": "str"}}
        save_metadata(initial_metadata, str(metadata_file))
        
        metadata = load_metadata(str(metadata_file))
        result = create_table(metadata, "users", ["age:int"])
        
        # Проверяем что метаданные не изменились
        assert result == initial_metadata
        # Проверяем сообщение об ошибке
        captured = capsys.readouterr()
        assert "уже существует" in captured.out
    
    def test_create_table_invalid_type(self, tmp_path, capsys):
        """Тест создания таблицы с невалидным типом данных."""
        metadata_file = tmp_path / "test_meta.json"
        save_metadata({}, str(metadata_file))
        
        metadata = load_metadata(str(metadata_file))
        result = create_table(metadata, "users", ["name:invalid_type"])
        
        assert "users" not in result
        captured = capsys.readouterr()
        assert "Неподдерживаемый тип данных" in captured.out
    
    @patch('builtins.input', return_value='y')
    def test_drop_table_success(self, mock_input, tmp_path):
        """Тест успешного удаления таблицы."""
        metadata_file = tmp_path / "test_meta.json"
        initial_metadata = {"users": {"ID": "int", "name": "str"}}
        save_metadata(initial_metadata, str(metadata_file))
        
        metadata = load_metadata(str(metadata_file))
        result = drop_table(metadata, "users")
        
        assert "users" not in result
    
    @patch('builtins.input', return_value='y')
    def test_drop_table_not_exists(self, mock_input, tmp_path, capsys):
        """Тест удаления несуществующей таблицы."""
        metadata_file = tmp_path / "test_meta.json"
        save_metadata({}, str(metadata_file))
        
        metadata = load_metadata(str(metadata_file))
        result = drop_table(metadata, "nonexistent")
        
        assert result == {}
        captured = capsys.readouterr()
        assert "не существует" in captured.out
    
    def test_list_tables_empty(self, capsys):
        """Тест списка таблиц когда нет таблиц."""
        list_tables({})
        captured = capsys.readouterr()
        assert "Нет созданных таблиц" in captured.out
    
    def test_list_tables_with_data(self, capsys):
        """Тест списка таблиц когда есть таблицы."""
        metadata = {"users": {}, "products": {}}
        list_tables(metadata)
        captured = capsys.readouterr()
        assert "users" in captured.out
        assert "products" in captured.out
    
    def test_insert_success(self, capsys):
        """Тест успешной вставки данных."""
        # Создаем таблицу
        metadata = {"users": {"ID": "int", "name": "str", "age": "int"}}
        
        # Вставляем данные
        insert(metadata, "users", '("Иван", 25)')
        
        # Проверяем что данные сохранились
        table_data = load_table_data("users")
        assert len(table_data) == 1
        assert table_data[0]["name"] == "Иван"
        assert table_data[0]["age"] == 25
        assert table_data[0]["ID"] == 1
        
        captured = capsys.readouterr()
        assert "успешно добавлена" in captured.out
    
    def test_insert_table_not_exists(self, capsys):
        """Тест вставки в несуществующую таблицу."""
        insert({}, "nonexistent", '("test", 25)')
        captured = capsys.readouterr()
        assert "не существует" in captured.out
    
    def test_info_table(self, capsys):
        """Тест информации о таблице."""
        metadata = {"users": {"ID": "int", "name": "str"}}
        
        # Сохраняем тестовые данные
        test_data = [{"ID": 1, "name": "Тест"}]
        save_table_data("users", test_data)
        
        info(metadata, "users")
        captured = capsys.readouterr()
        assert "Таблица: users" in captured.out
        assert "Количество записей: 1" in captured.out
    
    @patch('builtins.input', return_value='y')
    def test_delete_success(self, mock_input, capsys):
        """Тест успешного удаления данных."""
        # Создаем таблицу и данные
        metadata = {"users": {"ID": "int", "name": "str", "age": "int"}}
        test_data = [
            {"ID": 1, "name": "Иван", "age": 25},
            {"ID": 2, "name": "Мария", "age": 30}
        ]
        save_table_data("users", test_data)
        
        # Удаляем запись
        delete(metadata, "users", ("name", "Иван"))
        
        # Проверяем что запись удалилась
        table_data = load_table_data("users")
        assert len(table_data) == 1
        assert table_data[0]["name"] == "Мария"
        
        captured = capsys.readouterr()
        # Исправляем проверку текста сообщения
        assert "Удалено 1 записей" in captured.out
