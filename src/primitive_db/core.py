"""
Основной модуль бизнес-логики базы данных.
Содержит функции для работы с таблицами и данными.
"""

from .constants import (
    ERROR_MESSAGE_INVALID_COLUMN_FORMAT,
    ERROR_MESSAGE_INVALID_TYPE,
    ERROR_MESSAGE_TABLE_EXISTS,
    ERROR_MESSAGE_TABLE_NOT_EXISTS,
    SUCCESS_MESSAGE_TABLE_CREATED,
    SUCCESS_MESSAGE_TABLE_DROPPED,
    VALID_TYPES,
)
from .utils import save_metadata


def create_table(metadata, table_name, columns):
    """
    Создает новую таблицу в базе данных.
    """
    if table_name in metadata:
        print(ERROR_MESSAGE_TABLE_EXISTS.format(table_name))
        return metadata

    # Добавляем автоматический столбец ID
    columns_with_id = [('ID', 'int')]

    # Парсим и проверяем столбцы
    for column in columns:
        try:
            col_name, col_type = column.split(':')
            if col_type not in VALID_TYPES:
                print(ERROR_MESSAGE_INVALID_TYPE.format(col_type))
                return metadata
            columns_with_id.append((col_name, col_type))
        except ValueError:
            print(ERROR_MESSAGE_INVALID_COLUMN_FORMAT.format(column))
            return metadata

    # Создаем структуру таблицы
    table_structure = {col[0]: col[1] for col in columns_with_id}
    metadata[table_name] = table_structure

    # Формируем сообщение об успехе
    columns_str = ", ".join([f"{col[0]}:{col[1]}" for col in columns_with_id])
    print(SUCCESS_MESSAGE_TABLE_CREATED.format(table_name, columns_str))

    save_metadata(metadata)
    return metadata


def drop_table(metadata, table_name):
    """
    Удаляет таблицу из базы данных.
    """
    if table_name not in metadata:
        print(ERROR_MESSAGE_TABLE_NOT_EXISTS.format(table_name))
        return metadata

    del metadata[table_name]
    print(SUCCESS_MESSAGE_TABLE_DROPPED.format(table_name))

    save_metadata(metadata)
    return metadata


def list_tables(metadata):
    """
    Выводит список всех таблиц в базе данных.
    """
    if not metadata:
        print("Нет созданных таблиц.")
    else:
        for table_name in metadata:
            print(f"- {table_name}")
