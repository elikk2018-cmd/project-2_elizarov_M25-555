"""
Основной модуль бизнес-логики базы данных.
"""

from .constants import (
    CACHE_ENABLED,
    ERROR_MESSAGE_INVALID_COLUMN_FORMAT,
    ERROR_MESSAGE_INVALID_TYPE,
    ERROR_MESSAGE_TABLE_EXISTS,
    ERROR_MESSAGE_TABLE_NOT_EXISTS,
    SUCCESS_MESSAGE_TABLE_CREATED,
    SUCCESS_MESSAGE_TABLE_DROPPED,
    VALID_TYPES,
)
from .decorators import cacher, confirm_action, handle_db_errors, log_time
from .parser import parse_values
from .utils import load_table_data, save_metadata, save_table_data


@handle_db_errors
def create_table(metadata, table_name, columns):
    """
    Создает новую таблицу в базе данных.
    """
    if table_name in metadata:
        print(ERROR_MESSAGE_TABLE_EXISTS.format(table_name))
        return metadata

    columns_with_id = [('ID', 'int')]

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

    table_structure = {col[0]: col[1] for col in columns_with_id}
    metadata[table_name] = table_structure

    columns_str = ", ".join([f"{col[0]}:{col[1]}" for col in columns_with_id])
    print(SUCCESS_MESSAGE_TABLE_CREATED.format(table_name, columns_str))

    save_metadata(metadata)
    return metadata


@handle_db_errors
@confirm_action("удаление таблицы")
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


@handle_db_errors
def list_tables(metadata):
    """
    Выводит список всех таблиц в базе данных.
    """
    if not metadata:
        print("📭 Нет созданных таблиц.")
    else:
        print("📋 Список таблиц:")
        for table_name in metadata:
            print(f"  - {table_name}")


@handle_db_errors
@log_time
def insert(metadata, table_name, values_str):
    """
    Вставляет данные в таблицу.
    """
    if table_name not in metadata:
        print(f'❌ Ошибка: Таблица "{table_name}" не существует.')
        return

    # Парсим значения
    try:
        values = parse_values(values_str)
    except Exception as e:
        print(f'❌ Ошибка парсинга значений: {e}')
        return

    table_structure = metadata[table_name]
    data_columns = [col for col in table_structure.keys() if col != 'ID']

    # Проверяем количество значений
    if len(values) != len(data_columns):
        print(f'❌ Ошибка: Ожидалось {len(data_columns)} значений, получено {len(values)}.')
        return

    # Загружаем существующие данные
    table_data = load_table_data(table_name)

    # Генерируем новый ID
    if table_data:
        new_id = max(item['ID'] for item in table_data) + 1
    else:
        new_id = 1

    # Создаем новую запись
    new_record = {'ID': new_id}

    # Валидируем и преобразуем значения
    for i, column in enumerate(data_columns):
        value = values[i]
        col_type = table_structure[column]

        try:
            if col_type == 'int':
                new_record[column] = int(value)
            elif col_type == 'bool':
                if value.lower() in ['true', '1', 'yes', 'да']:
                    new_record[column] = True
                elif value.lower() in ['false', '0', 'no', 'нет']:
                    new_record[column] = False
                else:
                    raise ValueError(f"Некорректное булево значение: {value}")
            else:  # str
                if (value.startswith('"') and value.endswith('"')) or \
                   (value.startswith("'") and value.endswith("'")):
                    value = value[1:-1]
                new_record[column] = value
        except ValueError as e:
            print(f'❌ Ошибка преобразования типа для столбца {column}: {e}')
            return

    # Добавляем запись и сохраняем
    table_data.append(new_record)
    save_table_data(table_name, table_data)
    print(f'✅ Запись с ID={new_id} успешно добавлена в таблицу "{table_name}".')


