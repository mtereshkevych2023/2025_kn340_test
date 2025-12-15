import string
from random import choice
from typing import List, Set
from lab.file_module import get_n_random_words

WORDS = get_n_random_words(5)
print(f"Слова для вгадування: {WORDS}")


def choose_secret_word(words: List[str]) -> str:
    return choice(words)


def enter_letter_from_user() -> str:
    letter = str(input("Введіть одну літеру: ")).lower()
    return list(letter.lower())[0]


def check_letters_in_word(letters: Set[str], word: str) -> str:
    if word == "":
        raise ValueError("Слово не має бути порожнім")
    if not isinstance(word, str):
        raise TypeError("Слово має бути рядком")
    if len(letters) == 0:
        raise ValueError("Буква не має бути порожньою")
    if letters - set(string.ascii_lowercase):
        raise ValueError("Літери мають бути латинськими")
    return "".join([l if l in letters else "*" for l in word])


def check_if_word_guessed(letters: Set[str], word: str) -> bool:
    if all(l in letters for l in word):
        print(f"Ви вгадали букву !")
        return True

    return False


def main():
    secret_word = choose_secret_word(WORDS)
    # print(f"Загадане слово: {secret_word}")
    entered_user_letters = set()
    for _ in range(len(secret_word) + 3):
        entered_user_letters.add(enter_letter_from_user())
        result = check_letters_in_word(entered_user_letters, secret_word)
        print(f"Результат перевірки літери '{entered_user_letters}' у слові: {result}")
        if check_if_word_guessed(entered_user_letters, secret_word):
            break
    if not check_if_word_guessed(entered_user_letters, secret_word):
        print(f"Ви не вгадали СЛОВО !")
    print("Гру завершено! загадане слово було:", secret_word)


if __name__ == "__main__":
    main()
