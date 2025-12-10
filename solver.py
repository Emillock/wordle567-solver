import string
from typing import List, Dict
from itertools import product
lowercase_letters = list(string.ascii_lowercase)
print(lowercase_letters)
words_list_path = 'valid_words.txt'
with open(words_list_path, 'r') as file:
    words = [line.strip() for line in file.readlines()]


def solve_wordle(allowed_letters: List[List[str]], letters_number: int = 5):
    """Solve Wordle by generating all possible combinations of allowed letters.
    Args:
        allowed_letters (List[List[str]]): A list of lists, where each inner list contains
                                            the allowed letters for that position.
        letters_number (int): The number of letters in the Wordle word. Default is 5."""

    return list(filter(lambda w: len(w.strip()) == letters_number and (lambda word: all(c in allowed_letters[i] for i, c in enumerate(word.strip())))(w), words))