def _perform_select(metadata, table_name, where_clause=None):
    """
    Внутренняя функция для выполнения SELECT (отделена для кэширования).
    """
    from prettytable import PrettyTable

    from .utils import load_table_data

    table_data = load_table_data(table_name)

    if not table_data:
        print("📭 Таблица пуста.")
        return

    # Фильтруем данные если есть условие
    if where_clause:
        column, value = where_clause
        filtered_data = []
        for record in table_data:
            record_value = record.get(column)
            if str(record_value) == value:
                filtered_data.append(record)
        table_data = filtered_data

    # Создаем красивую таблицу для вывода
    table = PrettyTable()
    table.field_names = metadata[table_name].keys()

    for record in table_data:
        row = [record.get(field, '') for field in table.field_names]
        table.add_row(row)

    print(table)


@handle_db_errors
@log_time
def select(metadata, table_name, where_clause=None):
    """
    Выбирает данные из таблицы.
    """
    if table_name not in metadata:
        print(f'❌ Ошибка: Таблица "{table_name}" не существует.')
        return

    # Используем кэширование для часто выполняемых запросов
    if CACHE_ENABLED and where_clause:
        cache_key = f"select_{table_name}_{where_clause[0]}_{where_clause[1]}"
        cacher(cache_key, lambda: _perform_select(metadata, table_name, where_clause))
    else:
        _perform_select(metadata, table_name, where_clause)


@handle_db_errors
@log_time
def update(metadata, table_name, set_clause, where_clause):
    """
    Обновляет данные в таблице.
    """
    if table_name not in metadata:
        print(f'❌ Ошибка: Таблица "{table_name}" не существует.')
        return

    table_data = load_table_data(table_name)
    table_structure = metadata[table_name]
    updated_count = 0

    set_column, new_value = set_clause
    where_column, where_value = where_clause

    # Проверяем существование столбцов
    if set_column not in table_structure:
        print(f'❌ Ошибка: Столбец "{set_column}" не существует.')
        return

    if where_column not in table_structure:
        print(f'❌ Ошибка: Столбец "{where_column}" не существует.')
        return

    # Обновляем записи
    for record in table_data:
        if str(record.get(where_column)) == where_value:
            # Преобразуем новое значение к правильному типу
            col_type = table_structure[set_column]
            try:
                if col_type == 'int':
                    record[set_column] = int(new_value)
                elif col_type == 'bool':
                    if new_value.lower() in ['true', '1', 'yes', 'да']:
                        record[set_column] = True
                    elif new_value.lower() in ['false', '0', 'no', 'нет']:
                        record[set_column] = False
                    else:
                        raise ValueError(f"Некорректное булево значение: {new_value}")
                else:  # str
                    record[set_column] = new_value
                updated_count += 1
            except ValueError as e:
                print(f'❌ Ошибка преобразования типа: {e}')
                return

    if updated_count > 0:
        save_table_data(table_name, table_data)
        print(f'✅ Обновлено {updated_count} записей в таблице "{table_name}".')
    else:
        print('❌ Записи для обновления не найдены.')


@handle_db_errors
@confirm_action("удаление записей")
@log_time
def delete(metadata, table_name, where_clause):
    """
    Удаляет данные из таблицы.
    """
    if table_name not in metadata:
        print(f'❌ Ошибка: Таблица "{table_name}" не существует.')
        return

    table_data = load_table_data(table_name)
    where_column, where_value = where_clause

    if where_column not in metadata[table_name]:
        print(f'❌ Ошибка: Столбец "{where_column}" не существует.')
        return

    # Фильтруем записи
    original_count = len(table_data)
    table_data = [record for record in table_data 
                 if str(record.get(where_column)) != where_value]

    deleted_count = original_count - len(table_data)

    if deleted_count > 0:
        save_table_data(table_name, table_data)
        print(f'✅ Удалено {deleted_count} записей из таблицы "{table_name}".')
    else:
        print('❌ Записи для удаления не найдены.')


@handle_db_errors
def info(metadata, table_name):
    """
    Показывает информацию о таблице.
    """
    if table_name not in metadata:
        print(f'❌ Ошибка: Таблица "{table_name}" не существует.')
        return

    table_structure = metadata[table_name]
    table_data = load_table_data(table_name)

    print(f'📊 Таблица: {table_name}')
    columns_str = ", ".join([f"{col}:{typ}" for col, typ in table_structure.items()])
    print(f'📝 Столбцы: {columns_str}')
    print(f'📈 Количество записей: {len(table_data)}')
