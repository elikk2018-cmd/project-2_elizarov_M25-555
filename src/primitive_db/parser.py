"""
Парсер для сложных команд SQL-подобного синтаксиса.
"""


def parse_values(values_str):
    """
    Парсит значения из строки вида '(value1, value2, value3)'.
    """
    if values_str.startswith('(') and values_str.endswith(')'):
        values_str = values_str[1:-1]
    
    values = []
    current_value = ""
    in_quotes = False
    quote_char = None
    
    for char in values_str:
        if char in ['"', "'"] and not in_quotes:
            in_quotes = True
            quote_char = char
            current_value += char
        elif char == quote_char and in_quotes:
            in_quotes = False
            current_value += char
        elif char == ',' and not in_quotes:
            values.append(current_value.strip())
            current_value = ""
        else:
            current_value += char
    
    if current_value:
        values.append(current_value.strip())
    
    return values


def parse_where(where_parts):
    """
    Парсит условие WHERE.
    """
    if len(where_parts) != 3 or where_parts[1] != '=':
        raise ValueError("Некорректный формат условия WHERE")
    
    column = where_parts[0]
    value = where_parts[2]
    
    # Убираем кавычки для строковых значений
    if (value.startswith('"') and value.endswith('"')) or \
       (value.startswith("'") and value.endswith("'")):
        value = value[1:-1]
    
    return column, value


def parse_set(set_parts):
    """
    Парсит условие SET.
    """
    if len(set_parts) < 3 or set_parts[1] != '=':
        raise ValueError("Некорректный формат условия SET")
    
    column = set_parts[0]
    value = ' '.join(set_parts[2:])
    
    # Убираем кавычки для строковых значений
    if (value.startswith('"') and value.endswith('"')) or \
       (value.startswith("'") and value.endswith("'")):
        value = value[1:-1]
    
    return column, value
