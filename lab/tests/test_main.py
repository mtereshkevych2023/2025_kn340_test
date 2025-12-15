import random
import unittest
from unittest.mock import patch
from lab.main import *
from lab.file_module import func_for_module_import


def test_module_import():
    # Перевіряємо чи модуль імпортується коректно
    assert isinstance(func_for_module_import(), str), "Функція має повертати стрічку"


def test_always_failed_for_ci_demo():
    # Цей тест завжди падає для демонстрації CI
    assert True, "Цей тест завжди падає для демонстрації CI"


def test_func_check_if_word_guessed():
    # Тест який перевіряє чи при виклику функції був здійснений вивід через print
    # print буде викликатись тільки при правильно взагадних буквах
    with patch("builtins.print") as mock_print:
        result = check_if_word_guessed({"a", "b", "c"}, "abc")
        mock_print.assert_called_with("Ви вгадали букву !")
        assert result is True, "Функція має повертати True коли всі букви вгадані"


class TestWordChoice(unittest.TestCase):
    def test_word_in_list(self):
        """Перевіряємо чи вибране слово є в списку слів"""
        word = choose_secret_word(WORDS)
        self.assertIn(word, WORDS, f"Слово {word} має бути у списку {WORDS}")

    def test_word_is_string(self):
        """Перевіряємо чи вибране слово є рядком"""
        word = choose_secret_word(WORDS)
        self.assertIsInstance(word, str, f"Слово {word} має бути рядком")

    def test_word_length(self):
        """Перевіряємо довжину вибраного слова"""
        word = choose_secret_word(WORDS)
        self.assertGreater(len(word), 0, "Слово має бути не порожнім")
        self.assertLessEqual(len(word), 20, "Слово має бути не довшим за 20 символів")

    def test_word_not_numeric(self):
        """Перевіряємо чи вибране слово не є числом"""
        word = choose_secret_word(WORDS)
        self.assertFalse(word.isdigit(), f"Слово {word} не має бути числом")

    def test_word_not_empty(self):
        """Перевіряємо чи вибране слово не є порожнім"""
        word = choose_secret_word(WORDS)
        self.assertNotEqual(word, "", "Слово не має бути порожнім")

    def test_empty_list(self):
        """Перевіряємо обробку порожнього списку слів"""
        with self.assertRaises(IndexError):
            choose_secret_word([])


class TestEnterLetterFromUser(unittest.TestCase):
    @patch("builtins.input", side_effect=["1", "a"])
    def test_enter_letter_from_user(self, mock_input):
        self.assertEqual(enter_letter_from_user(), "1")
        self.assertEqual(enter_letter_from_user(), "a")

        # __builtins__.input = mock_input
        # try:
        #     self.assertEqual(enter_letter_from_user(), 'a')
        # finally:
        #     __builtins__.input = original_input


#     #########################################################################################################################
#     # Тут має бути новий метод - тільки перша буква буде зараховуватись
#     # Можна вводити більше однієї букви
#     # Вводити можна тільки латинські букви
#     #########################################################################################################################
#     def test_enter_multiple_letters(self):
#         for test_input in ['abcріап', 'bfd']:
#             with patch('builtins.input', return_value=test_input) as mock_input:
#                 self.assertEqual(enter_letter_from_user(), test_input[0])


