import numpy as np

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
    """Calculate letter frequency for each position"""
    freq_matrix = np.zeros((word_length, 26))
    
    for word in words:
        for pos, letter in enumerate(word):
            if letter.isalpha():
                letter_idx = ord(letter) - ord('a')
                freq_matrix[pos][letter_idx] += 1
    
    for pos in range(word_length):
        total = freq_matrix[pos].sum()
        if total > 0:
            freq_matrix[pos] = (freq_matrix[pos] / total) * 100
    
    return freq_matrix