def strict(func):
    """Декоратор для проверки типов аргументов функции."""

    def wrapper(*args, **kwargs):
        # Получаем аннотации типов аргументов функции
        type_hints = func.__annotations__

        # Проверяем позиционные аргументы
        arg_names = func.__code__.co_varnames
        for i, arg_value in enumerate(args):
            if i >= len(arg_names):
                break

            arg_name = arg_names[i]
            if arg_name in type_hints:
                expected_type = type_hints[arg_name]
                if not isinstance(arg_value, expected_type):
                    raise TypeError(
                        f"Аргумент '{arg_name}' должен быть типа {expected_type.__name__}, "
                        f"а передан {type(arg_value).__name__}"
                    )

        # Проверяем именованные аргументы
        for arg_name, arg_value in kwargs.items():
            if arg_name in type_hints:
                expected_type = type_hints[arg_name]
                if not isinstance(arg_value, expected_type):
                    raise TypeError(
                        f"Аргумент '{arg_name}' должен быть типа {expected_type.__name__}, "
                        f"а передан {type(arg_value).__name__}"
                    )


        return func(*args, **kwargs)

    return wrapper


@strict
def sum_two(a: int, b: int) -> int:
    return a + b


print(sum_two(1, 2))  # Выведет: 3
try:
    print(sum_two(1, 2.4))  # Вызовет TypeError
except TypeError as e:
    print(f"Ошибка: {e}")