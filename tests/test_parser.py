"""
Тесты для парсера команд.
"""

import pytest

from src.primitive_db.parser import parse_set, parse_values, parse_where


class TestParser:
    """Тесты для парсера команд."""
    
    def test_parse_values_simple(self):
        """Тест парсинга простых значений."""
        result = parse_values('("value1", "value2", "value3")')
        assert result == ['"value1"', '"value2"', '"value3"']
    
    def test_parse_values_without_parentheses(self):
        """Тест парсинга значений без скобок."""
        result = parse_values('"value1", "value2"')
        assert result == ['"value1"', '"value2"']
    
    def test_parse_values_with_commas_in_quotes(self):
        """Тест парсинга значений с запятыми в кавычках."""
        result = parse_values('("value,with,commas", "simple")')
        assert result == ['"value,with,commas"', '"simple"']
    
    def test_parse_where_success(self):
        """Тест успешного парсинга WHERE условия."""
        column, value = parse_where(["age", "=", "25"])
        assert column == "age"
        assert value == "25"
    
    def test_parse_where_with_quotes(self):
        """Тест парсинга WHERE условия с кавычками."""
        column, value = parse_where(["name", "=", '"Иван"'])
        assert column == "name"
        assert value == "Иван"
    
    def test_parse_where_invalid_format(self):
        """Тест парсинга некорректного WHERE условия."""
        with pytest.raises(ValueError, match="Некорректный формат условия WHERE"):
            parse_where(["age", "25"])  # Не хватает оператора
    
    def test_parse_set_success(self):
        """Тест успешного парсинга SET условия."""
        column, value = parse_set(["age", "=", "26"])
        assert column == "age"
        assert value == "26"
    
    def test_parse_set_with_quotes(self):
        """Тест парсинга SET условия с кавычками."""
        column, value = parse_set(["name", "=", '"Новое имя"'])
        assert column == "name"
        assert value == "Новое имя"
    
    def test_parse_set_invalid_format(self):
        """Тест парсинга некорректного SET условия."""
        with pytest.raises(ValueError, match="Некорректный формат условия SET"):
            parse_set(["age", "26"])  # Не хватает оператора
