"""
Модуль движка базы данных.
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
from .decorators import handle_db_errors
from .parser import parse_set, parse_where
from .utils import load_metadata


@handle_db_errors
def run():
    """
    Основная функция запуска приложения.
    """
    print("🚀 *** ПРИМИТИВНАЯ БАЗА ДАННЫХ ***")
    print("📖 Используйте 'help' для списка команд или 'exit' для выхода")
    print_crud_help()

    while True:
        try:
            user_input = input("\n>>> Введите команду: ").strip()
            if not user_input:
                continue

            parts = shlex.split(user_input)
            command = parts[0].lower()

            if command == 'exit':
                print("👋 Выход из программы. До свидания!")
                break
            elif command == 'help':
                print_crud_help()
            else:
                metadata = load_metadata()

                # Команды управления таблицами
                if command == 'create_table':
                    if len(parts) < 3:
                        print("❌ Ошибка: Недостаточно аргументов.")
                        print("📝 Формат: create_table <имя> <столбец1:тип> ...")
                    else:
                        table_name = parts[1]
                        columns = parts[2:]
                        create_table(metadata, table_name, columns)

                elif command == 'drop_table':
                    if len(parts) < 2:
                        print("❌ Ошибка: Не указано имя таблицы.")
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
                        print("❌ Ошибка: Неверный формат команды insert.")
                        print("📝 Формат: insert into <таблица> values (значение1, значение2, ...)")

                elif command == 'select':
                    if len(parts) >= 3 and parts[1] == 'from':
                        table_name = parts[2]
                        if len(parts) > 4 and parts[3] == 'where':
                            try:
                                where_clause = parse_where(parts[4:])
                                select(metadata, table_name, where_clause)
                            except Exception as e:
                                print(f"❌ Ошибка парсинга условия WHERE: {e}")
                        else:
                            select(metadata, table_name)
                    else:
                        print("❌ Ошибка: Неверный формат команды select.")
                        print("📝 Формат: select from <таблица> [where столбец = значение]")

                elif command == 'update':
                    if len(parts) >= 8 and parts[2] == 'set' and parts[5] == 'where':
                        table_name = parts[1]
                        try:
                            set_clause = parse_set(parts[3:5])
                            where_clause = parse_where(parts[6:8])
                            update(metadata, table_name, set_clause, where_clause)
                        except Exception as e:
                            print(f"❌ Ошибка парсинга: {e}")
                    else:
                        print("❌ Ошибка: Неверный формат команды update.")
                        print("📝 Формат: update <таблица> set <столбец>=<значение> where <столбец>=<значение>")

                elif command == 'delete':
                    if len(parts) >= 5 and parts[1] == 'from' and parts[3] == 'where':
                        table_name = parts[2]
                        try:
                            where_clause = parse_where(parts[4:6])
                            delete(metadata, table_name, where_clause)
                        except Exception as e:
                            print(f"❌ Ошибка парсинга условия WHERE: {e}")
                    else:
                        print("❌ Ошибка: Неверный формат команды delete.")
                        print("📝 Формат: delete from <таблица> where <столбец>=<значение>")

                elif command == 'info':
                    if len(parts) >= 2:
                        table_name = parts[1]
                        info(metadata, table_name)
                    else:
                        print("❌ Ошибка: Не указано имя таблицы.")

                else:
                    print(f"❌ Неизвестная команда: '{command}'")
                    print("💡 Используйте 'help' для просмотра доступных команд")

        except KeyboardInterrupt:
            print("\n👋 Выход из программы. До свидания!")
            break
        except Exception as e:
            print(f"❌ Произошла непредвиденная ошибка: {e}")


def print_crud_help():
    """
    Выводит справочную информацию по командам.
    """
    print("\n" + "="*50)
    print("🎯 **ДОСТУПНЫЕ КОМАНДЫ**")
    print("="*50)
    
    print("\n📊 **ОПЕРАЦИИ С ДАННЫМИ:**")
    print("  insert into <таблица> values (знач1, знач2, ...) - создать запись")
    print("  select from <таблица> [where столбец=значение]   - прочитать записи")
    print("  update <таблица> set столбец=значение where ...  - обновить запись")
    print("  delete from <таблица> where столбец=значение     - удалить запись")
    print("  info <таблица>                                   - информация о таблице")
    
    print("\n🗂️  **УПРАВЛЕНИЕ ТАБЛИЦАМИ:**")
    print("  create_table <таблица> <столбец1:тип> ...        - создать таблицу")
    print("  list_tables                                       - список таблиц")
    print("  drop_table <таблица>                              - удалить таблицу")
    
    print("\n🔧 **ОБЩИЕ КОМАНДЫ:**")
    print("  exit                                              - выход")
    print("  help                                              - справка")
    
    print("\n💡 **ПРИМЕРЫ:**")
    print("  create_table users name:str age:int is_active:bool")
    print("  insert into users values (\"Иван\", 25, true)")
    print("  select from users where age = 25")
    print("="*50)
