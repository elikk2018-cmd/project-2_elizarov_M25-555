"""
Константы проекта.
Централизованное хранение всех строковых и числовых констант.
"""

# Пути к файлам
META_FILE = "db_meta.json"
DATA_DIR = "data"

# Поддерживаемые типы данных
VALID_TYPES = {'int', 'str', 'bool'}

# Сообщения для пользователя
WELCOME_MESSAGE = "***База данных***"
EXIT_MESSAGE = "Выход из программы."
ERROR_MESSAGE_TABLE_EXISTS = 'Ошибка: Таблица "{}" уже существует.'
ERROR_MESSAGE_TABLE_NOT_EXISTS = 'Ошибка: Таблица "{}" не существует.'
SUCCESS_MESSAGE_TABLE_CREATED = 'Таблица "{}" успешно создана со столбцами: {}'
SUCCESS_MESSAGE_TABLE_DROPPED = 'Таблица "{}" успешно удалена.'
ERROR_MESSAGE_INVALID_TYPE = 'Ошибка: Неподдерживаемый тип данных "{}".'
ERROR_MESSAGE_INVALID_COLUMN_FORMAT = 'Ошибка: Некорректный формат столбца "{}".'