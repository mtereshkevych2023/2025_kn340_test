# Цей модуль буде відповідати за генерацію слів які потрібно вгадати
import random

INITIAL_WORDS = [
    "apple",
    "banana",
    "cherry",
    "orange",
    "Python",
    "Developer",
    "function",
    "variable",
    "iteration",
    "condition",
]


def get_n_random_words(n: int) -> list:
    if n > len(INITIAL_WORDS):
        print("Неможливо згенерувати стільки слів.")
        raise ValueError("Кількість слів перевищує доступну.")
    elif not isinstance(n, int):
        print("Введено некоректне значення для кількості слів.")
        raise ValueError("n має бути додатним цілим числом.")
    elif n <= 0:
        print("Кількість слів має бути додатним цілим числом.")
        raise ValueError("n має бути додатним цілим числом.")
    else:
        print(f"Генерація {n} випадкових слів.")
    return [w.lower() for w in random.sample(INITIAL_WORDS, n)]


def func_for_module_import():
    return "Ця функція призначена для тестування імпорту модуля."


def test_func_return_value():
    """
    Пробуємо створити тест всередині модуля"""
    assert type(func_for_module_import()) is str, "Функція має повертати стрічку"
