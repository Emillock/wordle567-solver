import numpy as np
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

def calculate_position_frequencies(words, word_length):
  
    # x 26 letters
    freq_matrix = np.zeros((word_length, 26))
    
    for word in words:
        for pos, letter in enumerate(word):
            if letter.isalpha():
                letter_idx = ord(letter) - ord('a')
                freq_matrix[pos][letter_idx] += 1
    
    # Convert to percentages
    for pos in range(word_length):
        total = freq_matrix[pos].sum()
        if total > 0:
            freq_matrix[pos] = (freq_matrix[pos] / total) * 100
    
    return freq_matrix
def main():
    print("Loading word list")
    words = load_words()
    print(f"Total words: {len(words):,}")
    
    print("\nSeparating by length")
    words_5, words_6, words_7 = separate_by_length(words)
    print(f"5-letter words: {len(words_5):,}")
    print(f"6-letter words: {len(words_6):,}")
    print(f"7-letter words: {len(words_7):,}")
    print("\nCalculating position frequencies for 5-letter words...")
    freq_5 = calculate_position_frequencies(words_5, 5)
    
    letters = [chr(i) for i in range(ord('a'), ord('z')+1)]
    pos_0_freq = freq_5[0]
    top_3_indices = np.argsort(pos_0_freq)[-3:][::-1]
    
    print("\nTop 3 letters at position 1:")
    for idx in top_3_indices:
        print(f"  {letters[idx]}: {pos_0_freq[idx]:.2f}%")

if __name__ == "__main__":
    main()