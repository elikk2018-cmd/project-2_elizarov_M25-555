"""
Модуль движка базы данных.
Отвечает за основной цикл программы и обработку команд.
"""

import shlex

from .core import (
    create_table,
    delete,
    drop_table,
    info,
    insert,
    list_tables,
    select,
    update,
)
from .parser import parse_set, parse_where
from .utils import load_metadata


def run():
    """
    Основная функция запуска приложения.
    """
    print("***Операции с данными***")
    print_crud_help()

    while True:
        try:
            user_input = input(">>>Введите команду: ").strip()
            if not user_input:
                continue

            parts = shlex.split(user_input)
            command = parts[0].lower()

            if command == 'exit':
                print("Выход из программы.")
                break
            elif command == 'help':
                print_crud_help()
            else:
                metadata = load_metadata()

                # Команды управления таблицами
                if command == 'create_table':
                    if len(parts) < 3:
                        print("Ошибка: Недостаточно аргументов.")
                    else:
                        table_name = parts[1]
                        columns = parts[2:]
                        create_table(metadata, table_name, columns)

                elif command == 'drop_table':
                    if len(parts) < 2:
                        print("Ошибка: Не указано имя таблицы.")
                    else:
                        table_name = parts[1]
                        drop_table(metadata, table_name)

                elif command == 'list_tables':
                    list_tables(metadata)

                # CRUD операции
                elif command == 'insert':
                    if len(parts) >= 4 and parts[1] == 'into' and parts[3] == 'values':
                        table_name = parts[2]
                        values_str = ' '.join(parts[4:])
                        insert(metadata, table_name, values_str)
                    else:
                        print("Ошибка: Неверный формат команды insert.")

                elif command == 'select':
                    if len(parts) >= 3 and parts[1] == 'from':
                        table_name = parts[2]
                        if len(parts) > 4 and parts[3] == 'where':
                            try:
                                where_clause = parse_where(parts[4:])
                                select(metadata, table_name, where_clause)
                            except Exception as e:
                                print(f"Ошибка парсинга условия WHERE: {e}")
                        else:
                            select(metadata, table_name)
                    else:
                        print("Ошибка: Неверный формат команды select.")

                elif command == 'update':
                    if len(parts) >= 8 and parts[2] == 'set' and parts[5] == 'where':
                        table_name = parts[1]
                        try:
                            set_clause = parse_set(parts[3:5])
                            where_clause = parse_where(parts[6:8])
                            update(metadata, table_name, set_clause, where_clause)
                        except Exception as e:
                            print(f"Ошибка парсинга: {e}")
                    else:
                        print("Ошибка: Неверный формат команды update.")

                elif command == 'delete':
                    if len(parts) >= 5 and parts[1] == 'from' and parts[3] == 'where':
                        table_name = parts[2]
                        try:
                            where_clause = parse_where(parts[4:6])
                            delete(metadata, table_name, where_clause)
                        except Exception as e:
                            print(f"Ошибка парсинга условия WHERE: {e}")
                    else:
                        print("Ошибка: Неверный формат команды delete.")

                elif command == 'info':
                    if len(parts) >= 2:
                        table_name = parts[1]
                        info(metadata, table_name)
                    else:
                        print("Ошибка: Не указано имя таблицы.")

                else:
                    print(f"Функции '{command}' нет. Попробуйте снова.")

        except KeyboardInterrupt:
            print("\nВыход из программы.")
            break
        except Exception as e:
            print(f"Произошла ошибка: {e}")


def print_crud_help():
    """
    Выводит справочную информацию по CRUD командам.
    """
    print("\n***Операции с данными***")
    print("Функции:")
    print("<command> insert into <имя_таблицы> values (<значение1>, <значение2>, ...) - создать запись")
    print("<command> select from <имя_таблицы> where <столбец> = <значение> - прочитать записи по условию")
    print("<command> select from <имя_таблицы> - прочитать все записи")
    print("<command> update <имя_таблицы> set <столбец1> = <новое_значение1> where <столбец_условия> = <значение_условия> - обновить запись")
    print("<command> delete from <имя_таблицы> where <столбец> = <значение> - удалить запись")
    print("<command> info <имя_таблицы> - вывести информацию о таблице")
    print("\nУправление таблицами:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")
