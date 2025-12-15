from collections import Counter
from typing import Dict, List

#Word List
def load_valid_answers(letters_number:int=5) -> List[str]:
    #Loads n-letter words from the specified file path
    words = []

    try:
        with open(f'word_lists/answers_{letters_number}letter.txt', 'r') as f:
            words = [w.strip() for w in f.readlines()]
    except FileNotFoundError:
        print(f"Error: 'word_lists/answers_{letters_number}letter.txt' not found. Using a sample list for simulation.")
        return []

    #Filter the list to make sure only n-letter words are used
    n_letter_words = [w for w in words if len(w) == letters_number]

    if not n_letter_words:
        print(f"Warning: No {letters_number}-letter words found. Using sample list.")
        return []

    return n_letter_words

def max_letter_counts(words: List[str], letters_number:int=5) -> Dict[str, int]:
    """Return dict letter -> max count in any 5-letter word from words."""
    maxc = {chr(ord('a')+i): 0 for i in range(26)}
    for w in words:
        w = w.strip().lower()
        if len(w) != letters_number or not w.isalpha():
            continue
        cnt = Counter(w)
        for ch, v in cnt.items():
            if v > maxc[ch]:
                maxc[ch] = v
    return maxc