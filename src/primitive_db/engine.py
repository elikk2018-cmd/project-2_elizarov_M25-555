"""
Модуль движка базы данных.
Отвечает за основной цикл программы и обработку команд.
"""

import shlex

from .core import create_table, drop_table, list_tables
from .utils import load_metadata


def run():
    """
    Основная функция запуска приложения.
    """
    print("***База данных***")
    print_help()

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
                print_help()
            else:
                metadata = load_metadata()

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

                else:
                    print(f"Функции '{command}' нет. Попробуйте снова.")

        except KeyboardInterrupt:
            print("\nВыход из программы.")
            break
        except Exception as e:
            print(f"Произошла ошибка: {e}")


def print_help():
    """
    Выводит справочную информацию по доступным командам.
    """
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")
