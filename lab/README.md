# Звіт до лабораторної роботи №1
## Тема: Основи тестування, Unit-тестування та Mock об'єкти
### Мета роботи
Вивчити основні принципи автоматичного тестування коду, опанувати бібліотеки `unittest` та `pytest`, навчитися використовувати Mock об'єкти для мокування функцій, та аналізувати покриття коду за допомогою `coverage`.

---

## 1. Введення - Assert та базова валідація

На першому етапі ми ознайомилися з механізмом `assert` для перевірки правильності умов у коді.

### 1.1 Теорія assert

`assert` — це вбудований механізм Python для перевірки тверджень. Якщо умова хибна, викидається виключення `AssertionError`.

Синтаксис:
```python
assert умова, "Повідомлення про помилку"
```

### 1.2 Практичні приклади

#### Приклад з test_file_module.py
У проекті використовується валідація у функції `get_n_random_words()`:

```python
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
```

#### Приклад з main.py
Валідація вхідних даних у функції `check_letters_in_word()`:

```python
def check_letters_in_word(letters: Set[str], word: str) -> str:
    if word == "":
        raise ValueError("Слово не має бути порожнім")
    if not isinstance(word, str):
        raise TypeError("Слово має бути рядком")
    if len(letters) == 0:
        raise ValueError("Буква не має бути порожньою")
    if letters - set(string.ascii_lowercase):
        raise ValueError("Літери мають бути латинськими")
```

### 1.3 Застосування у проекті

Валідація була застосована для:
- Перевірки типів даних (int для кількості слів, str для слова, Set для букв)
- Контролю діапазонів (n > 0, n <= len(INITIAL_WORDS))
- Перевірки користувацького вводу (тільки латинські букви)
- Перевірки порожніх значень

---

## 2. Unit-тестування з unittest

Unit-тести перевіряють окремі функції та методи, порівнюючи очікувані результати з фактичними.

### 2.1 Основи unittest

`unittest` — вбудована в Python бібліотека для написання та запуску тестів. Ключові компоненти:
- `TestCase` — базовий клас для тестових класів
- `setUp()` — виконується перед кожним тестом
- `tearDown()` — виконується після кожного тесту
- `setUpClass()` — виконується один раз на початку класу
- Методи перевірки: `assertEqual()`, `assertTrue()`, `assertRaises()`, `assertIn()` та інші

### 2.2 Структура тестів у проекті

Файл: [tests/test_main.py](tests/test_main.py)

#### Клас 1: TestWordChoice
Тестування функції вибору секретного слова `choose_secret_word()`:

```python
class TestWordChoice(unittest.TestCase):
    def test_word_in_list(self):
        """Перевіряємо чи вибране слово є в списку слів"""
        word = choose_secret_word(WORDS)
        self.assertIn(word, WORDS)

    def test_word_is_string(self):
        """Перевіряємо чи вибране слово є рядком"""
        word = choose_secret_word(WORDS)
        self.assertIsInstance(word, str)

    def test_word_length(self):
        """Перевіряємо довжину вибраного слова"""
        word = choose_secret_word(WORDS)
        self.assertGreater(len(word), 0)
        self.assertLessEqual(len(word), 20)

    def test_empty_list(self):
        """Перевіряємо обробку порожнього списку слів"""
        with self.assertRaises(IndexError):
            choose_secret_word([])
```

#### Клас 2: TestEnterLetterFromUser
Тестування введення букви користувачем з використанням Mock об'єктів:

```python
class TestEnterLetterFromUser(unittest.TestCase):
    @patch("builtins.input", side_effect=["1", "a"])
    def test_enter_letter_from_user(self, mock_input):
        self.assertEqual(enter_letter_from_user(), "1")
        self.assertEqual(enter_letter_from_user(), "a")
```

Тут використовується декоратор `@patch` для мокування функції `input()`. Це дозволяє автоматизувати введення без ручного набору.

#### Клас 3: TestCheckLettersInWord
Найбільший та найдетальніший клас з тестуванням функції перевірки букв у слові:

```python
class TestCheckLettersInWord(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.empty_test_word = ""
        return super().setUpClass()

    def setUp(self):
        # Підготовка тестових даних
        letters_to_guess = set("abcdefghijklmnopqrstuvwxyz")
        self.test_word = "".join(
            random.choices(list(letters_to_guess), k=random.randint(3, 8))
        )
        self.guess_letters = letters_to_guess
        self.no_letters = set()

    def tearDown(self):
        # Очищення даних
        self.test_word = None
        self.guess_letters = None
        self.no_letters = None
```

**Методи тестування:**

- `test_user_entered_cyrillic_letter()` — перевіряємо що функція піднімає помилку для кириличних букв
- `test_all_letters_guessed()` — коли всі букви вгадано, повинна повернутись саме слово
- `test_no_letters_guessed()` — порожній набір букв викликає ValueError
- `test_some_letters_guessed()` — частичне вгадування показує "*" на місце невгаданих букв
- `test_repeated_letters()` — правильна обробка повторюваних букв
- `test_valid_interface_arguments()` — перевірка типів аргументів (str, set)
- `test_empty_word()` — порожне слово викликає помилку
- `test_empty_letters()` — порожний набір букв викликає помилку

#### Клас 4: TestCheckIfWordGuessed
Тестування функції перевірки успішного вгадування слова:

