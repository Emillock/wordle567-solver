#
#word list
def load_words(filepath='valid_words.txt'):
    """Load all valid words from the dataset"""
    with open(filepath, 'r') as file:
        words = [line.strip().lower() for line in file.readlines()]
    return words
def separate_by_length(words):
    """Separate words into 5, 6, and 7-letter categories"""
    words_5 = [w for w in words if len(w) == 5]
    words_6 = [w for w in words if len(w) == 6]
    words_7 = [w for w in words if len(w) == 7]
    return words_5, words_6, words_7
def main():
    print("Loading word list")
    words = load_words()
    print(f"Total words: {len(words):,}")
    
    print("\nSeparating by length")
    words_5, words_6, words_7 = separate_by_length(words)
    print(f"5-letter words: {len(words_5):,}")
    print(f"6-letter words: {len(words_6):,}")
    print(f"7-letter words: {len(words_7):,}")

if __name__ == "__main__":
    main()