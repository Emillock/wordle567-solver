from collections import Counter
from typing import Dict, List

#Word List
def load_valid_words(path: str = 'valid_words.txt', letters_number:int=5) -> List[str]:
    #Loads 5-letter words from the specified file path

    #In case of error, will use sample words
    sample_words = ["crane", "train", "power", "sheep", "light"]
    words = []

    try:
        with open(path, 'r') as file:
            #Store all words in lowercase and strip whitespace
            words = [line.strip().lower() for line in file.readlines()]
    except FileNotFoundError:
        print(f"Error: {path} not found. Using a sample list for simulation.")
        words = sample_words

    #Filter the list to make sure only 5-letter words are used
    n_letter_words = [w for w in words if len(w) == letters_number]

    if not n_letter_words:
        print(f"Warning: No {letters_number}-letter words found. Using sample list.")
        return sample_words

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