```python
class TestCheckIfWordGuessed(unittest.TestCase):
    def setUp(self):
        self.test_word = "test"
        self.all_letters = set(self.test_word)
        self.partial_letters = {"t", "e"}
        self.no_letters = set()
        self.extra_letters = set("testzxy")

    def test_word_fully_guessed(self):
        """Всі літери вгадано"""
        self.assertTrue(check_if_word_guessed(self.all_letters, self.test_word))

    def test_word_partially_guessed(self):
        """Не всі літери вгадано"""
        self.assertFalse(check_if_word_guessed(self.partial_letters, self.test_word))

    def test_extra_letters_guessed(self):
        """Зайві літери не впливають на результат"""
        self.assertTrue(check_if_word_guessed(self.extra_letters, self.test_word))
```

### 2.3 Запуск unittest тестів

```bash
# Запуск всіх тестів
python -m unittest discover -s tests -v

# Запуск конкретного файлу
python -m unittest tests.test_main -v

# Запуск конкретного класу
python -m unittest tests.test_main.TestWordChoice -v

# Запуск конкретного методу
python -m unittest tests.test_main.TestWordChoice.test_word_in_list -v
```

### 2.4 Результати unittest

Тести виконуються успішно. Використовується також функція `test_func_check_if_word_guessed()` з мокуванням print:

```python
def test_func_check_if_word_guessed():
    with patch("builtins.print") as mock_print:
        result = check_if_word_guessed({"a", "b", "c"}, "abc")
        mock_print.assert_called_with("Ви вгадали букву !")
        assert result is True
```

---

## 3. PyTest як альтернатива unittest

### 3.1 Встановлення

```bash
pip install pytest
```

### 3.2 Теорія PyTest

PyTest — сучасна альтернатива unittest з простішим синтаксисом:

| Аспект | unittest | pytest |
|--------|----------|--------|
| Синтаксис | Класи + методи | Функції |
| Асерти | `self.assertEqual()` | Прямий `assert` |
| Фікстури | `setUp()` / `tearDown()` | `@pytest.fixture` |
| Запуск | `python -m unittest` | `pytest` |

### 3.3 Структура тестів PyTest

Файл: [tests/test_file_module.py](tests/test_file_module.py)

```python
def test_get_n_random_words():
    """
    Перевіряємо чи функція повертає правильну кількість слів
    """
    for n in range(1, 6):
        words = get_n_random_words(n)
        assert len(words) == n, f"Expected {n} words, got {len(words)}"


def test_get_n_random_words_raise_value_error():
    """
    Перевіряємо чи функція піднімає ValueError для невалідних параметрів
    """
    invalid_inputs = [-1, 0, 1.5, 2.5, 50]
    for n in invalid_inputs:
        with pytest.raises(ValueError):
            get_n_random_words(n)


def test_get_n_random_words_expect_print_outputs():
    """
    Перевіряємо виводи функції з мокуванням print
    """
    with patch("builtins.print") as mock_print:
        for n in range(1, 6):
            get_n_random_words(n)
            mock_print.assert_called_with(f"Генерація {n} випадкових слів.")
```

### 3.4 Запуск PyTest

```bash
pytest -v
pytest tests/test_file_module.py -v
pytest tests/test_file_module.py::test_get_n_random_words -v
```

---

## 4. Mock об'єкти та патчування

Mock об'єкти — це об'єкти які імітують поведінку інших об'єктів. Це дозволяє тестувати код без залежностей від зовнішніх систем.

### 4.1 Приклади з коду

#### Мокування input()

```python
@patch("builtins.input", side_effect=["1", "a"])
def test_enter_letter_from_user(self, mock_input):
    self.assertEqual(enter_letter_from_user(), "1")
    self.assertEqual(enter_letter_from_user(), "a")
```

#### Мокування print()

```python
def test_func_check_if_word_guessed():
    with patch("builtins.print") as mock_print:
        result = check_if_word_guessed({"a", "b", "c"}, "abc")
        mock_print.assert_called_with("Ви вгадали букву !")
        assert result is True
```

Декоратор `@patch` замінює функцію на Mock об'єкт, який можна інспектувати та контролювати під час тесту.

---

## 5. Coverage - аналіз покриття коду

### 5.1 Поняття покриття

Покриття коду — це відсоток рядків коду які були виконані під час запуску тестів.

### 5.2 Встановлення

```bash
pip install coverage pytest-cov
```

### 5.3 Типи покриття

- **Line Coverage** — яка кількість рядків коду виконана
- **Branch Coverage** — які гілки (if/else) протестовані

---

## 6. Структура проекту

```
lab/
├── main.py                    # Основна гра
├── file_module.py             # Модуль для генерації слів
├── tests/
│   ├── test_main.py          # Тести для main.py (unittest)
│   ├── test_file_module.py    # Тести для file_module.py (pytest)
│   └── __init__.py
├── pyproject.toml            # Конфігурація проекту
└── 1.ipynb                    # Jupyter notebook
```

---

## 7. Висновки

### Опановані знання
- ✅ Механізм assert та валідація
- ✅ unittest: TestCase, setUp/tearDown, методи перевірки
- ✅ pytest: функції, асерти, обробка винятків
- ✅ Mock об'єкти та патчування функцій
- ✅ Аналіз покриття коду
- ✅ Структура тестів у реальному проекті

### Висновок

Лабораторна робота виконана успішно. Вивчено основні принципи автоматичного тестування та практично застосовано їх до реального проекту гри "Guess the word".
