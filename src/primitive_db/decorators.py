"""
Декораторы для улучшения функциональности и обработки ошибок.
"""

import functools
import time

from .constants import CONFIRM_MESSAGES, ERROR_MESSAGES


def handle_db_errors(func):
    """
    Декоратор для обработки ошибок базы данных.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print(ERROR_MESSAGES["FILE_NOT_FOUND"])
        except KeyError as e:
            print(ERROR_MESSAGES["KEY_ERROR"].format(e))
        except ValueError as e:
            print(ERROR_MESSAGES["VALUE_ERROR"].format(e))
        except Exception as e:
            print(ERROR_MESSAGES["UNEXPECTED_ERROR"].format(e))
    return wrapper


def confirm_action(action_name):
    """
    Декоратор для подтверждения опасных операций.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            template = '❓ Вы уверены, что хотите выполнить "{}"? [y/n]: '
            prompt = template.format(action_name)
            response = input(prompt).strip().lower()
            if response == 'y':
                return func(*args, **kwargs)
            else:
                print(CONFIRM_MESSAGES["ACTION_CANCELLED"])
                return None
        return wrapper
    return decorator


def log_time(func):
    """
    Декоратор для логирования времени выполнения.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.monotonic()
        result = func(*args, **kwargs)
        end_time = time.monotonic()
        execution_time = end_time - start_time
        msg = f"⏱️  Функция {func.__name__} выполнилась за {execution_time:.3f} секунд"
        print(msg)
        return result
    return wrapper


def create_cacher():
    """
    Фабрика для создания кэшера с замыканием.
    """
    cache = {}
    
    def cache_result(key, value_func):
        if key in cache:
            msg = f"♻️  Используем кэшированный результат для ключа: {key}"
            print(msg)
            return cache[key]
        else:
            value = value_func()
            cache[key] = value
            msg = f"💾 Сохраняем в кэш для ключа: {key}"
            print(msg)
            return value
    
    return cache_result


# Создаем глобальный экземпляр кэшера
cacher = create_cacher()