class TestCheckLettersInWord(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("=== Запускаємо тести ===")
        cls.empty_test_word = ""
        return super().setUpClass()

    def setUp(self):
        print(">>> Приготуємо дані для тестів")
        letters_to_guess = set(
            [
                "a",
                "b",
                "c",
                "d",
                "e",
                "f",
                "g",
                "h",
                "i",
                "j",
                "k",
                "l",
                "m",
                "n",
                "o",
                "p",
                "q",
                "r",
                "s",
                "t",
                "u",
                "v",
                "w",
                "x",
                "y",
                "z",
            ]
        )

        self.test_word = "".join(
            random.choices(list(letters_to_guess), k=random.randint(3, 8))
        )
        self.guess_letters = letters_to_guess
        # Копіюємо класовий атрибут в атрибут екземпляра
        self.empty_test_word = self.__class__.empty_test_word
        # Сетапимо пусті значення для тестів які перевіряють на порожні дані
        self.no_letters = set()
        return super().setUp()

    def tearDown(self):
        print(">>> Видаляємо дані після тестів")
        self.test_word = None
        self.guess_letters = None
        self.no_letters = None
        return super().tearDown()

    def test_user_entered_cyrillic_letter(self):
        """
        Перевіряємо чи користувач ввів кириличну букву
        1. Якщо ввів кириличну букву, то функція має впасти з помилкою ValueError
        2. Якщо ввів латинську букву, то функція має працювати і повернути щось
        >>>Цей тест готовий<<<
        """
        print("||| Починаємо процес тестування |||")
        # self.assertFalse(True) # Ми хочемо щоб цей тест завжди впав
        with self.assertRaises(ValueError):
            check_letters_in_word({"а", "б", "в"}, self.test_word)
        result = check_letters_in_word({"a", "b", "c"}, self.test_word)
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)

    def test_all_letters_guessed(self):
        """
        Даний тест є валідний"""
        test_word = "apple"
        self.assertEqual(check_letters_in_word(set(test_word), test_word), test_word)

    def test_no_letters_guessed(self):
        """Перевіряємо випадок коли не вгадано жодної літери"""
        with self.assertRaises(ValueError):
            check_letters_in_word(set(), "banana")

    def test_some_letters_guessed(self):
        self.assertEqual(check_letters_in_word({"a", "n"}, "banana"), "*anana")

    def test_repeated_letters(self):
        self.assertEqual(check_letters_in_word({"b", "a"}, "banana"), "ba*a*a")

    #################################################################################################################################
    def test_valid_interface_arguments(self):
        """
        Перевіряємо чи функція працює з валідними аргументами
        Перевіряємо чи справді передаються слова і букви вірного типу
        1. Якщо ми передаємо неправильні типи то функція має впасти
        2. Якщо ми передаємо правильні типи то функція має працювати
        """

        # Ми виносимо ці змінні у setUp щоб не дублювати код
        # test_word = "ValideWord"
        # guess_letters = set(["a", "b", "c"])
        # Переприсвоювати змінні не потрібно, бо вони є в setUp
        test_word = self.test_word
        guess_letters = self.guess_letters
        print(f"test_word: {test_word}, guess_letters: {guess_letters}")
        # Не валідні типи
        for arg in [
            123,
            12.5,
            None,
        ]:
            with self.assertRaises(TypeError):
                check_letters_in_word(guess_letters, arg)

        # Це бага, тут неправильна поведінка, бо функція приймає список замість рядка
        # Тому ми переписали функцію щоб вона ловила цю помилку і не працювала з неправильними типами
        with self.assertRaises(TypeError):
            check_letters_in_word(guess_letters, ["a", "p", "p", "l", "e"])
        # Валідні типи
        self.assertIsInstance(test_word, str)
        self.assertIsInstance(guess_letters, set)

    def test_empty_word(self):
        """
        Перевіряємо чи вгадане слово є порожнім
        1. Передаємо порожне слово, виловлюємо помилку
        2. Передаємо слово і очікуємо що функція щось поверне
        >>>Цей тест готовий<<<
        """
        guess_letters = set(["a", "b"])

        with self.assertRaises(ValueError):
            check_letters_in_word(self.guess_letters, self.empty_test_word)
        self.assertGreater(
            len(check_letters_in_word(self.guess_letters, self.test_word)), 0
        )

    def test_empty_letters(self):
        """
        Перевірка на порожню букву.
        В даному тесті ми перевіряємо коли слово є а буква яка вгадується є порожньою
        >>>Цей тест готовий<<<
        """

        # Виловлюємо Помилку
        with self.assertRaises(ValueError):
            check_letters_in_word(self.no_letters, self.test_word)
        # Перевіряємо текст помилки, що це саме наша помилка яку ми написали
        with self.assertRaises(ValueError) as context:
            check_letters_in_word(self.no_letters, self.test_word)
            self.assertEqual(str(context.exception), "Слово не має бути порожнім")
        # Для контрольної перевірки передаємо букву і тут має бути повернутись значення
        # Якшо буква буде (при правильних даних) то функція щось поверне
        self.assertTrue(len(check_letters_in_word({"a"}, self.test_word)) > 0)


class TestCheckIfWordGuessed(unittest.TestCase):
    """Тести для перевірки функції check_if_word_guessed"""

    def setUp(self):
        """Підготовка даних для кожного тесту"""
        print(">>> Підготовка даних для тестів check_if_word_guessed")
        self.test_word = "test"
        self.all_letters = set(self.test_word)
        self.partial_letters = {"t", "e"}
        self.no_letters = set()
        self.extra_letters = set("testzxy")
        return super().setUp()

    def tearDown(self):
        """Очищення даних після кожного тесту"""
        print(">>> Очищення даних після тестів check_if_word_guessed")
        self.test_word = None
        self.all_letters = None
        self.partial_letters = None
        self.no_letters = None
        self.extra_letters = None
        return super().tearDown()

    def test_word_fully_guessed(self):
        """Перевіряємо випадок коли всі літери вгадано"""
        self.assertTrue(
            check_if_word_guessed(self.all_letters, self.test_word),
            f"Всі літери {self.all_letters} мають бути вгадані у слові {self.test_word}",
        )

    def test_word_partially_guessed(self):
        """Перевіряємо випадок коли вгадано не всі літери"""
        self.assertFalse(
            check_if_word_guessed(self.partial_letters, self.test_word),
            f"Не всі літери {self.partial_letters} вгадані у слові {self.test_word}",
        )

    def test_no_letters_guessed(self):
        """Перевіряємо випадок коли не вгадано жодної літери"""
        self.assertFalse(
            check_if_word_guessed(self.no_letters, self.test_word),
            f"Порожній набір літер {self.no_letters} не може вгадати слово {self.test_word}",
        )

    def test_extra_letters_guessed(self):
        """Перевіряємо випадок коли вгадано зайві літери"""
        self.assertTrue(
            check_if_word_guessed(self.extra_letters, self.test_word),
            f"Додаткові літери у наборі {self.extra_letters} не мають впливати на вгадування слова {self.test_word}",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
